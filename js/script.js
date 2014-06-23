$(document).ready(function() {
      
    $('.service-active').mouseenter(function(){
        $(this).fadeOut('fast');
        $(this).next().fadeIn('fast');
    });
    $('.service-hover').mouseout(function(){
        $(this).fadeOut('fast');
        $(this).prev().fadeIn('fast');
    });
    
    $('.service').mouseenter(function(){
        console.log('enter');
    });
    $('.service').mouseout(function() {
        console.log('exit');
    });
    
});
