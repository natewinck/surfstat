$(function() {


jQuery.fn.fadeSlide = function(speed, easing, callback) {
  if (this.is(":hidden")) {
    return this.slideDown(speed, easing).fadeTo(speed, 1, easing, callback);
  } else {
    return this.fadeTo(speed, 0, easing).slideUp(speed, easing, callback);
  }
};
    
    
/* SMOOTH SCROLLING
------------------------------
*  Any time a link is clicked that goes to an #anchor,
*  scroll to it instead of jumping to it.
*  Also prevents a # from appearing in the URL
* 
*  INPUT
*  a[href*=#*]      Any <a> with an href that starts with # (but not only #)
*  
*  EVENT
*  click
------------------------------ */
$("a[href*=#]:not([href=#])").click(function() {
    if (location.pathname.replace(/^\//,'') == this.pathname.replace(/^\//,'') && location.hostname == this.hostname) {
        var target = $(this.hash);
        target = target.length ? target : $('[name=' + this.hash.slice(1) +']');
        if (target.length) {
            $('html,body').animate({
            scrollTop: target.offset().top
        }, 500);
        return false;
        }
    }
});



/* CHARTS
------------------------------ 
*  Sets up all charts on a page with the .chart selector.
*  Data is grabbed from the chartData[] associative array
*  that corresponds with the canvas's data-id attribute.
*  
*  When the chart either comes in view or is unhidden,
*  the chart fades in after a short delay.
*  
*  INPUT
*  canvas.chart
*  chartData[]        Global variable defined before this section
*  
*  EVENT
*  inview
*  
------------------------------ */
// Set up each of the inview events.
$("canvas.chart").on("inview", function() {
    var $this = $(this);
    $this.removeClass("hidden").off("inview");
    setTimeout(function() {
        showLineChart($this)
    }, 250);
    //$this.fadeIn(1000);
    $this.animate({ opacity: 1 }, 1000);
});

// showLineChart($this)
//
// Shows the line chart based on its data-id
function showLineChart($this) {
    // Get the canvas context
    var ctx = $this[0].getContext("2d");
    
    // Get the chart data that corresponds to the data-id
    var data = chartData[$this.attr("data-id")];
    
    
    // If colors are not set for the datasets, give them default color schemes
    for (var d in data.datasets) {
        var dataset = data.datasets[d];
        switch(Number(d)) {
            // First dataset color scheme
            case 0:
                if (!dataset.fillColor) dataset.fillColor = "rgba(220,220,220,0.5)";
                if (!dataset.strokColor) dataset.strokeColor = "rgba(220,220,220,1)";
                if (!dataset.pointColor) dataset.pointColor = "rgba(220,220,220,1)";
                if (!dataset.pointStrokeColor) dataset.pointStrokeColor = "#fff";
                break;
                
            // Second dataset color scheme (layered on top of first)
            case 1:
                if (!dataset.fillColor) dataset.fillColor = "rgba(73,23,109,0.5)";
                if (!dataset.strokColor) dataset.strokeColor = "rgba(52,12,75,1)";
                if (!dataset.pointColor) dataset.pointColor = "rgba(52,12,75,1)";
                if (!dataset.pointStrokeColor) dataset.pointStrokeColor = "#fff";
                break;
            
            // Default dataset color scheme
            default:
                if (!dataset.fillColor) dataset.fillColor = "rgba(220,220,220,0.5)";
                if (!dataset.strokColor) dataset.strokeColor = "rgba(220,220,220,1)";
                if (!dataset.pointColor) dataset.pointColor = "rgba(220,220,220,1)";
                if (!dataset.pointStrokeColor) dataset.pointStrokeColor = "#fff";
        }     
    }
    
    // Options for the animated charts
    var options = {
        ///Boolean - Whether grid lines are shown across the chart
        scaleShowGridLines : false,

        //String - Scale label font declaration for the scale label
        scaleFontFamily : "'Helvetica Neue', 'Arial'",

        //Function - Fires when the animation is complete
        onAnimationComplete : null
    }
    
    // Draw the chart
    var chart = new Chart(ctx).Line(data, options);
}




/* TABBABLE TABS
------------------------------ 
*  Assigns a CLICK event to all .nav a elements that have a data-toggle attribute.
*  The elements that have a corresponding id to the <a> href will show or hide.
*  
*  Pseudo example: <a href="#surfice"></a> will show <div id="surfice"></div>
*  
*  INPUT
*  .nav a[data-toggle]          <a> elements that have a data-toggle attribute
* 
*  EVENT
*  click
*
------------------------------ */
$('.nav a[data-toggle]').click(function (e) {
    e.preventDefault()
    $(this).tab('show')
})



/* SURFICE BUTTONS
------------------------------ 
*  Assigns a mouseover and mouseout event to all .surfice elements.
*  The first element inside .surfice will fade out when hovering over .surfice
*  while the second element will fade in.  The opposite is true on mouseout
*  
*  INPUT
* .surfice
* 
*  EVENT
*  hover (mouseover and mouseout)
*
------------------------------ */
/*
$(".surfice").hover(
    // Mouseover the Surfice element
    function() {
        // The First element of the Surfice is 
        // what is supposed to be displayed always
        // The Second element is hidden initially.
        // When hovering over Surfice, stop any animation
        // that might be happening (like fading in)
        
        $(this).children().first().stop().fadeOut(200);
        $(this).children().last().stop().fadeIn(200);
    },
    
    // Mouseout of the Surfice element
    function() {
        // When mousing out of a Surfice element,
        // Fade out the second element and fade in the
        // first (original) element.  But before that,
        // Stop any animation that might be happening (so
        // that it doesn't keep queueing up)
        
        $(this).children().last().stop().fadeOut(200);
        $(this).children().first().stop().fadeIn(200);
    }
);
*/



/* ON/OFF TOGGLE
------------------------------ 
*  Creates an on/off toggle switch out of checkbox inputs with .onoff-toggle
*  
*  INPUT
* .onoff-toggle
*
------------------------------ */
//$(".onoff-toggle").bootstrapSwitch();



/* DROPDOWN SELECT
------------------------------ 
*  Takes a bootstrap group button selector and turns it into
*  the equivalent of <select>.  It will also change a hidden input
*  and change the value to the value defined on the li elements.
*  
*  Takes any group of bootstrap buttons with the .dropdown-select class.
*  It then takes the text of the selected li element and puts it in the
*  element with the data-bind='label' attribute.
*  Next, it toggles the select so the dropdown disappears
*  Finally the input[type='hidden'] element within the .dropdown-select element
*  receives li[value] attribute
*  
*  If the dropdown also has .autosubmit class, the form is submitted
*  
*  INPUT
* .dropdown-select .dropdown-menu li        The li elements in the group button options
*
------------------------------ */
$(".dropdown-select .dropdown-menu li").click(function(event) {
    var $target = $( event.currentTarget );
    var $group = $target.closest( '.dropdown-select' )
    $group
        .find( '[data-bind="label"]' ).text( $target.text() )
        .end()
        .children( '.dropdown-toggle' ).dropdown( 'toggle' );
    
    $group.find( 'input[type="hidden"]' ).val( $target.attr("value") )
    
    // If the dropdown autosubmits the form, submit it now!
    if ($group.hasClass("autosubmit")) {
        $(this).parents("form").submit();
    }
    
    return false;
 
});
    

/* AUTOSUBMIT DROPDOWN
------------------------------ */
//$("form .dropdown-select.autosubmit .dropdown-menu li a").click(function(e) {
//    console.log("HI");
//    e.preventDefault();
//    
//    $(this).parents("form").submit();
//});


/* SELECT ALL
------------------------------ 
*  Finds all inputs that have the class select-all
*  When the user focuses on the input, select everything inside
*  
*  INPUT
*  input.select-all        input elements with class "select-all"
*
------------------------------ */
// $("input.select-all").click(function() {
// 	$(this).select();
// });
    

// $('#confirm-delete').on('show.bs.modal', function(e) {
//     $(this).find('form').attr('action', $(e.relatedTarget).data('href'));
//     console.log("here");
// });


/* LIST GROUP SELECT
------------------------------ 
*  Selects all list groups that the .select class and makes them a select
*  
*  INPUT
*  .list-group.select .list-group-item       The list elements (links)
*
------------------------------ */
$(".list-group.select .list-group-item").click(function(e) {
	// Prevent a # from showing up in the URL
	e.preventDefault();
	
	if (!$(this).hasClass("active")) {
		// Find the previous element that was selected
		var old_id = $(this).closest(".list-group.select").find(".list-group-item.active").removeClass("active").attr("href");
		var new_id = $(this).addClass("active").attr("href");
	
		// Using the id of the old selected item, fade out the corresponding panel
		// and fade in the new one
		//$(old_id).fadeSlide(750, "swing", $(new_id).fadeSlide());
		// $(old_id).fadeSlide(200, "swing", function() {
// 			$(this).removeClass("in");
// 			$(new_id).addClass("in").fadeSlide(200, "swing", function() {
// 				//$(this).addClass("in");
// 			});
// 		});
		console.log($(old_id));
		console.log($(new_id));
		$(old_id).removeClass("active in");
		$(new_id).addClass("active in");
		
	}
	
});


$(".navbar-nav a").click(function(e) {
	//e.preventDefault();
	var html;
	//console.log($(this).attr("href"));
	$.get($(this).attr("href"), function(html) {
		//var html = $.load($(this).attr("href"));
		console.log(html);
		//window.history.pushState({"html": html},"A new one", $(this).attr("href"));
	});
});

});