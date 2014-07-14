/* iequals
------------------------------
*  Checks if two strings are equal to each other (case insensitive).
*
*  Example: "A cool Surf" turns into "a-cool-surf"
*
*  RETURNS
*  bool
*  
------------------------------ */
if (typeof String.prototype.iequals === 'undefined') String.prototype.iequals = function(string) { return this.toLowerCase() === string.toLowerCase(); };

function getJSONVal(json, keys) {
	//console.log(json);
	//console.log(keys);
	//console.log(keys[0]);
	// If this is the last level of keys, return the object
	if (keys.length == 1 || typeof(json) == undefined) {
		//console.log("the last level");
		//console.log(json[keys[0]]);
		return json[keys[0]];
	} else {
		// Get the next level of json values
		json = json[keys[0]];
		
		// Remove the first element of the keys since we are now past that level
		keys.shift();
		
		// Recursive...get the JSON object at the next level of keys
		return getJSONVal(json, keys);
	}
}

function flipQuotes(str) {
  var result = [], i = 0, lim = str.length, c;

  for (; i < lim; i += 1) {
    c = str.charAt(i);
    switch(c) {
      case '"':
        result.push("'");
        break;

      case "'":
        result.push('"');
        break;

      default:
        result.push(c);
    }
  }

  return result.join('');
}

