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
		}
		
		// For radio buttons, make sure only the checked one of a specific
		// name/id is stored
		else if ($(this).prop("type") == "radio") {
			// Check to see if this is the checked radio or not. If it's not,
			// don't store it.
			if ( $(this).prop("checked") ) {
				data[$(this).attr("data-name")] = $(this).val();
			}
		}
		
		// If nothing special needs to happen, add it to the associative array
		else {
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
		
		// Delete any existing input in this form with name=data
		$(this).find("[name=data]").remove();
		
		// Append the input into the form
		$(this).append(input);
	}
	
	if (!validate(this)) {
		e.preventDefault();
		return false;
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
$("body").on("submit", "form[type='ajax']", function(e) {
    // Prevent the form from submitting
    e.preventDefault();
    
    // For convenience...
    var $form = $(this);
    
    // Give some feedback to the user when submitting the ajax request
    ajaxProcessingDisplay($form);
    
    // Serialize all the data in the form so that it can be passed
    var data = $(this).serialize();
    
    $.post(this.action, data,
    	// Get the response from the server
    	function(data, textStatus, jqXHR) {
    		
    		// Display success to the page's form
    		ajaxSuccessDisplay($form);
			
			// Since something was updated, refresh the AJAX fields on the page
			refreshAJAXPage($form);
    	})
		.done(function() {
			// Nothing here (same as above)
		})
		.fail(function(test) {
			
			// Display to the user that the ajax operation failed
			ajaxFailDisplay($form)
			
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
	var $modal = $(this).closest(".modal");
	$modal.find("form").submit();
});



});