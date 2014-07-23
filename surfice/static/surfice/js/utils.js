/* iequals
------------------------------
*  Checks if two strings are equal to each other (case insensitive).
*
*  Example: "A cool Surf" turns into "a-cool-surf"
*
*  RETURNS
*  bool
*  
------------------------------ */
if (typeof String.prototype.iequals === 'undefined') String.prototype.iequals = function(string) { return this.toLowerCase() === string.toLowerCase(); };

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

/* getDynamicColor
------------------------------ 
*  Gets the color that the text should be
*  against a color of background
*  
*  INPUT
*  rgb		RGB or hex color of the background "rgb(255, 255, 255)"
*  
*  RETURNS
*  rgb white or "inherit"
*  
------------------------------ */
function getDynamicColor(rgb) {
	// If they entered a hex code by accident...
	if (rgb.indexOf("#") > -1) {
		var hex = rgb;
		var result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
		rgb = (result) ? [
			parseInt(result[1], 16),
			parseInt(result[2], 16),
			parseInt(result[3], 16)
		] : null;
	
	} else {
		rgb = rgb.match(/^rgb\((\d+),\s*(\d+),\s*(\d+)\)$/);
		rgb.shift();
	}

	var total = 0;
	for (var i = 0; i < rgb.length; i++) {
		total += parseInt(rgb[i]);
	}
	
	var avg = total / 3.0;
	
	// If the average is less than halfway to dark
	// change the color of the text to white
	if (avg / 255 < 0.4) {
		return "rgb(255, 255, 255)";
	} else {
		return "inherit";
	}
}