jQuery( function ( $ ) {
    var attachment = [];
    var show_images;
    // sa-confirm-button-container
    isNumber = function (evt) {
        evt = (evt) ? evt : window.event;
        var charCode = (evt.which) ? evt.which : evt.keyCode;
        if (charCode > 31 && (charCode <= 45 || charCode > 57)) {
            return false;
        }
        return true;
    }

    dropzone_file_upload2 = function(el){

        var token = $('input[name="_token"]').val();
        Dropzone.autoDiscover = false; 
        var myDropzone = new Dropzone("div#mydocumentdropzone", { 
            url: "/admin/attachment_images",
            addRemoveLinks: true,
            // acceptedFiles: "image/*,.mp4,.mov,.avi,.mpeg, .flv, .mkv, mpg, .webm, .xls,.xlsx,.csv,.doc,.docx,.txt,application/doc,application/pdf,application/txt,'text/csv,application/vnd.ms-excel',application/ppt,application/pptx,application/docx",
            dictRemoveFile: 'Remove',
            params: {
                _token: token
        },
        success: function(file,done) {
            attachment.push(done.success.original);
            $('#uploaddocError').removeClass('has-error has-danger');
            $('#documentimages').val(attachment);
            this.emit('removedfile',file);
            var mockup = {name: done.success.original, size: done.success.size};
            this.emit('addedfile', mockup);

            var filename = (file.name); // Get extension
            var newimage = "";

            var filename = filename.toLowerCase();
            var ext = filename.split('.').pop();

            // Check extension
            if (ext == "pdf") {
                thumbImg = '/images/pdf.png';
            }else if(ext == 'mp4' || ext == 'mov' || ext == 'avi'){
                thumbImg = "/images/video.png"; // default image path
            }else if(ext != 'png' && ext != 'jpg' && ext != 'jpeg'){
                thumbImg = "/images/contract.png"; // default image path
            }else{
                thumbImg = "/images/image.png"; // default image path
            }
            this.emit('thumbnail', mockup, thumbImg);
            this.emit('complete', mockup)
        },removedfile: function(file) {

            var _ref;
            if (file.previewElement) {
                if ((_ref = file.previewElement) != null) {
                    _ref.parentNode.removeChild(file.previewElement);
                }
            }
            var myString =  $(document).find('#documentimages').val().split(',');
            for( var i = 0; i < myString.length; i++){ 
               if ( myString[i] === file.name) {
                    myString.splice(i, 1); 
               }
            }
            for( var i = 0; i < attachment.length; i++){ 
               if ( attachment[i] === file.name) {
                    attachment.splice(i, 1); 
               }
            }
            $(document).find('#documentimages').val(myString.toString());
            var document_id = ($('input[name="document_id"]').val() !== undefined) ? $('input[name="document_id"]').val() : '';
            $.ajax({
                type: 'POST',
                url: '/admin/remove_documentimages',
                dataType: "json",
                data: { FileName: file.name, _token: token, document_id: document_id },
                success: function (result) {
                   
                },
                error: function(err){

                }
            });            
        }})
        $(el).each(function (key, value) {
            var file = {name: value.original, size: value.size};
            myDropzone.options.addedfile.call(myDropzone, file);
            
                var thumbImg = value.path;

            var filename = (file.name); // Get extension
            var newimage = "";

            var filename = filename.toLowerCase();
            var ext = filename.split('.').pop();

            // Check extension
            if (ext == "pdf") {
                thumbImg = '/images/pdf.png';
            }else if(ext == 'mp4' || ext == 'mov' || ext == 'avi'){
                thumbImg = "/images/video.png"; // default image path
            }else if(ext != 'png' && ext != 'jpg' && ext != 'jpeg'){
                thumbImg = "/images/contract.png"; // default image path
            }else{
                thumbImg = "/images/image.png"; // default image path
                 thumbImg = value.path;

            }

            myDropzone.options.thumbnail.call(myDropzone, file, thumbImg);

            myDropzone.emit("complete", file);
        });

        
    }

    if($(document).find('form').hasClass('uploadsDocuments') == true){

        show_images = ($(this).find('input[name="show_exist_attachment"]').val() !== undefined) ? JSON.parse($(this).find('input[name="show_exist_attachment"]').val()) : '';
        dropzone_file_upload2(show_images);
    }
});   


$(document).on('click', '.dropify-clear', function() {

    var removeimage =$(this).parent().find('input').data('image');

    if(removeimage=='albumImageRemove'){
        $(this).parent().find('input').prop('required',true);
    }

});



$(document).on('click', '#saveGallery', function() {

    if($('input[name="albumImage"]').val()==''){
        $('input[name="albumImage"]').prop('required',true);
    }    

});

$('body').on('change','#doc_class,#docsessionid',function(){

    var class_id = $('#doc_class').val(); 
    var token = $('input[name="_token"]').val();
    var session_id = $('select[name="session_id"]').val();
     
    if(class_id){
        $.ajax({
            type: 'POST',
            url: '/admin/getstudents',
            dataType: "json",
            data: { class_id: class_id, session_id: session_id, _token: token },

            success:function(res){  
               
                $('#student_ids').removeAttr("readOnly");
                $('#student_ids').prop("readOnly",false);

                if(res){   
                
                    var html='';
                    $.each(res,function(key,value){
                        html += '<option value="'+key+'">'+value+'</option>';
                    });
                    
                    $('#studentdiv').show();
                    $('#student_ids').addClass('selectpicker');
                    $('#student_ids').html(html);
                    $("#student_ids").attr('required',true);
                    $("#student_ids").selectpicker('refresh');
                }else{
                   
                    $('#student_ids').html('<option value="">Select Student</option>');
                    $("#student_ids").selectpicker('refresh');
                    
                }
            },error:function(err){
                alert('errorr');

            }


        });
    }else{
       $('#student_ids').html('<option value="">Select Student</option>');
       $('#student_ids').selectpicker('refresh');

        // $(".student").empty();
    }

// 5c963cb6b38edb7cff5b68e6,5c9fbee0b38edb5a192cb8ba
});


$('body').on('change', '.docType', function(){

    var docType = $(this).val(); 

    if(docType=='selected'){
        $("#student_ids").attr('required');
        $("#doc_class").attr('required',true);
        $("#student_ids").html('');
        $("#student_ids").selectpicker('refresh');
        $("#doc_class").val('');
        $("#doc_class").selectpicker('refresh');
        $('#showClassSection').show();

    }else{

        $("#student_ids").removeAttr('required');
        $("#doc_class").removeAttr('required');

        $("#student_ids").html('');
        $("#student_ids").selectpicker('refresh');
        $("#doc_class").selectpicker('refresh');
        $('#showClassSection').hide();
        $('#studentdiv').hide();
    } 
});    

$("form#uploadsDocuments").submit(function(e){
    
    if($('#documentimages').val()==''){
        $('#uploaddocError').addClass('has-error has-danger');
        e.preventDefault();
    }

});



