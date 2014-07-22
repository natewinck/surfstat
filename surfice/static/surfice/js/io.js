$(function() {

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
			
			// Show a notification about the POST
			var notification = $form.attr("data-ajax-success");
			if (notification == "" || typeof notification === "undefined") notification = "Save successful."
			ss.notify("success", notification);
			
			// Since something was updated, refresh the AJAX fields on the page
			refreshAJAXPage($form);
			
			// Stop the pulsing
			$button.removeClass("flash");
			
			// Pause for a moment, then re-enable the submit button
			setTimeout(function() {
				$button.removeClass("disabled");
				$button.text($buttonText);
			}, 750);
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
			
			// Get the fail notification
			var notification = $form.attr("data-ajax-fail");
			
			// Show the notification
			if (notification == "" || typeof notification === "undefined") notification = "Save failed."
			ss.notify("danger", notification);
			
			// Pause for a moment, then re-enable the submit button
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
	var $modal = $(this).parents(".modal");
	$modal.find("form").submit();
	$modal.modal("hide");
});

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