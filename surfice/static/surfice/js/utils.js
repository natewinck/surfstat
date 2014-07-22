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