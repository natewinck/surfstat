$(document).ready(function() {
    //toggle `popup` / `inline` mode
    $.fn.editable.defaults.mode = 'popup';     
    
    //make username editable
    $('#username1').editable();
    
    
        //make username editable
    $('#update1').editable();
    
    
        //make username editable
    $('#add1').editable();

        //make username editable
    $('#username2').editable();
    
    
        //make username editable
    $('#update2').editable();
    
    
        //make username editable
    $('#add2').editable();
  
    //make username editable
    $('#username3').editable();
    
    
        //make username editable
    $('#update3').editable();
    
    
        //make username editable
    $('#add3').editable();

    
    //make status editable
    $('#status').editable({
        type: 'select',
        title: 'Select status',
        placement: 'right',
        value: 2,
        source: [
            {value: 1, text: 'status 1'},
            {value: 2, text: 'status 2'},
            {value: 3, text: 'status 3'}
        ]

        //uncomment these lines to send data on server
        ,pk: 1
        ,url: '/'
    });
});