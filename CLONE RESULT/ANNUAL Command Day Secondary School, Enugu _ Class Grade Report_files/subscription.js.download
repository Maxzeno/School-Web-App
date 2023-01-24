$("#subscriptionData").on("submit", function(e) {

    e.preventDefault();

    var school_id = $("#school_id").val();
    var studentsCount = $("#studentsCount").val();
    var currency = $("#currency").val();
    var duration = $("#duration").val();
    var contactNumber = $("#contactNumber").val();

    if(school_id !='' && studentsCount!='' && currency !='' && contactNumber!=''){
        $.ajax({
            type: 'POST',
            url: '/admin/store_accountPlan',
            dataType: "json",
            data: $('#subscriptionData').serialize(),
            beforeSend: function(){
                $('#loader').css('display','block');
            },
            success:function(res){

                if($.isEmptyObject(res.error)){
                    $('#loader').css('display','none');
                    $('#subscribemodal').modal('hide');
                    $('#confirmation_popup').modal('show');

                    setTimeout(function() {
                        location.reload();
                    }, 5000);

                }else{

                    $.each( res.error, function( key, value ) {

                        $('#loader').css('display','none');

                        if(key=='currency' || key=='currency'){

                            $('select[name="'+key+'"]').closest('.form-group').addClass('has-error');
                            $('select[name="'+key+'"]').closest('.form-group').find('div.help-block').removeClass("hide").slideDown(400).html(value);

                        }else{
                            $('input[name="'+key+'"]').closest('.form-group').addClass('has-error');
                            $('input[name="'+key+'"]').closest('.form-group').find('div.help-block').removeClass("hide").slideDown(400).html(value);
                        }

                    });
                }
            },error: function(xhr, ajaxOptions, thrownError) {

                $('#loader').css('display','none');
            }

        });

    }else{
       console.log('You are not authoried.');
    }

    return false;


});




$(document).on('click', '.fillDataSubscription', function(e){

    var subscriptionDate= $(this).data('subscriptiondate');
    var school_id= $(this).data('school_id');

    $('#school_id').val(school_id);
    $('#subscriptionDate').val(subscriptionDate);

    $('#subscriptionDate').datetimepicker({
        // setDate: new Date(subscriptionDate),
        format: 'DD-MM-YYYY'
            // ignoreReadonly: true


    });



    // $('#subscriptionDate').datetimepicker("setDate", new Date(subscriptionDate) );

});

$(document).on('click', '.fillDataContract', function(e){

    var contractDate= $(this).data('contractdate');
    var partner_id= $(this).data('partner_id');

    $('#partner_id').val(partner_id);
    $('#contractDate').val(contractDate);

    $('#contractDate').datetimepicker({
        // setDate: new Date(subscriptionDate),
        format: 'DD-MM-YYYY'
            // ignoreReadonly: true


    });



    // $('#subscriptionDate').datetimepicker("setDate", new Date(subscriptionDate) );

});


/* jQuery(function() {
         jQuery( "#subscriptionDate" ).datepicker({ }).attr('readonly','readonly');
    });*/

$("#store_subscriptionDate").on("submit", function(e) {

    e.preventDefault();

    var school_id = $("#school_id").val();
    var subscriptionDate = $("#subscriptionDate").val();

    if(school_id !='' && subscriptionDate!=''){
        $.ajax({
            type: 'POST',
            url: '/superadmin/store_subscriptionDate',
            dataType: "json",
            data: $('#store_subscriptionDate').serialize(),
            beforeSend: function(){
                $('#loader').css('display','block');
            },
            success:function(res){

                if($.isEmptyObject(res.error)){
                    $('#loader').css('display','none');
                    $('#expireDateModal').modal('hide');
                    $('#confirmation_popup').modal('show');

                    setTimeout(function() {
                        location.reload();
                    }, 5000);

                }else{

                    $.each( res.error, function( key, value ) {

                        $('#loader').css('display','none');

                        $('input[name="'+key+'"]').closest('.form-group').addClass('has-error');
                        $('input[name="'+key+'"]').closest('.form-group').find('div.help-block').removeClass("hide").slideDown(400).html(value);

                    });
                }
            },error: function(xhr, ajaxOptions, thrownError) {

                $('#loader').css('display','none');
            }

        });

    }else{
       console.log('You are not authoried.');
    }

    return false;


});

$("#save_contractDate").on("submit", function(e) {

    e.preventDefault();

    var partner_id = $("#partner_id").val();
    var subscriptionDate = $("#contractDate").val();

    if(partner_id !='' && subscriptionDate!=''){
        $.ajax({
            type: 'POST',
            url: '/superadmin/save_contractDate',
            dataType: "json",
            data: $('#save_contractDate').serialize(),
            beforeSend: function(){
                $('#loader').css('display','block');
            },
            success:function(res){

                if($.isEmptyObject(res.error)){
                    $('#loader').css('display','none');
                    $('#expireDateModal').modal('hide');
                    $('#confirmation_popup').modal('show');

                    setTimeout(function() {
                        location.reload();
                    }, 5000);

                }else{

                    $.each( res.error, function( key, value ) {

                        $('#loader').css('display','none');

                        $('input[name="'+key+'"]').closest('.form-group').addClass('has-error');
                        $('input[name="'+key+'"]').closest('.form-group').find('div.help-block').removeClass("hide").slideDown(400).html(value);

                    });
                }
            },error: function(xhr, ajaxOptions, thrownError) {

                $('#loader').css('display','none');
            }

        });

    }else{
       console.log('You are not authoried.');
    }

    return false;


});
