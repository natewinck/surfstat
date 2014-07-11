/* Refresh AJAX Page
------------------------------
*  Whenever an AJAX form is submitted, this function is
*  fired with the jQuery form that submitted the request
*  along with the data that $.getJSON returns.
*  
*  This method functions as a handler for other functions to
*  update the related elements.  Elements are related by their
*  data-ajax-update attributes; these hook into the listener.  The form targets each of these
*  elements with space delimited selectors in its
*  data-ajax-update-target attribute.  This function will then
*  find all the elements with that data-ajax-update attribute.
*  
*  Note that an element can only have one data-ajax-update attribute!
* 
*  INPUT
*  $form			The jQuery form that submitted the AJAX request
***  data				The JSON data returned from the $.getJSON request **
*  
------------------------------ */
function refreshAJAXPage($form) {
	
	// Get the getData
	var getData = ($form.attr("data-ajax-get")) ? $.parseJSON($form.attr("data-ajax-get")) : "";
	
	// Clear the fields labeled to be cleared
	$form.find("input[data-ajax-clear], textarea[data-ajax-clear]").val("").text("");
	$form.find("select[data-ajax-clear]").prop("selectedIndex", 0);
	
	// Get new data from the database and then once it gets it
	// refresh the page with the new data
	// TO DO: Stop using the data passed to this function and start using ss
	ss.get($form.attr("data-ajax-action"), getData, function(data) {
		console.log(data);
		
		// Get the selectors and split them into an array
		var selectors = $form.attr("data-ajax-update-target").split(' ');
		
		// Now loop through the selectors and fire a separate methods for each one
		$.each(selectors, function(key, selector) {
			
			refreshAJAXPageHandler(selector, data);
			
		});
	});
	
}

/* -----------------------------------------
*  refreshSurfName($elements, data)
*
*  Refreshes all the name/value fields of the page within
*  the matched elements
*
*  INPUT
*  $elements		jQuery array of matched elements
*  data				Data containing the description attribute
*
*  ----------------------------------------- */
function refreshSurfName($elements, data) {
	// First change the form element's success notify text
	// for future notifications
	//$form.attr("data-ajax-success", data.name + "'s name and description were successfully updated.");
	//$form.attr("data-ajax-fail", data.name + "'s name and description were unable to be updated.");
	
	// Loop through these elements
	$elements.each(function() {
		$element = $(this);
		
		// If the element is a tab, update its id so that it matches the
		// previously mentioned #href
		if ($element.hasClass("tab-pane"))
			$element.attr("id", "surf-" + data.name.slugify());
		
		else {
			// First change the contents of the element to the name
			$element.text(data.name).val(data.name);

			// If a list-group-item is updated, don't forget to add the right-arrow
			if ($element.hasClass("list-group-item"))
				$element.append("<span class=\"glyphicon glyphicon-chevron-right pull-right\"></span>");

			// If an anchor is updated, don't forget to update it's #href
			if ($element.is("a"))
				//console.log(data.name);
				$element.attr("href", "#surf-" + data.name.slugify());
			}
	});
}

/* -----------------------------------------
*  refreshDescription($elements, data)
*
*  Refreshes all the description fields of the page within
*  the matched elements
*
*  INPUT
*  $elements		jQuery array of matched elements
*  data				Data containing a description attribute
*
*  ----------------------------------------- */
function refreshDescription($elements, data) {

	$elements.each(function() {
		$element = $(this);
	
		// Change the text value to the description
		$element.text(data.description);
	
	});
	
}

/* -----------------------------------------
*  refreshSurfsSurfices($elements, data)
*
*  Refreshes all the description fields of the page within
*  the matched elements with the passed data
*
*  INPUT
*  $elements		jQuery array of matched elements
*  data				Array of surfs with deep data including surfices
*
*  ----------------------------------------- */
function refreshSurfsSurfices($elements, data) {
			
	// Create a copy of the data variable so that we can splice it as we go through
	// When we display a surfice, it should be removed from the data
	// so we don't need to loop over it anymore.
	var tempData = data.slice(0);

	$elements.each(function() {
		$element = $(this);
	
		// Empty the table first
		$element.html("");

		// Set the empty variable so we know if this table ends up empty or not
		var empty = true;
		var surfId = $element.attr("data-ajax-id");
	
		// Search through the array to find the surf.id that matches surfId
		for (var i in tempData) 
			// If we have found the surf that matches the id in the html
			// add its surfices to the table
			if ("surf-" + tempData[i].id == surfId) {
				// Loop through this surf's surfices and put them in the table
				$.each(tempData[i].surfices, function(key, surfice) {
					// If there's a match for this piece of data, add it to the table
					addSurficeRowToSurf($element, surfice);
					
					// We added a row so the table isn't empty
					empty = false;
				});
			
				// We've used this surf so delete it from the array
				tempData.splice(i, 1);
			
				// We found the surf that relates to this id
				// so break out of the search loop
				break;
	
			}
	
		// If nothing is left in surfices, fill the table with only an empty row
		if (empty) {
			var $row = $("<tr><td>No Surfices in here</td></tr>");
			$element.append($row);
		}

	});

}

