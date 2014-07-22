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