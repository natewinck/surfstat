// Options for the animated graphs
var options = {
    //Boolean - If we show the scale above the chart data			
    scaleOverlay : false,

    //Boolean - If we want to override with a hard coded scale
    scaleOverride : false,

    //** Required if scaleOverride is true **
    //Number - The number of steps in a hard coded scale
    scaleSteps : null,
    //Number - The value jump in the hard coded scale
    scaleStepWidth : null,
    //Number - The scale starting value
    scaleStartValue : null,

    //String - Colour of the scale line	
    scaleLineColor : "rgba(0,0,0,.1)",

    //Number - Pixel width of the scale line	
    scaleLineWidth : 1,

    //Boolean - Whether to show labels on the scale	
    scaleShowLabels : true,

    //Interpolated JS string - can access value
    scaleLabel : "<%=value%>",

    //String - Scale label font declaration for the scale label
    scaleFontFamily : "'Arial'",

    //Number - Scale label font size in pixels	
    scaleFontSize : 12,

    //String - Scale label font weight style	
    scaleFontStyle : "normal",

    //String - Scale label font colour	
    scaleFontColor : "#666",	

    ///Boolean - Whether grid lines are shown across the chart
    scaleShowGridLines : false,

    //String - Colour of the grid lines
    scaleGridLineColor : "rgba(0,0,0,.05)",

    //Number - Width of the grid lines
    scaleGridLineWidth : 1,	

    //Boolean - Whether the line is curved between points
    bezierCurve : true,

    //Boolean - Whether to show a dot for each point
    pointDot : true,

    //Number - Radius of each point dot in pixels
    pointDotRadius : 3,

    //Number - Pixel width of point dot stroke
    pointDotStrokeWidth : 1,

    //Boolean - Whether to show a stroke for datasets
    datasetStroke : true,

    //Number - Pixel width of dataset stroke
    datasetStrokeWidth : 2,

    //Boolean - Whether to fill the dataset with a colour
    datasetFill : true,

    //Boolean - Whether to animate the chart
    animation : true,

    //Number - Number of animation steps
    animationSteps : 60,

    //String - Animation easing effect
    animationEasing : "easeOutQuart",

    //Function - Fires when the animation is complete
    onAnimationComplete : null
}

$(function() {

// SMOOTH SCROLLING
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

/* GRAPHS
------------------- */

// Set up each of the inview events.
$(".graph").on("inview", function() {
    var $this = $(this);
    $this.removeClass("hidden").off("inview");
    setTimeout(function() {
        showGraph($this)
    }, 250);
    //$this.fadeIn(1000);
    $this.animate({ opacity: 1 }, 1000)
});


function showGraph($this) {
    var ctx = $this[0].getContext("2d");
    
    var data = {
        labels : ["January","February","March","April","May","June","July"],
        datasets : [
            {
                fillColor : "rgba(220,220,220,0.5)",
                strokeColor : "rgba(220,220,220,1)",
                pointColor : "rgba(220,220,220,1)",
                pointStrokeColor : "#fff",
                data : [65,59,90,81,56,55,40]
            },
            {
                fillColor : "rgba(73,23,109,0.5)",
                strokeColor : "rgba(52,12,75,1)",
                pointColor : "rgba(52,12,75,1)",
                pointStrokeColor : "#fff",
                data : [28,48,40,19,96,27,40]
            }
        ]
    }

    var chart = new Chart(ctx).Line(data, options);
}
    
/* ----------------------------
/* Tabbable Tabs
/* ---------------------------- */
$('#hangtime a').click(function (e) {
    e.preventDefault()
    $(this).tab('show')
})


});