/* Contains
------------------------------
*  Create a contains function for String objects
*
*  RETURNS
*  true if found
*  false if not found
*  
------------------------------ */
if (typeof String.prototype.contains === 'undefined') String.prototype.contains = function(it) { return this.indexOf(it) != -1; };

/* Slugify
------------------------------
*  Create a slugified version of a String.
*
*  Example: "A cool Surf" turns into "a-cool-surf"
*
*  RETURNS
*  The modified string
*  
------------------------------ */
if (typeof String.prototype.slugify === 'undefined') String.prototype.slugify = function() { return this.toLowerCase().replace(/ /g,'-').replace(/[^\w-]+/g,''); };

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
*  data				The JSON data returned from the $.getJSON request
*  
------------------------------ */
function refreshAJAXPage($form, data) {
	
	// Get the selectors and split them into an array
	var selectors = $form.attr("data-ajax-update-target").split(' ');
	
	// Now loop through the selectors and fire a separate methods for each one
	$.each(selectors, function(key, selector) {
		
		// First get the element(s) that match this selector
		$elements = $("[data-ajax-update=\"" + selector + "\"]");
		
		// If there are no elements to match, continue onto the next loop
		if (!$elements.length) return;
		
		// If surf-name is set, change the contents of the
		// element to the data.name variable
		if (selector.contains("surf-name")) {
			
			// Loop through these elements
			$elements.each(function() {
				$element = $(this);
				
				// First change the contents of the element to the name
				$element.text(data.name);
			
				// If a list-group-item is updated, don't forget to add the right-arrow
				if ($element.hasClass("list-group-item"))
					$element.append("<span class=\"glyphicon glyphicon-chevron-right pull-right\"></span>");
			
				// If an anchor is updated, don't forget to update it's #href
				if ($element.is("a"))
					$element.attr("href", "#surf-" + data.name.slugify());
			
				// If the form is in a tab, update its id so that it matches the
				// previously mentioned #href
				$form.closest(".tab-pane").attr("id", "surf-" + data.name.slugify());
				
			});
		}
		
		// Change the contents to description
		else if (selector.contains("surf-description")) {
			
			$elements.each(function() {
				$element = $(this);
				
				// Change the text value to the description
				$element.text(data.description);
				
			});
		}
		
		// Change the contents of ALL the surfices tables
		else if (selector.contains("surf-surfices")) {
			
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
				
				// Go backwards through the array so we can remove array
				// elements after we display them
				for (var i = tempData.length-1; i >= 0; i--) 
					if ("surf-" + tempData[i].surf.id == surfId) {
						// If there's a match for this piece of data, add it to the table
						var surfice = tempData[i];
						var $row = $("<tr class=\"dynamic-color\" style=\"background-color:" + surfice.status.data.color +"; color: " + getDynamicColor(surfice.status.data.color) + ";\">");
						$row.append("<td>" + surfice.name + "</td>");
						$row.append("<td>" + surfice.status.name + "</td>");
						
						// Since we're going backwards through the array
						// add this to the beginning of the element instead of the end
						$element.prepend($row);
					
						// We added a row so the table isn't empty
						empty = false;
						// We've used this surfice so delete it from the array
						tempData.splice(i, 1);
				
					}
				
				// If nothing is left in surfices, fill the table with only an empty row
				if (empty) {
					var $row = $("<tr><td>No Surfices in here</td></tr>");
					$element.append($row);
				}
			
			});
			
		}
		
		// Update the selectors to reflect addition or removal of surfices from surfs
		else if (selector.contains("surf-not-surfices")) {
			
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
				for (var key in data) {
				
					var surfice = data[key];
				
					// If the surfice is not part of this surf, make it available
					// to be added to the surf
					if ("surf-" + surfice.surf.id != surfId) {
						var $option = $("<option value=\"" + surfice.id + "\">" + surfice.name + "</option>");
						$element.append($option);
					}
				}
			});
		}
		
		// Update every delete dialog box for surfs
		else if (selector.contains("surf-delete")) {
			$elements.each(function() {
				$element = $(this);
				
				var surfId = $element.attr("data-ajax-id");
				$element.html("");
				
				
				
			});
		}
		
		
	});
	
}