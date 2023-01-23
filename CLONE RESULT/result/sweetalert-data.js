/*SweetAlert Init*/

$(function() {
	"use strict";

	var SweetAlert = function() {};

    //examples
    SweetAlert.prototype.init = function() {

    //Warning Message
    $(document).on("click", '#is_delete .is_delete' ,function(e){
        var Id = $(this).data('id');
        var Message = $(this).data('message');
        var url = $(this).data('url');
        var redirect = $(this).data('redirect');
        var CSRF_TOKEN = $('meta[name="csrf-token"]').attr('content');
        var is_true = false;
        var message = '';
        var textmes=''; var confirmButtonTextmes ='';
        if(url=='/admin/rejectRequest'){
            textmes = "Do you want to "+Message+" ?";
            confirmButtonTextmes ='Yes, Reject it!';
        }else{
            textmes = "Do you want to Delete the "+Message+" ?";
            confirmButtonTextmes ='Yes, Delete it!';
        }

        swal({
            title: "Are you sure?",
            text: textmes,
            type: "warning",
            showCancelButton: true,
            confirmButtonColor: "#A57BB6",
            confirmButtonText: confirmButtonTextmes,
            closeOnConfirm: false,
            showLoaderOnConfirm: true
        }, function(isConfirm){
            if (isConfirm) {
                $('#loader').show();
                $.ajax({
                    /* the route pointing to the post function */
                    url: url,
                    type: 'POST',
                    async: true,
                    /* send the csrf-token and the input to the controller */
                    data: {_token: CSRF_TOKEN, id: Id,delete:2},
                    dataType: 'JSON',
                    /* remind that 'data' is the response of the AjaxController */
                    success: function (data) {
                        if(data.status == 200){
                            swal(""+Message+"!", Message+" "+data.message+" Successfully.", data.code);
                            setTimeout(function(){location.href=redirect} , 2000);
                        }else{
                            swal(""," "+data.message+".", data.code);
                        }
                    }
                });
            }
        });
        return false;
    });


    //Basic
    $('#sa-basic').on('click',function(e){
	    swal({
			title: "Here's a message!",
            confirmButtonColor: "#4e9de6",
        });
		return false;
    });

    //A title with a text under
    $('#sa-title').on('click',function(e){
	    swal({
			title: "Here's a message!",
            text: "Lorem ipsum dolor sit amet",
			confirmButtonColor: "#4e9de6",
        });
		return false;
    });

    //Success Message
	$('#sa-success').on('click',function(e){
        swal({
			title: "Updated Successfully!",
             type: "success",
			text: "Lorem ipsum dolor sit amet",
			confirmButtonColor: "#A57BB6",
        });
        setTimeout(function(){location.href="manage-users.php"} , 2000);
       // window.location.href = 'http://www.google.com';
		return false;
    });

    //Warning Message
  //   $('#sa-warning,.sa-warning').on('click',function(e){
	 //    swal({
  //           title: "Are you sure?",
  //           text: "Do you want to Deactivate the User ?",
  //           type: "warning",
  //           showCancelButton: true,
  //           confirmButtonColor: "#A57BB6",
  //           confirmButtonText: "Yes, Deactivate it!",
  //           closeOnConfirm: false
  //       }, function(){
  //           swal("Deactivated!", "User Deactivated Successfully.", "success");
  //           setTimeout(function(){location.href="manage-users.php"} , 2000);
  //       });

		// return false;
  //   });


    //Warning Message
    // $('#delete_user').on('click',function(e){
    //     swal({
    //         title: "Are you sure?",
    //         text: "Do you want to delete ?",
    //         type: "warning",
    //         showCancelButton: true,
    //         confirmButtonColor: "#A57BB6",
    //         confirmButtonText: "Yes, Delete it!",
    //         closeOnConfirm: false
    //     }, function(){
    //         swal("Deleted!", "User Deleted Successfully.", "success");
    //         setTimeout(function(){location.href=""} , 2000);
    //     });

    //     return false;
    // });

    //Parameter
	$('#sa-params').on('click',function(e){
        swal({
            title: "Are you sure?",
            text: "You will not be able to recover this imaginary file!",
            type: "warning",
            showCancelButton: true,
            confirmButtonColor: "#f0c541",
            confirmButtonText: "Yes, delete it!",
            cancelButtonText: "No, cancel plx!",
            closeOnConfirm: false,
            closeOnCancel: false
        }, function(isConfirm){
            if (isConfirm) {
                swal("Deleted!", "Your imaginary file has been deleted.", "success");
            } else {
                swal("Cancelled", "Your imaginary file is safe :)", "error");
            }
        });
		return false;
    });

    //Custom Image
	$('#sa-image').on('click',function(e){
		swal({
            title: "John!",
            text: "Recently joined twitter",
            imageUrl: "dist/img/user.png" ,
			confirmButtonColor: "#ed6f56",

        });
		return false;
    });

    //Auto Close Timer
	$('#sa-close').on('click',function(e){
        swal({
            title: "Auto close alert!",
            text: "I will close in 2 seconds.",
            timer: 2000,
            showConfirmButton: false
        });
		return false;
    });


    },
    //init
    $.SweetAlert = new SweetAlert, $.SweetAlert.Constructor = SweetAlert;

	$.SweetAlert.init();
});