/* -----------------------------------------
*  refreshSurficesSelect($elements, data)
*
*  Update the matched selectors to reflect
*  addition or removal of surfices from surfs
*
*  INPUT
*  $elements		jQuery array of matched elements
*  data				Array of surfs with deep data including surfices
*
*  ----------------------------------------- */
function refreshSurficesSelect($elements, data) {
				
	$elements.each(function() {
		$element = $(this);
	
		var surfId = $element.attr("data-ajax-id");

		//{% for surfice in surfices %}
		//	{% if surfice not in surf.surfices %}
		//	<option value="{{ surfice.id }}">{{ surfice.name }}</option>
		//	{% endif %}
		//{% endfor %}
		$element.html("");

		// For every surfice in data...
		// Loop through the surfs
		$.each(data, function(key, surf) {
		
			// Only show surfices that are in other surfs
			// So exclude the current surf
			if ("surf-" + surf.id != surfId) {
				// Loop through this surf's surfices and add them to the <select>
				$.each(surf.surfices, function(key, surfice) {
					var $option = $("<option value=\"" + surfice.id + "\">" + surfice.name + "</option>");
					$element.append($option);
				});
			}
		
		});
	
	});
}

/* -----------------------------------------
*  refreshSurfDelete($elements, data)
*
*  Update the delete dialog box for each surf ($elements)
*
*  INPUT
*  $elements		jQuery array of matched elements
*  data				Array of surfs with deep data including surfices
*
*  ----------------------------------------- */
function refreshSurfDelete($elements, data) {
	
	// To make naming easier, rename data to surfs
	var surfs = data;

	$elements.each(function() {
		$element = $(this);
	
		var surfId = $element.attr("data-ajax-id");
		$element.html("");
	
		/* Django code
		{% if surf.surfices|length_is:"0" %}
		<p>There aren't any surfices in <span data-ajax-update="surf-name-{{ surf.id }}">{{ surf.name }}</span>, so it will be deleted and nothing else will happen.</p>
		<input name="is_empty" type="hidden">
		{% else %}

		<p>All surfices included in this surf will be pushed to another surf.</p>
		<div class="form-group">
			<label class="col-sm-4 control-label" for="new_surf">Reassign Surfices to...</label>
			<div class="col-sm-6">
				<select name="new_surf" class="form-control">
					<option disabled selected>Select a surf...</option>
					{% for new_surf in surfs %}
						{% if new_surf != surf %}
						<option value="{{ new_surf.id }}">{{ new_surf.name }}</option>
						{% endif %}
					{% endfor %}
				</select>
			</div>
		</div>
		{% endif %}
		*/
	
		// Find the surf that corresponds to this delete dialog box
		$.each(surfs, function(key, surf) {
			if ("surf-" + surf.id == surfId) {
			
				// If there aren't any surfices in this surf, allow the user to delete it
				// without reassigning surfices
				if (surf.surfices.length == 0) {
					$element.append("<p>There aren't any surfices in <span data-ajax-update=\"surf-name-" + surf.id + "\">" + surf.name + "</span>, so it will be deleted and nothing else will happen.</p>"
								 + "<input name=\"is_empty\" type=\"hidden\">");
				}
			
				// If there are surfices in this surf, display the content needed
				// to re-assign surfices
				else {
					$div = $("<p>All surfices included in this surf will be pushed to another surf.</p>" +
							"<div class=\"form-group\">" +
								"<label class=\"col-sm-4 control-label\" for=\"new_surf\">Reassign Surfices to...</label>" +
								"<div class=\"col-sm-6\">" +
									"<select name=\"new_surf\" class=\"form-control\">" +
										"<option disabled selected>Select a surf...</option>" +
										// We'll insert the other options here //
									"</select>" +
								"</div>" +
							"</div>");
				
					$select = $div.find("select");
				
					$.each(surfs, function(key, new_surf) {
						if (new_surf.id != surf.id) {
							$select.append("<option value=\"" + new_surf.id + "\" data-ajax-update=\"surf-name-" + new_surf.id + "\">" + new_surf.name + "</option>");
						}
					});
				
					$element.append($div);
				}
			
			}
		});
	
	});
}

