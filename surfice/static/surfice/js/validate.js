/* VALIDATION
------------------------------ 
*  Validate forms before submitting for the purpose of
*  preventing form submission.
*  
*  INPUT
*  input[name="name"][data-ajax-check]
*  
*  KEYUP VALIDATORS
*  surf-name
*  surfice-name
*  status-name
* 
*  EVENT
*  keyup
*
------------------------------ */

/* SET UP THE LISTENERS */
$('input[name="name"][data-ajax-check]').each(function() {
	$input = $(this);
	
	//var check = $.data($input.get(0), "ajax-check");
	var check = $(this).attr("data-ajax-check");
	if (typeof check === 'undefined') {
		// Nothing to do if check is undefined
	}
	else if (check == "surf-name")
		$input.keyup(function(){ surfNameField( $(this) ) });
	
	else if (check == "surfice-name")
		$input.keyup(function(){ surficeNameField( $(this) ) });
	
	else if (check == "status-name")
		$input.keyup(function(){ statusNameField( $(this) ) });
});

$('input[name="email"][data-ajax-check]').each(function() {
	$input = $(this);
	
	$input.keyup(function() {
		if (!isValidEmail( $(this).val() )) {
			$(this).closest(".form-group").removeClass("has-success").addClass("has-error");
		} else {
			$(this).closest(".form-group").removeClass("has-error").addClass("has-success");
		}
		
	});
	
});

/* CHECK SURF NAME FIELDS */
function surfNameField($input) {
	// Get the id of this object so that we don't check the name against itself
	var surfId = $input.closest("form").find('input[name="surf"]').val();
	
	// If the surfs array already exists, just fire the function without getting all the info
	// If surfs is empty, however, get the new data
	if (Object.size(ss.surfs) == 0) {
		console.log("getting new surfs");
		ss.getSurfs(function(data) {
			checkNameField($input, ss.surfs, surfId);
		});
		
	} else {
		checkNameField($input, ss.surfs, surfId);
	}
	
}

/* CHECK SURFICE NAME FIELDS */
function surficeNameField($input) {
	// Get the id of this object so that we don't check the name against itself
	var surficeId = $input.closest("form").find('input[name="surfice"]').val();
	
	// If the surfs array already exists, just fire the function without getting all the info
	// If surfs is empty, however, get the new data
	if (Object.size(ss.surfices) == 0) {
		console.log("getting new surfices");
		ss.getSurfices(function(data) {
			checkNameField($input, ss.surfices, surficeId);
		});
		
	} else {
		checkNameField($input, ss.surfices, surficeId);
	}
}

/* CHECK STATUS NAME FIELDS */
function statusNameField($input) {
	// Get the id of this object so that we don't check the name against itself
	var statusId = $input.closest("form").find('input[name="status"]').val();
	
	// If the surfs array already exists, just fire the function without getting all the info
	// If surfs is empty, however, get the new data
	if (Object.size(ss.statuses) == 0) {
		console.log("getting new surfices");
		ss.getStatuses(function(data) {
			checkNameField($input, ss.statuses, statusId);
		});
		
	} else {
		checkNameField($input, ss.statuses, statusId);
	}
}

/* THE ACTUAL NAME CHECKER */
function checkNameField($input, data, id) {
	
	// Strip all extra whitespace from the field
	var val = $input.val().replace(/\s+/gm," ").trim();
	
	// Loop through all the surfs to find a match
	// not including this current surf
	$.each(data, function(key, obj) {
		
		// If the name is blank, throw an error
		// Otherwise if the new name is the same as another
		// surf and that I'm not checking its own name,
		// throw an error.
		if (	val == "" ||
				(	id != obj.id &&
					val.iequals(obj.name)
				)
		) {
			$input.closest(".form-group").removeClass("has-success").addClass("has-error");
			return false;
		} else {
			$input.closest(".form-group").removeClass("has-error").addClass("has-success");
		}
	});
}

function validate(form) {
	// If there are errors in the form, return false
	// Otherwise, return true
	return ($(form).find(".has-error").length > 0) ? false : true;
}

function isValidEmail(emailAddress) {
    var pattern = new RegExp(/^((([a-z]|\d|[!#\$%&'\*\+\-\/=\?\^_`{\|}~]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])+(\.([a-z]|\d|[!#\$%&'\*\+\-\/=\?\^_`{\|}~]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])+)*)|((\x22)((((\x20|\x09)*(\x0d\x0a))?(\x20|\x09)+)?(([\x01-\x08\x0b\x0c\x0e-\x1f\x7f]|\x21|[\x23-\x5b]|[\x5d-\x7e]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(\\([\x01-\x09\x0b\x0c\x0d-\x7f]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]))))*(((\x20|\x09)*(\x0d\x0a))?(\x20|\x09)+)?(\x22)))@((([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.)+(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.?$/i);
    return pattern.test(emailAddress);
};