$(function() {


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
    $.post(this.action,
    	// Get the data and serialize it
    	function() {
    		// name = data
    		// Attribute data-name=x
    		//$(this).children(a
    		formData = $(this).serializeArray();
    		
    		data = {};
    		$(this).children('[name="data"]').each(function() {
    			data[$(this).attr("data-name")] = $(this).val()
    		});
    		
    		// If there were data fields found
    		if (!jQuery.isEmptyObject(data)) {
    			formData.push({name: "data", value: data});
    		}
    		
    		return formData
    		
    	},
    	// Get the response from the server
    	function(data, textStatus, jqXHR) {
    		// use data, which will be all JSON
    	}
    
    );
});

$("form").on("submit", function(e) {
	data = {};
	$(this).children('[name="data"]').each(function() {
		data[$(this).attr("data-name")] = $(this).val()
	});
	
	// If there were data fields found
	if (!jQuery.isEmptyObject(data)) {
		formData.push({name: "data", value: data});
	}
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
	$(this).parents(".modal").find("form").submit();
});




});