/* -----------------------------------------
*  refreshSurfSurfices($elements, data)
*
*  Update this surf's surfices table (usually because the status was updated)
*
*  INPUT
*  $elements		jQuery array of matched elements
*  data				Array of surfices
*
*  ----------------------------------------- */
function refreshSurfSurfices($elements, data) {
	
	// Only replace the rows in the table if there
	// are surfices in the surf
	if (data.length > 0) {
		
		// Loop through the tables to be updated
		$elements.each(function() {
			$element = $(this);
		
			// Empty the table
			$element.html("");
		
			// Loop through the surfices we just got and add them to the table
			$.each(data, function(key, surfice) {
				addSurficeRowToSurf($element, surfice);
			});
		});
	}
}

/* -----------------------------------------
*  refreshSurficeName($elements, data)
*
*  Update all the surfice names
*
*  INPUT
*  $elements		jQuery array of matched elements
*  data				data that has a name attribute
*
*  ----------------------------------------- */
function refreshSurficeName($elements, data) {
	// First change the form element's success notify text
	// for future notifications
	//$form.attr("data-ajax-success", data.name + "'s name and description were successfully updated.");
	//$form.attr("data-ajax-fail", data.name + "'s name and description were unable to be updated.");
	
	// Loop through these elements
	$elements.each(function() {
		$element = $(this);
		
		// If the element is a tab, update its id so that it matches the
		// #href mentioned below
		if ($element.hasClass("tab-pane"))
			$element.attr("id", "surfice-" + data.name.slugify());
		
		else {
			// First change the contents of the element to the name
			$element.text(data.name).val(data.name);

			// If a list-group-item is updated, don't forget to add the right-arrow
			if ($element.hasClass("list-group-item"))
				$element.append("<span class=\"glyphicon glyphicon-chevron-right pull-right\"></span>");

			// If an anchor is updated, don't forget to update its #href
			if ($element.is("a"))
				$element.attr("href", "#surfice-" + data.name.slugify());
		}
		
	});
}

/* -----------------------------------------
*  refreshSurficeSurf($elements, data)
*
*  Update all of this surfice's names
*
*  INPUT
*  $elements		jQuery array of matched elements
*  data				data that has a surf object with a name attribute
*
*  ----------------------------------------- */
function refreshSurficeSurf($elements, data) {
	
	// Loop through the elements and change the surf name in each one
	$elements.each(function() {
		$element = $(this);
		
		// Change the contents of the element to the name of the surfice's surf
		$element.text(data.surf.name).val(data.surf.name);
		
	});
}

/* -----------------------------------------
*  refreshSurficeStatus($elements, data)
*
*  Update all the surfice names
*
*  INPUT
*  $elements		jQuery array of matched elements
*  data				data that has a status object with a name attribute
*
*  ----------------------------------------- */
function refreshSurficeStatus($elements, data) {
	
	// Loop through the elements and change the surfice status in each one
	$elements.each(function() {
		$element = $(this);
		
		// Change the contents of the element to the name of the surfice's surf
		$element.text(data.status.name).val(data.status.name);
		
	});
}

/* -----------------------------------------
*  refreshStatusName($elements, data)
*
*  Update all the status names
*
*  INPUT
*  $elements		jQuery array of matched elements
*  data				data that has a name attribute
*
*  ----------------------------------------- */
function refreshStatusName($elements, data) {
	
	// Loop through these elements
	$elements.each(function() {
		$element = $(this);
		
		// If the element is a tab, update its id so that it matches the
		// #href mentioned below
		if ($element.hasClass("tab-pane"))
			$element.attr("id", "status-" + data.name.slugify());
		
		else {
			// First change the contents of the element to the name
			$element.text(data.name).val(data.name);

			// If a list-group-item is updated, don't forget to add the right-arrow
			if ($element.hasClass("list-group-item"))
				$element.append("<span class=\"glyphicon glyphicon-chevron-right pull-right\"></span>");

			// If an anchor is updated, don't forget to update its #href
			if ($element.is("a"))
				$element.attr("href", "#status-" + data.name.slugify());
		}
		
	});
}

