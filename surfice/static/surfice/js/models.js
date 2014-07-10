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


function Surfstat() {
	this.surfs = [];
	this.surfices = [];
	this.statuses = [];
	this.events = [];
	this.dings = [];
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
	this.getJSON("ajax/" + action, getData, function(data) {
		
		// Get a single surf
		if (action == "get-surf") {
			console.log("get-surf");
			console.log(data);
			$.each(s.surfs, function(key, surf) {
				console.log(surf);
				if (surf.id == data.id) {
					console.log("Found!!");
					s.surfs[key] = data;
					return false;
				}
			});
		}
		
		// Get all the surfs
		else if (action == "get-surfs") {
			s.surfs = data;
		}
		
		// Get all the surfs and their containing surfices
		else if (action == "get-surfs-with-surfices") {
			s.surfs = data;
		}
		
		// Get a single surfice and put in the array
		else if (action == "get-surfice") {
			$.each(s.surfices, function(key, surfice) {
				if (surfice.id == data.id) {
					s.surfices[key] = surfice;
					return false;
				}
			});
		}
		
		// For getting ALL surfices (need to add specificity later)
		else if (action == "get-surfices") {
			// This is wrong...especially if I only get a few surfices
			s.surfices = data;
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