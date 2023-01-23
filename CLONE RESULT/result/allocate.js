
$(".requestAllocateStudent").submit(function(e) {

    e.preventDefault(); 

    var formdata = $('.requestAllocateStudent').serialize();

    var parentrequest = $('.requestAllocateStudent').serializeArray();
    var student_id=''; var requestSelected='';

    jQuery.each( parentrequest, function( i, field ) {
        if(i==2){
            student_id=field.value;
        } 

    });
    
    if(student_id==''){ 
        $('.activeError').text('Please select Child');
    }

    if(student_id!=''){

        var return_url=$('#return_url').val();

        $('#loader').show();

        $.ajax({
            type: 'POST',
            url: '/admin/allocate_student',
            dataType: "json",
            data: formdata,
            success: function (result) {
                setTimeout(function(){location.href='/admin/'+return_url} , 2000);                  
            }
        }); 
    }    

    return false;   

});




$(document).on('click', '.allocateStud', function(e){ 

    var selectedForm = $(this).data('rerquestaccept');    
    $('.sub'+selectedForm).addClass('submitRequest');
    $('.selectChildError'+selectedForm).addClass('activeError');

});  


$(document).on('click', '.stdClose', function(e){ 

    var selectedForm = $(this).data('rerquestaccept');    
    $('.sub'+selectedForm).removeClass('submitRequest');
    $('.selectChildError'+selectedForm).removeClass('activeError');

});  