/* -----------------------------------------
*  refreshStatusColor($elements, data)
*
*  Update all color fields of a status
*
*  INPUT
*  $elements		jQuery array of matched elements
*  data				data that has a data.color attribute (data.data.color)
*
*  ----------------------------------------- */
function refreshStatusColor($elements, data) {
	
	// Loop through the elements and change the surf name in each one
	$elements.each(function() {
		$element = $(this);
		
		// Change the contents of the element to the name of the surfice's surf
		$element.text(data.data.color).val(data.data.color);
		
	});
}

/* -----------------------------------------
*  refreshAJAXPageHandler($elements, data, $form=null)
*
*  This function acts as a dispatcher to fire the correct
*  functions based on the selector.
*  
*  Takes a selector string and finds any data-ajax-update
*  html attributes that contains the word contained in the
*  selector string.
*  
*  The data can be any data, but is usually an array.
*  $form is only passed to those functions that need it.
*
*  All selectors are cached in the global ss variable.
*  If elements are added to the DOM with AJAX, they need
*  to be added to this cache.
*
*  INPUT
*  $elements		jQuery array of matched elements
*  data				data that has a name attribute
*  $form (optional) The form that requested the refresh
*
*  ----------------------------------------- */
function refreshAJAXPageHandler(selector, data) {
	// First get the element(s) that contain this whole selector
	//$elements = $("[data-ajax-update=\"" + selector + "\"]");
	
	// If the elements that match this selector haven't been cached in ss
	// go ahead and cache them now
	if (!ss.ajax.$elements[selector])
		ss.ajax.$elements[selector] = $("[data-ajax-update~=\"" + selector + "\"]");
	
	// Pull the matching elements from the cache
	$elements = ss.ajax.$elements[selector];

	// If there are no elements to match, continue onto the next loop
	if (!$elements.length) return;
	
	// If surf-name is set, change the contents of the
	// element to the data.name variable
	if (selector.contains("surf-name"))
		refreshSurfName($elements, data);
	
	// Change the contents to description
	else if (selector.contains("surf-description") || selector.contains("surfice-description") || selector.contains("status-description"))
		refreshDescription($elements, data);
	
	// Change the contents of ALL the surfices tables
	else if (selector.contains("surfs-surfices"))
		refreshSurfsSurfices($elements, data);
	
	// Update the selectors to reflect addition or removal of surfices from surfs
	else if (selector.contains("surfices-select"))
		refreshSurficesSelect($elements, data);
	
	// Update every delete dialog box for surfs
	else if (selector.contains("surf-delete"))
		refreshSurfDelete($elements, data);
	
	// Update this surf's surfices (usually because the status was updated)
	else if (selector.contains("surf-surfices"))
		refreshSurfSurfices($elements, data);
	
	// Update all the surfice names
	else if (selector.contains("surfice-name"))
		refreshSurficeName($elements, data);
	
	// Update this surfice's surf on the page
	else if (selector.contains("surfice-surf"))
		refreshSurficeSurf($elements, data);
	
	// Update this surfice's status on the page
	else if (selector.contains("surfice-status"))
		refreshSurficeStatus($elements, data);
	
	// Update the status name on the page
	else if (selector.contains("status-name"))
		refreshStatusName($elements, data);
	
	// Update the status color on the page
	else if (selector.contains("status-color"))
		refreshStatusColor($elements, data);
	
	// No error if a selector isn't matched
	
	// function loop($elements, fn) {
// 		$.each($elements, function() {
// 			fn($(this));
// 		}
// 	}
}

/* -----------------------------------------
*  addSurficeRowToSurf($table, surfice)
*
*  Append a surfice row to a table.
*
*  INPUT
*  $table		The table to append to
*  surfice		The surfice to be added to the table
*
*  ----------------------------------------- */
function addSurficeRowToSurf($table, surfice) {
	var $row = $("<tr class=\"dynamic-color\" style=\"background-color:" + surfice.status.data.color +"; color: " + getDynamicColor(surfice.status.data.color) + ";\">");
	$row.append("<td>" + surfice.name + "</td>");
	$row.append("<td>" + surfice.status.name + "</td>");

	// Now add the created row to the table
	$table.append($row);
}