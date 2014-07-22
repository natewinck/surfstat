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
	console.log(this);
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

function surfNameField($input) {
	var surfId = $input.closest("form").find('input[name="surf"]').val();
	
	// If the surfs array already exists, just fire the function without getting all the info
	// If surfs is empty, however, get the new data
	if (Object.size(ss.surfs) == 0) {
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
		var val = $input.val().replace(/\s+/gm," ").trim();
		console.log(val);
		$.each(ss.surfs, function(key, surf) {
			//console.log($input.val().replace(/^\s+|\s+$/gm,'') + " - " + surf.name);
			//console.log($input.val().replace(/^\s+|\s+$/gm,'').iequals(surf.name));
			
			console.log(surfId);
			console.log(surf.id);
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
	if (Object.size(ss.surfices) == 0) {
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
	if (Object.size(ss.statuses) == 0) {
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