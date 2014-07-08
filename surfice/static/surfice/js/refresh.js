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
	
	// Now loop through the selectors and fire a separate method for each one
	for (var key in selectors) {
		
		// For convenience sake, make a selector variable
		var selector = selectors[key];
		
		// First get the element(s) that match this selector
		$elements = $("[data-ajax-update=\"" + selector + "\"]");
		
		// If an element was found, start firing functions
		$elements.each(function() {
			var $element = $(this);
			
			// If surf-name is set, change the contents of the
			// element to the data.name variable
			if (selector.contains("surf-name")) {
				
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
			}
			
			// Change the contents to description
			else if (selector.contains("surf-description")) {
				$element.text(data.description);
			}
			
			// Change the contents of ALL the surfices tables
			else if (selector.contains("surf-surfices")) {
				
				var surfId = $element.attr("data-ajax-id").slugify();
				//console.log(surfId);
				$element.html("");
				
				// Loop through the data looking for the same surf id
				var indicesToRemove = [];
				var empty = true;
				for (var key in data) if ("surf-" + data[key].surf.name.slugify() == surfId) {
					//console.log(data[key].name);
					// If there's a match for this piece of data, add it to the table
					//for (var key in data) {
					var surfice = data[key];
					var $row = $("<tr class=\"dynamic-color\" style=\"background-color:" + surfice.status.data.color +"; color: " + getDynamicColor(surfice.status.data.color) + ";\">");
					$row.append("<td>" + surfice.name + "</td>");
					$row.append("<td>" + surfice.status.name + "</td>");
		
					$element.append($row);
					indicesToRemove.push(key);
					empty = false;
					//data.splice(key, 1);
					//}
					
				}
				//console.log(indicesToRemove);
				for (var key in indicesToRemove) {
					// Don't do this yet...it might interfere with the selectors
					// Maybe work with a local copy of the data so it goes faster
					//data.splice(parseInt(indicesToRemove[key]), 1);
				}
				
				if (empty) {
					var $row = $("<tr><td>No Surfices in here</td></tr>");
					$element.append($row);
				}
				//console.log(data);
				
				
				
			}
			
			// Update the selectors to reflect addition or removal of surfices from surfs
			else if (selector.contains("surf-not-surfices")) {
				var surfId = $element.attr("data-ajax-id").slugify();
				
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
					if ("surf-" + surfice.surf.name.slugify() != surfId) {
						var $option = $("<option value=\"" + surfice.id + "\">" + surfice.name + "</option>");
						$element.append($option);
					}
				}
			}
			
		});
	}
	
}