$(function() {

$ajaxGlobalFields = $("[data-ajax-global-update]");
$ajaxLocalFields = $("[data-ajax-update]");
$ajaxSurfices = $ajaxGlobalFields.is("[data-ajax-surfices]");
$ajaxSurfs = $ajaxGlobalFields.is("[data-ajax-surfs]");
$ajaxStatuses = $ajaxGlobalFields.is("[data-ajax-statuses]");
$ajaxSurfSurfices = $ajaxGlobalFields.is("[data-ajax-surfsurfices]");
$ajaxNotSurfSurfices = $ajaxGlobalFields.is("[data-ajax-notsurfsurfices]");


/* FORM SUBMIT
------------------------------ 
*  Automatically converts all data-name inputs into a JSON string.
*  That string is assigned to a hidden input in the form named "data"
*  
*  INPUT
*  form
* 
*  EVENT
*  submit
*
------------------------------ */
$("form").submit(function(e) { //listen for submit event
	var data = {};
	$(this).find("[data-name]").each(function() {
		
		// NOT GOOD PRACTICE. NEED TO MAKE MORE GENERIC
		// The only exception is for color which needs to be stored with the #
		if ($(this).attr("data-name") == "color") {
			data[$(this).attr("data-name")] = "#" + $(this).val();
		} else {
			data[$(this).attr("data-name")] = $(this).val();
		}
	});
	
	// If there were data fields found
	if (!jQuery.isEmptyObject(data)) {
		
		// Create the hidden input field that will store
		// the JSON data.
		var input = $("<input>", {
			type: "hidden",
			name: "data",
			value: JSON.stringify( data ).replace(/["]/g, "\"")
		});
		
		// Delete any input in this with name=data
		$(this).find("[name=data]").remove();
		
		// Append the input into the form
		$(this).append(input);
	}
	
});

/* AJAX FORM
------------------------------ 
*  Automatically makes any form with type=ajax only submit over AJAX
*  
*  INPUT
*  form[type='ajax']
* 
*  EVENT
*  submit
*
------------------------------ */
$("form[type='ajax']").on("submit", function(e) {
    e.preventDefault();
    
    // Give some feedback to the user
    // First get the submit button
    var $button = $(this).find('[type="submit"]');
    var $form = $(this);
    
    // Disable the button and add a flash animation (in css)
    $button.addClass("disabled");
	$button.addClass("flash");
	
	// Get the button text so we can replace it later
	$buttonText = $button.text();
	if ($button.attr("data-value-processing")) {
		$button.text($button.attr("data-value-processing"));
	} else {
		$button.text("Saving...");
	}
    
    // Serialize all the data in the form so that it can be passed
    var data = $(this).serialize();
    
    $.post(this.action, data,
    	// Get the response from the server
    	function(data, textStatus, jqXHR) {
    		
    		// If the submit succeeded
    		if ($button.attr("data-value-success")) {
    			$button.text($button.attr("data-value-success"));
    		} else {
				$button.text("Saved");
			}
			
			// (MOVE TO SEPARATE FUNCTION) Update all ajax fields
			
			//var $fields = $("[data-ajax-update=" + $form.attr("data-ajax-update-target") + "]");
			
			// Since new data has been added, refresh the ss object
			//ss.getSurfs();
			
			
			//refreshAJAXPage($form, $form.attr("data-ajax-action"), getData)
			//console.log(window.location.pathname + $form.attr("data-ajax-action"));
			
			// For testing purposes:
			// set the message to display: none to fade it in later.
			// var message = $('<div class="alert alert-error errormessage" style="display: none;">');
// 			// a close button
// 			var close = $('<button type="button" class="close" data dismiss="alert">&times</button>');
// 			message.append(close); // adding the close button to the message
// 			message.append(data); // adding the error response to the message
// 			// add the message element to the body, fadein, wait 3secs, fadeout
// 			message.appendTo($('body')).fadeIn(300).delay(3000).fadeOut(500);
			
			var notification = $form.attr("data-ajax-success");
			if (notification == "" || typeof notification === "undefined") notification = "Save successful."
			ss.notify("success", notification);
			
			refreshAJAXPage($form);
			/*
			$.getJSON(window.location.pathname + $form.attr("data-ajax-action"), getData)
				.done(function(data) {
					console.log(data);
					
					// Refresh the page with the JSON data
					refreshAJAXPage($form, data);
					
				})
				.fail(function(data) {
					
				});
			*/
			//field = $(this).attr("[data-ajax-update]");
			// $form.find("[data-ajax-update]").each(function() {
// 				
// 				
// 			});
			
			$button.removeClass("flash");
			setTimeout(function() {
				$button.removeClass("disabled");
				$button.text($buttonText);
			}, 750);
			//$button.text($buttonText);
    	})
		.done(function() {
			// Nothing here (same as above)
		})
		.fail(function() {
			
			if ($button.attr("data-value-fail")) {
    			$button.text($button.attr("data-value-fail"));
    		} else {
				$button.text("Failed");
			}
			
			// Get the button type so we can return to it after showing that it failed
			var originalBtnType = "";
			if ($button.hasClass("btn-danger")) originalBtnType = "btn-danger";
			else if ($button.hasClass("btn-default")) originalBtnType = "btn-default";
			else if ($button.hasClass("btn-primary")) originalBtnType = "btn-primary";
			else if ($button.hasClass("btn-success")) originalBtnType = "btn-success";
			else if ($button.hasClass("btn-info")) originalBtnType = "btn-info";
			else if ($button.hasClass("btn-warning")) originalBtnType = "btn-warning";
			else if ($button.hasClass("btn-link")) originalBtnType = "btn-link";
			
			$button.addClass("btn-danger").removeClass(originalBtnType);
			$button.removeClass("flash");
			
			var notification = $form.attr("data-ajax-fail");
			console.log(notification);
			if (notification == "" || typeof notification === "undefined") notification = "Save failed."
			ss.notify("danger", notification);
			
			setTimeout(function() {
				$button.removeClass("disabled");
				$button.removeClass("btn-danger").addClass(originalBtnType);
    			$button.text($buttonText);
			}, 750);
			
		})
		.always(function() {
    		// Nothing
		});
});

function sleep(milliseconds) {
   var currentTime = new Date().getTime();

   while (currentTime + milliseconds >= new Date().getTime()) {
   }
}


/* SUBMIT FORM
------------------------------ 
*  Automatically makes any modal box use its submit button to submit a form included
*  
*  INPUT
*  .modal [type="submit"]
* 
*  EVENT
*  click
*
------------------------------ */
$('.modal [type="submit"]').click(function(e) {
	e.preventDefault();
	$(this).parents(".modal").find("form").submit();
});


/* VALIDATION
------------------------------- */
function surfNameField($input) {
	
	var surfId = $input.closest("form").find('input[name="surf"]').val();
	
	// If the surfs array already exists, just fire the function without getting all the info
	// If surfs is empty, however, get the new data
	if (ss.surfs.length == 0) {
		console.log("getting new surfs");
		ss.getSurfs(function(data) {
			checkField();
		});
		
	} else {
		checkField();
	}
	
	// Create a closure for checking the field to comply with DRY programming
	function checkField() {
		// Loop through all the surfs to find a match
		// not including this current surf
		$.each(ss.surfs, function(key, surf) {
			//console.log($input.val().replace(/^\s+|\s+$/gm,'') + " - " + surf.name);
			//console.log($input.val().replace(/^\s+|\s+$/gm,'').iequals(surf.name));
			
			var val = $input.val().replace(/\s+/gm," ").trim();
			
			// If the name is blank, throw an error
			// Otherwise if the new name is the same as another
			// surf and that I'm not checking its own name,
			// throw an error.
			if (	val == "" ||
					(	surfId != surf.id &&
						val.iequals(surf.name)
					)
			) {
				$input.closest(".form-group").removeClass("has-success").addClass("has-error");
				return false;
			} else {
				$input.closest(".form-group").removeClass("has-error").addClass("has-success");
			}
		});
	}
}

function surficeNameField($input) {
	
	var surficeId = $input.closest("form").find('input[name="surfice"]').val();
	
	// If the surfs array already exists, just fire the function without getting all the info
	// If surfs is empty, however, get the new data
	if (ss.surfices.length == 0) {
		console.log("getting new surfices");
		ss.getSurfices(function(data) {
			checkField();
		});
		
	} else {
		checkField();
	}
	
	// Create a closure for checking the field to comply with DRY programming
	function checkField() {
		// Loop through all the surfs to find a match
		// not including this current surf
		$.each(ss.surfices, function(key, surfice) {
			//console.log($input.val().replace(/^\s+|\s+$/gm,'') + " - " + surfice.name);
			//console.log($input.val().replace(/^\s+|\s+$/gm,'').iequals(surfice.name));
			
			var val = $input.val().replace(/\s+/gm," ").trim();
			
			// If the name is blank, throw an error
			// Otherwise if the new name is the same as another
			// surfice and that I'm not checking its own name,
			// throw an error.
			if (	val == "" ||
					(	surficeId != surfice.id &&
						val.iequals(surfice.name)
					)
			) {
				$input.closest(".form-group").removeClass("has-success").addClass("has-error");
				return false;
			} else {
				$input.closest(".form-group").removeClass("has-error").addClass("has-success");
			}
		});
	}
}

function statusNameField($input) {
	
	var statusId = $input.closest("form").find('input[name="status"]').val();
	
	// If the surfs array already exists, just fire the function without getting all the info
	// If surfs is empty, however, get the new data
	if (ss.statuses.length == 0) {
		console.log("getting new surfices");
		ss.getStatuses(function(data) {
			checkField();
		});
		
	} else {
		checkField();
	}
	
	// Create a closure for checking the field to comply with DRY programming
	function checkField() {
		// Loop through all the surfs to find a match
		// not including this current surf
		$.each(ss.statuses, function(key, status) {
			//console.log($input.val().replace(/^\s+|\s+$/gm,'') + " - " + surfice.name);
			//console.log($input.val().replace(/^\s+|\s+$/gm,'').iequals(surfice.name));
			
			var val = $input.val().replace(/\s+/gm," ").trim();
			
			// If the name is blank, throw an error
			// Otherwise if the new name is the same as another
			// status and that I'm not checking its own name,
			// throw an error.
			if (	val == "" ||
					(	statusId != status.id &&
						val.iequals(status.name)
					)
			) {
				$input.closest(".form-group").removeClass("has-success").addClass("has-error");
				return false;
			} else {
				$input.closest(".form-group").removeClass("has-error").addClass("has-success");
			}
		});
	}
}

$('input[name="name"][data-ajax-check]').keyup(function(e) {
	$input = $(this);
	
	//var check = $.data($input.get(0), "ajax-check");
	var check = $(this).attr("data-ajax-check");
	
	if (typeof check === 'undefined') {
		// Nothing to do if check is undefined
	}
	else if (check == "surf-name")
		surfNameField($input);
	
	else if (check == "surfice-name")
		surficeNameField($input);
	
	else if (check == "status-name")
		statusNameField($input);
});

var textfield = $("input[name=username]");

$('button.login[type="submit"]').click(function(e) {
	//e.preventDefault();
	//little validation just to check username
	if (textfield.val() != "") {
		//$("body").scrollTo("#output");
		$("#output").addClass("alert alert-success animated fadeInUp").html("Welcome back " + "<span style='text-transform:uppercase'>" + textfield.val() + "</span>");
		$("#output").removeClass(' alert-danger');
		$("input").css({
			"height":"0",
			"padding":"0",
			"margin":"0",
			"opacity":"0"
		});
		//change button text 
		$('button[type="submit"]')//.html("continue")
			.removeClass("btn-info")
			.addClass("btn-default").click(function(){
				$("input").css({
					"height":"auto",
					"padding":"10px",
					"opacity":"1"
				}).val("");
			});
		
		//show avatar
		//$(".avatar").css({
		//	"background-image": "url('http://api.randomuser.me/0.3.2/portraits/women/35.jpg')"
		//});
	} else {
		//remove success mesage replaced with error message
		$("#output").removeClass(' alert alert-success');
		$("#output").addClass("alert alert-danger animated fadeInUp").html("sorry enter a username ");
	}
	//console.log(textfield.val());

});





});