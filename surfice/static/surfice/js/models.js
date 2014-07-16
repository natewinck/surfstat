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

/* Size
------------------------------
*  Find the size of an associative array.
*
*  RETURNS
*  The size
*  
------------------------------ */
if (typeof Object.size === 'undefined')
	Object.size = function(obj) {
		var size = 0, key;
		for (key in obj) {
			if (obj.hasOwnProperty(key)) size++;
		}
		return size;
	};

function Surfstat() {
	this.surfs = {};
	this.surfices = {};
	this.statuses = {};
	this.events = {};
	this.dings = {};
	// Ajax variable
	this.ajax = {
		// elements is a dictionary with selectors as the key
		$elements: {}
	};
}

Surfstat.prototype.getJSON = function(url, getData, callbackSuccess, callbackFail) {
	var s = this;
	var hasFailCallback = arguments.length == 4;
	$.getJSON(window.location.pathname + url, getData)
		.done(function(data) {
			// Make sure callback is a function
			if (typeof callbackSuccess === "function")
				callbackSuccess(data);
			
		})
		.fail(function(data) {
			if (hasFailCallback && typeof callbackFail === "function")
				callbackFail(data);
		});
}

Surfstat.prototype.getSurfs = function(callbackSuccess, callbackFail) {
	var s = this;
	this.getJSON("ajax/get-surfs", function(data){ s.surfs = data }, callbackFail);
}

Surfstat.prototype.getSurfices = function(callbackSuccess, callbackFail) {
	var s = this;
	this.getJSON("ajax/get-surfices", function(data){ s.surfices = data }, callbackFail);
}

Surfstat.prototype.getStatuses = function(callbackSuccess, callbackFail) {
	var s = this;
	this.getJSON("ajax/get-statuses", function(data){ s.statuses = data }, callbackFail);
}

Surfstat.prototype.getEvents = function(callbackSuccess, callbackFail) {
	var s = this;
	this.getJSON("ajax/get-events", function(data){ s.events = data }, callbackFail);
}

Surfstat.prototype.getDings = function(callbackSuccess, callbackFail) {
	var s = this;
	this.getJSON("ajax/get-dings", function(data){ s.dings = data }, callbackFail);
}

Surfstat.prototype.get = function(action, getData, callbackSuccess, callbackFail) {
	var s = this;
	if (typeof action === 'undefined') action = "";
	
	this.getJSON(action, getData, function(data) {
		
		// Remove "ajax/" from the action if it exists
		action = action.replace(/^(ajax\/)/gm, "");	
		
		// Get a single surf
		if (action == "get-surf") {
			console.log("get-surf");
			console.log(data);
			s.surfs[data.id] = data
		}
		
		// Get all the surfs
		else if (action == "get-surfs") {
			// Put the data into dictionary array by id
			for (var key in data) {
				s.surfs[data[key].id] = data[key];
			}
			//s.surfs = data;
		}
		
		// Get all the surfs and their containing surfices
		else if (action == "get-surfs-with-surfices") {
			// Put data into dictionary array by id
			for (var key in data) {
				s.surfs[data[key].id] = data[key];
			}
		}
		
		// Get a single surfice and put in the array
		else if (action == "get-surfice") {
			// Insert surfice into array at the correct point
			s.surfices[data.id] = data;
		}
		
		// For getting ALL surfices (need to add specificity later)
		else if (action == "get-surfices") {
			// Put data into dictionary array by id
			for (var key in data) {
				s.surfices[data[key].id] = data[key];
			}
		}
		
		// Get a single status and put it in the array
		else if (action == "get-status") {
			// Insert data into array at the correct dictionary position
			s.statuses[data.id] = data
		}
		
		// Get a single status and put it in the array
		else if (action == "get-statuses") {
			// Put data into dictionary array by id
			for (var key in data) {
				s.statuses[data[key].id] = data[key];
			}
		}
		
		else if (action == "get-event") {
			console.log(data);
			s.events[data.id] = data;
		}
		
		else if (action == "get-events") {
			// Put data into dictionary array by id
			for (var key in data) {
				s.events[data[key].id] = data[key];
			}
		}
		
		else if (action == "get-ding") {
			console.log(data);
			s.dings[data.id] = data;
		}
		
		else if (action == "get-dings") {
			// Put data into dictionary array by id
			for (var key in data) {
				s.dings[data[key].id] = data[key];
			}
		}
		
		// If action is empty or not available
		else {
			var data = (data) ? data : {};
		}
		
		// After everything, call the callback
		callbackSuccess(data);
	},
	function(data) {
		if (typeof callbackFail === 'function')
			callbackFail(data);
	});
}

// Get a surf based on the id provided
Surfstat.prototype.surf = function(id) {
	for (var key in this.surfs) {
		if (this.surfs[key].id == id) {
			return this.surfs[key];
		}
	}
}

Surfstat.prototype.notify = function(type, text) {
	$('.notifications').notify({
		type: type,
		message: { text: text },
		transition: '',
		fadeOut: { enabled: true, delay: 3000 },
		// onClose overrides fadeOut (custom)
		onClose: function(element) {
			$(element).removeClass("fade in");
			$(element).stop(true).fadeSlide(200, "swing");
		}
	}).show(); // for the ones that aren't closable and don't fade out there is a .hide() function.
}

ss = new Surfstat();