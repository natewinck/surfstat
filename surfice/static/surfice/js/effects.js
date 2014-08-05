$(function() {


/* $().fadeSlide
------------------------------ 
*  If an element is hidden, this slides the element down and then fades in.
*  If an element is visible, this fades the element out and then slides up
*  
*  INPUT
*  speed		Speed of transitions
*  easing		jQuery easing options
*  callback		function called after transitions
*  
*  
------------------------------ */
jQuery.fn.fadeSlide = function(speed, easing, callback) {
  if (this.is(":hidden")) {
    return this.slideDown(speed, easing).fadeTo(speed, 1, easing, callback);
  } else {
    return this.fadeTo(speed, 0, easing).slideUp(speed, easing, callback);
  }
};

/* $().slideRow
------------------------------ 
*  Using options "up" or "down", this collapses an element up or down.
*  
*  INPUT
*  speed		Speed of transition
*  easing		jQuery easing options
*  callback		function called after transitions
*  
*  
------------------------------ */
(function($) {
var sR = {
    defaults: {
        slideSpeed: 400,
        easing: false,
        callback: false     
    },
    thisCallArgs: {
        slideSpeed: 400,
        easing: false,
        callback: false
    },
    methods: {
        up: function (arg1,arg2,arg3) {
            if(typeof arg1 == 'object') {
                for(p in arg1) {
                    sR.thisCallArgs.eval(p) = arg1[p];
                }
            }else if(typeof arg1 != 'undefined' && (typeof arg1 == 'number' || arg1 == 'slow' || arg1 == 'fast')) {
                sR.thisCallArgs.slideSpeed = arg1;
            }else{
                sR.thisCallArgs.slideSpeed = sR.defaults.slideSpeed;
            }

            if(typeof arg2 == 'string'){
                sR.thisCallArgs.easing = arg2;
            }else if(typeof arg2 == 'function'){
                sR.thisCallArgs.callback = arg2;
            }else if(typeof arg2 == 'undefined') {
                sR.thisCallArgs.easing = sR.defaults.easing;    
            }
            if(typeof arg3 == 'function') {
                sR.thisCallArgs.callback = arg3;
            }else if(typeof arg3 == 'undefined' && typeof arg2 != 'function'){
                sR.thisCallArgs.callback = sR.defaults.callback;    
            }
            var $cells = $(this).find('td');
            $cells.wrapInner('<div class="slideRowUp" />');
            var currentPadding = $cells.css('padding');
            $cellContentWrappers = $(this).find('.slideRowUp');
            $cellContentWrappers.slideUp(sR.thisCallArgs.slideSpeed,sR.thisCallArgs.easing).parent().animate({
                                                                                                                paddingTop: '0px',
                                                                                                                paddingBottom: '0px'},{
                                                                                                                complete: function () {
                                                                                                                    $(this).children('.slideRowUp').replaceWith($(this).children('.slideRowUp').contents());
                                                                                                                    $(this).parent().css({'display':'none'});
                                                                                                                    $(this).css({'padding': currentPadding});
                                                                                                                }});
            var wait = setInterval(function () {
                if($cellContentWrappers.is(':animated') === false) {
                    clearInterval(wait);
                    if(typeof sR.thisCallArgs.callback == 'function') {
                        sR.thisCallArgs.callback.call(this);
                    }
                }
            }, 100);                                                                                                    
            return $(this);
        },
        down: function (arg1,arg2,arg3) {
            if(typeof arg1 == 'object') {
                for(p in arg1) {
                    sR.thisCallArgs.eval(p) = arg1[p];
                }
            }else if(typeof arg1 != 'undefined' && (typeof arg1 == 'number' || arg1 == 'slow' || arg1 == 'fast')) {
                sR.thisCallArgs.slideSpeed = arg1;
            }else{
                sR.thisCallArgs.slideSpeed = sR.defaults.slideSpeed;
            }

            if(typeof arg2 == 'string'){
                sR.thisCallArgs.easing = arg2;
            }else if(typeof arg2 == 'function'){
                sR.thisCallArgs.callback = arg2;
            }else if(typeof arg2 == 'undefined') {
                sR.thisCallArgs.easing = sR.defaults.easing;    
            }
            if(typeof arg3 == 'function') {
                sR.thisCallArgs.callback = arg3;
            }else if(typeof arg3 == 'undefined' && typeof arg2 != 'function'){
                sR.thisCallArgs.callback = sR.defaults.callback;    
            }
            var $cells = $(this).find('td');
            $cells.wrapInner('<div class="slideRowDown" style="display:none;" />');
            $cellContentWrappers = $cells.find('.slideRowDown');
            $(this).show();
            $cellContentWrappers.slideDown(sR.thisCallArgs.slideSpeed, sR.thisCallArgs.easing, function() { $(this).replaceWith( $(this).contents()); });

            var wait = setInterval(function () {
                if($cellContentWrappers.is(':animated') === false) {
                    clearInterval(wait);
                    if(typeof sR.thisCallArgs.callback == 'function') {
                        sR.thisCallArgs.callback.call(this);
                    }
                }
            }, 100);
            return $(this);
        }
    }
};

$.fn.slideRow = function(method,arg1,arg2,arg3) {
    if(typeof method != 'undefined') {
        if(sR.methods[method]) {
            return sR.methods[method].apply(this, Array.prototype.slice.call(arguments,1));
        }
    }
};
})(jQuery);

// Prevent css animations from loading, then remove the preload class so they work
$(window).load(function() {
	// Remove the class from body that prevents animations onload
	$("body").removeClass("preload");
});
    
    
/* SMOOTH SCROLLING
------------------------------
*  Any time a link is clicked that goes to an #anchor,
*  scroll to it instead of jumping to it.
*  Also prevents a # from appearing in the URL
* 
*  INPUT
*  a[href^=#*]      Any <a> with an href that starts with # (but not only #)
*  
*  EVENT
*  click
------------------------------ */
///*
//$("a[href*=#]:not([href=#])").click(function(e) {
$("a[href^=#]:not([href=#])").click(function(e) {
	e.preventDefault();
    if (location.pathname.replace(/^\//,'') == this.pathname.replace(/^\//,'') && location.hostname == this.hostname) {
        var target = $(this.hash);
        target = target.length ? target : $('[name=' + this.hash.slice(1) +']');
        if (target.length) {
            $('html,body').stop().animate({
            scrollTop: target.offset().top
        }, 500);
        //console.log("You clicked a hashtag!");
        //window.location.hash = this.hash.slice(1);
        //return false;
        }
    }
});
//*/


/* CHARTS
------------------------------ 
*  Sets up all charts on a page with the .chart selector.
*  Data is grabbed from the chartData[] associative array
*  that corresponds with the canvas's data-id attribute.
*  
*  When the chart either comes in view or is unhidden,
*  the chart fades in after a short delay.
*  
*  INPUT
*  canvas.chart
*  chartData[]        Global variable defined before this section
*  
*  EVENT
*  inview
*  
------------------------------ */
// Set up each of the inview events.
$("canvas.chart").on("inview", function() {
    var $this = $(this);
    $this.removeClass("hidden").off("inview");
    setTimeout(function() {
        showLineChart($this)
    }, 250);
    //$this.fadeIn(1000);
    $this.animate({ opacity: 1 }, 1000);
});

// showLineChart($this)
//
// Shows the line chart based on its data-id
function showLineChart($this) {
    // Get the canvas context
    var ctx = $this[0].getContext("2d");
    
    // Get the chart data that corresponds to the data-id
    var data = chartData[$this.attr("data-id")];
    
    
    // If colors are not set for the datasets, give them default color schemes
    for (var d in data.datasets) {
        var dataset = data.datasets[d];
        switch(Number(d)) {
            // First dataset color scheme
            case 0:
                if (!dataset.fillColor) dataset.fillColor = "rgba(220,220,220,0.5)";
                if (!dataset.strokColor) dataset.strokeColor = "rgba(220,220,220,1)";
                if (!dataset.pointColor) dataset.pointColor = "rgba(220,220,220,1)";
                if (!dataset.pointStrokeColor) dataset.pointStrokeColor = "#fff";
                break;
                
            // Second dataset color scheme (layered on top of first)
            case 1:
                if (!dataset.fillColor) dataset.fillColor = "rgba(73,23,109,0.5)";
                if (!dataset.strokColor) dataset.strokeColor = "rgba(52,12,75,1)";
                if (!dataset.pointColor) dataset.pointColor = "rgba(52,12,75,1)";
                if (!dataset.pointStrokeColor) dataset.pointStrokeColor = "#fff";
                break;
            
            // Default dataset color scheme
            default:
                if (!dataset.fillColor) dataset.fillColor = "rgba(220,220,220,0.5)";
                if (!dataset.strokColor) dataset.strokeColor = "rgba(220,220,220,1)";
                if (!dataset.pointColor) dataset.pointColor = "rgba(220,220,220,1)";
                if (!dataset.pointStrokeColor) dataset.pointStrokeColor = "#fff";
        }     
    }
    
    // Options for the animated charts
    var options = {
        ///Boolean - Whether grid lines are shown across the chart
        scaleShowGridLines : false,

        //String - Scale label font declaration for the scale label
        scaleFontFamily : "'Helvetica Neue', 'Arial'",

        //Function - Fires when the animation is complete
        onAnimationComplete : null
    }
    
    // Draw the chart
    var chart = new Chart(ctx).Line(data, options);
}




/* TABBABLE TABS
------------------------------ 
*  Assigns a CLICK event to all .nav a elements that have a data-toggle attribute.
*  The elements that have a corresponding id to the <a> href will show or hide.
*  
*  Pseudo example: <a href="#surfice"></a> will show <div id="surfice"></div>
*  
*  INPUT
*  .nav a[data-toggle]          <a> elements that have a data-toggle attribute
* 
*  EVENT
*  click
*
------------------------------ */
$('.nav a[data-toggle]').click(function (e) {
    e.preventDefault()
    $(this).tab('show')
})


/* DROPDOWN SELECT
------------------------------ 
*  Takes a bootstrap group button selector and turns it into
*  the equivalent of <select>.  It will also change a hidden input
*  and change the value to the value defined on the li elements.
*  
*  Takes any group of bootstrap buttons with the .dropdown-select class.
*  It then takes the text of the selected li element and puts it in the
*  element with the data-bind='label' attribute.
*  Next, it toggles the select so the dropdown disappears
*  Finally the input[type='hidden'] element within the .dropdown-select element
*  receives li[value] attribute
*  
*  If the dropdown also has .autosubmit class, the form is submitted
*  
*  INPUT
* .dropdown-select .dropdown-menu li        The li elements in the group button options
*
------------------------------ */
$(".dropdown-select .dropdown-menu li").click(function(event) {
    var $target = $( event.currentTarget );
    var $group = $target.closest( '.dropdown-select' );
    dropdownSelect($target);
    // If the dropdown autosubmits the form, submit it now!
    if ($group.hasClass("autosubmit")) {
        $(this).parents("form").submit();
    }
    
    return false;
 
});

/* dropdownSelect($li)
-----------------------
*  The heart of the dropdown select functionality.
*  Selects a list element.
*
*  INPUT
*  $li		jQuery list object
----------------------- */
function dropdownSelect($li) {
	var $target = $li;
    var $group = $target.closest( '.dropdown-select' );
    $group
        .find( '[data-bind="label"]' ).text( $target.text() )
        .end()
        .children( '.dropdown-toggle' ).dropdown( 'toggle' );
    $group.find( 'input[type="hidden"]' ).val( $target.attr("value") )
}

/* LIST GROUP SELECT
------------------------------ 
*  Selects all list groups that the .select class and makes them a select.
*  Automatically finds the tabs associated with the href (by id)
*  and hides/shows them
*  
*  INPUT
*  .list-group.select .list-group-item       The list elements (links)
*
------------------------------ */
$(".list-group.select .list-group-item").click(function(e) {
	// Prevent a # from showing up in the URL
	e.preventDefault();
	
	selectTab( $(this) );
	
});

function selectTab($button, push) {
	push = typeof push !== 'undefined' ? push : true;
	if (!$button.hasClass("active") && $button.length > 0) {
		// Find the previous element that was selected and remove classes
		var old_id = $button.closest(".list-group.select").find(".list-group-item.active").removeClass("active").attr("href");
		
		// Find the element new element taht was clicked and add the active class to it
		var new_id = $button.addClass("active").attr("href");
		
		// Hide the old tab and show the new one
		$(old_id).removeClass("active in");
		$(new_id).addClass("active in");
		
		// Change hash for page-reload
		//window.location.hash = $button.prop("hash");
		if (push) {
			var data = {hash: new_id};
			//console.log("Pushing " + data.hash);
			history.pushState(data, "", $button.prop("hash"));
		}
	}
}

window.addEventListener("popstate", function(e) {
	//console.log(e.state.hash);
	
	// Javascript to enable link to tab
	// If there is a state, use its hash property set in selectTab
	if (e.state) {
		console.log("Popping " + e.state.hash);
		if (e.state.hash.match('#')) {
			//console.log("the hashtag: " + e.state.hash.split('#')[1]);
			selectTab( $('.list-group.select a[href=#'+e.state.hash.split('#')[1]+']'), false );
		} 
	}
	// If this event is the first time it's run, there won't be a state
	// so get the hash from the url
	else {
		var url = document.location.toString();
		//console.log("Getting from URL " + url);
		if (url.match('#')) {
			selectTab( $('.list-group.select a[href=#'+url.split('#')[1]+']'), false );
		} else {
			// If there is no hashtag, push a state with the current button selected
			// (assuming there is only one .list-group.select tag on the page
			selectTab( $(".list-group.select a.list-group-item.active").removeClass("active"), false );
			
			// Since this is the first time it's loaded, replace the state rather than push it
			var $button = $(".list-group.select a.list-group-item.active");
			var data = {hash: $button.attr("href")};
			//console.log("Replacing " + data.hash);
			// Don't add the hash to the url so that the page doesn't jump there onload
			history.replaceState(data, "");
		}
	}
	e.preventDefault();
	return false;
	
	/*var url = document.location.toString();
	if (url.match('#')) {
		selectTab( $('.list-group.select a[href=#'+url.split('#')[1]+']') );
	}
	*/
});

/* DYNAMIC COLOR
------------------------------
*  Adjust the color of the text based on 
*  the background color.
*  
*  INPUT
*  .dynamic-color
*
*  EVENT
*  onload
------------------------------ */
$(".dynamic-color").each(function() {
	// If the average is less than halfway to dark
	// change the color of the text to white
	$(this).css("color", getDynamicColor($(this).css("background-color")));
});

/* DELETE DIALOG MODALS
------------------------------ 
*  Replace informational and AJAX information in the
*  confirm delete dialog boxes when showing a dialog box.
*  This way, only one delete dialog box needs to be loaded
*  instead of one for every object.
*  
*  INPUT
*  #confirm-delete-event
*  #confirm-delete-ding
*  
*  EVENT
*  show.bs.modal		Bootstrap trigger for showing a modal dialog
*  
------------------------------ */
$("#confirm-delete-event").on("show.bs.modal", function(e) {
	// Get the delete button
	var $deleteButton = $(e.relatedTarget);
	
	// Get the event row that was clicked
	var $row = $(e.relatedTarget).closest("tr");
	
	// For convenience
	var $modal = $(this);
	
	// Replace the text in the delete dialog box
	$modal.find("[data-event-surfice]").text( $row.find('[data-name="surfice"]').text() );
	$modal.find('input[name="event"]').val( $deleteButton.attr("data-event-id") );
	
	
	// Get the update target, both old and new
	// First get all the selectors
	var selectors = ($modal.find("form").attr("data-ajax-update-target")) ? $modal.find("form").attr("data-ajax-update-target").split(' ') : [];
	
	// We're wanting to find the one that contains "delete-event-", so loop through
	// the selectors and find it
	var dataAjaxUpdateTarget = "";
	for (var key in selectors) {
		// If we find delete-event-, replace it with the word that contains the correct id
		if (selectors[key].contains("delete-event-")) {
			selectors[key] = "delete-event-" + $deleteButton.attr("data-event-id");
		}
		
		// Piece the string back together
		dataAjaxUpdateTarget += selectors[key] + " ";
	}
	// Delete the last (unnecessary) space
	dataAjaxUpdateTarget.slice(0, -1);
	
	// Now that we have the new attr, set the data-ajax-update-target attribute
	$modal.find("form").attr("data-ajax-update-target", dataAjaxUpdateTarget);
	
	
	// When clicking submit, hide the modal
	$modal.find('[type="submit"]').off().click(function() {
		// Hide the modal
		$modal.modal("hide");
		
		// Since submit was clicked, we don't need this event listener anymore
		$(this).off();
	});
});

$("#confirm-delete-ding").on("show.bs.modal", function(e) {
	var $deleteButton = $(e.relatedTarget);
	var $row = $(e.relatedTarget).closest("tr");
	var $modal = $(this);
	
	// Replace the text in the delete dialog box
	$modal.find("[data-ding-surfice]").text( $row.find('[data-name="surfice"]').text() );
	$modal.find('input[name="ding"]').val( $deleteButton.attr("data-ding-id") );
	
	
	// Get the update target, both old and new
	// First get all the selectors
	var selectors = ($modal.find("form").attr("data-ajax-update-target")) ? $modal.find("form").attr("data-ajax-update-target").split(' ') : [];
	
	// We're wanting to find the one that contains "delete-ding-", so loop through
	// the selectors and find it
	var dataAjaxUpdateTarget = "";
	for (var key in selectors) {
		// If we find delete-ding-, replace it with the word that contains the correct id
		if (selectors[key].contains("delete-ding-")) {
			selectors[key] = "delete-ding-" + $deleteButton.attr("data-ding-id");
		}
		
		// Piece the string back together
		dataAjaxUpdateTarget += selectors[key] + " ";
	}
	// Delete the last (unnecessary) space
	dataAjaxUpdateTarget.slice(0, -1);
	
	// Now that we have the new attr, set the data-ajax-update-target attribute
	$modal.find("form").attr("data-ajax-update-target", dataAjaxUpdateTarget);
	
	
	// When clicking submit, hide the modal
	$modal.find('[type="submit"]').off().click(function() {
		$modal.modal("hide");
		
		// Since it's been clicked
		$(this).off();
	});
});

$(".modal").on("show.bs.modal", onModalShow);
$(".modal").on("hide.bs.modal", onModalHide);
$(".modal").on("shown.bs.modal", onModalShown);

function onModalShow(e) {
	$modal = $(this);
	
	// Set up pressing enter
	$modal.on("keydown", function(e) {
		// If the user presses enter, and the user isn't entering tags
		// and the user is not in a textarea, submit the form
		if	(
				e.which == 13 &&
				$(e.target).parent(".bootstrap-tagsinput").length == 0 &&
				!$(e.target).is("textarea")
			)
		{
			e.preventDefault();
			$modal.find('[type="submit"]').trigger("click");
		}
	});
	//console.log("show");
}

function onModalHide(e) {
	$modal = $(this);
	$modal.off("keydown");
}

function onModalShown(e) {
	$modal = $(this);
	
	
	$focusElement = $modal.find(".focus").first();
	
	// If no element is specified as the to focus first,
	// find the first visible input and focus it
	if ($focusElement.length == 0)
		$focusElement = $modal
			.find("input, select, textarea")
			.filter(function(index) {
				return ($(this).css("display") != "none");
			})
			.first();
	
	$focusElement.focus();
}

/* MULTISELECT
------------------------------ 
*  Replace all <select>s in the HTML with a prettier
*  and more user-friendly version.  Multiselect has
*  numerous options and can be found at
*  http://davidstutz.github.io/bootstrap-multiselect/
*  
*  INPUT
*  .multiselect-surfs
*  .multiselect-surfices
*  .multiselect
*  
*  EVENT
*  onload
*  
------------------------------ */
$(".multiselect").multiselect();

$(".multiselect-surfs").multiselect({
	buttonContainer: '<br><div class="btn-group" />',
	enableFiltering: true,
	enableCaseInsensitiveFiltering: true,
	onChange: function($element, checked) {
		// Get how many elements are selected
		var length = 0;
		
		// If there are more than 0 in the select, set the length
		if ( this.$select.val() != null )
			length = this.$select.val().length;
		
		// If the user deselected an option and now the length is zero,
		// create the hidden input
		var $input = $('<input id="hiddenNoneSurf" type="hidden" name="surf" value="-1">');
		if (!checked && length == 0) {
			this.$select.closest("form").append($input);
		}
		
		// If the user checked an option and now the length is one
		// (meaning that it was just empty), delete the hidden input
		else if (checked && length == 1) {
			$("#hiddenNoneSurf").remove();
		}
	}
});

$(".multiselect-surfices").multiselect({
	buttonContainer: '<div class="btn-group btn-group-justified" />',
	// Bootstrap buttons need to be wrapped in another div
	// That option is not given however...
	//buttonClass: "btn btn-block btn-default",
	buttonWidth: "100%",
	enableFiltering: true,
	enableCaseInsensitiveFiltering: true,
	includeSelectAllOption: true
});

/* AUTOSIZE
------------------------------ 
*  Makes any textarea with the autosize class resize
*  when text is inputted.
*  
*  INPUT
*  textarea.autosize
*  
*  EVENT
*  focus
*  
------------------------------ */
$("textarea.autosize").on('focus', function() {
	$(this).autosize();
});

/* ROW LINK
------------------------------ 
*  Makes any row with a data-href attribute also a link
*  Changes the cursor automatically to a pointer
*  Won't fire when clicking on an <a>
*  
*  INPUT
*  tr[data-href]
*  
*  EVENT
*  focus
*  
------------------------------ */
$("table").on('click', 'tr[data-href]', function(e) {
	//console.log(e);
	if ($(this).attr("data-href") != "") {
		//console.log("href");
		window.location = $(this).attr("data-href");
	}
});

$("table").on("click", 'tr[data-href] a[data-toggle="modal"]', function(e) {
	// Create a custom modal show trigger for table row elements that have data-href
	$($(this).attr("data-target")).modal('show');
	return false;
});


/* SURFICE CLICK
------------------------------ 
*  Makes all the surfices able to be clicked even when 
*  clicking on the div rather than the <a>
*  
*  INPUT
*  .surfices div.surfice
*  
*  EVENT
*  click
*  
------------------------------ */
$(".surfices > div.surfice").click(function() {
	//console.log('click');
	//console.log(this);
	$( $(this).find("a").attr("data-target") ).modal("show");
});

});

/* AJAX PROCESSES DISPLAY
-------------------------------
*  Pulse buttons, replace text, and perform other display functions
*  to signal to the user that processing is either happening
*  or has happened and was successful or unsuccessful
*
*  INPUT
*  $form		jQuery form object that submitted the ajax request
*
------------------------------- */
function ajaxProcessingDisplay($form) {
	var $button = $form.find('[type="submit"]');
	
    // Disable the button and add a flash animation (in css)
    $button.addClass("disabled");
	$button.addClass("flash");
	
	// Get the button text so we can replace it later
	$button.attr("data-value-original", $button.text());
	if ($button.attr("data-value-processing")) {
		$button.text($button.attr("data-value-processing"));
	} else {
		$button.text("Saving...");
	}
}

function ajaxSuccessDisplay($form) {
	// If the form was inside a modal, hide the modal
	$form.closest(".modal").modal("hide");
	
	var $button = $form.find('[type="submit"]');
	
	if ($button.attr("data-value-success")) {
		$button.text($button.attr("data-value-success"));
	} else {
		$button.text("Saved");
	}
	
	// Show a notification about the POST
	var notification = $form.attr("data-ajax-success");
	if (notification == "" || typeof notification === "undefined") notification = "Save successful."
	ss.notify("success", notification);
	
	// Stop the pulsing
	$button.removeClass("flash");
	
	// Pause for a moment, then re-enable the submit button
	setTimeout(function() {
		$button.removeClass("disabled");
		$button.text($button.attr("data-value-original"));
	}, 750);
}

function ajaxFailDisplay($form) {
	var $button = $form.find('[type="submit"]');
	
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
		$button.text($button.attr("data-value-original"));
	}, 750);
}