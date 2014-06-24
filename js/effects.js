$(function() {

    
    
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

});