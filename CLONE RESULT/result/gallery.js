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

    dropzone_file_upload = function(el){

        var token = $('input[name="_token"]').val();
        Dropzone.autoDiscover = false; 
        var myDropzone = new Dropzone("div#mydropzone", { 
            url: "/admin/gallery_attachment_images",
            addRemoveLinks: true,
            acceptedFiles: "image/*",
            dictRemoveFile: 'Remove',
            params: {
                _token: token
        },
        success: function(file,done) {
            attachment.push(done.success.original);
            $('#eventimages').val(attachment);
            this.emit('removedfile',file);
            var mockup = {name: done.success.original, size: done.success.size};
            this.emit('addedfile', mockup);
            this.emit('thumbnail', mockup, '/files/' + done.success.original);
            this.emit('complete', mockup)
        },removedfile: function(file) {
            var _ref;
            if (file.previewElement) {
                if ((_ref = file.previewElement) != null) {
                    _ref.parentNode.removeChild(file.previewElement);
                }
            }
            var myString =  $(document).find('#eventimages').val().split(',');
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
            $(document).find('#eventimages').val(myString.toString());
            var gallery_id = ($('input[name="gallery_id"]').val() !== undefined) ? $('input[name="gallery_id"]').val() : '';
            $.ajax({
                type: 'POST',
                url: '/admin/gallery_remove_images',
                dataType: "json",
                data: { FileName: file.name, _token: token, gallery_id: gallery_id },
                success: function (result) {
                // console.log(result);                            
                   
                }
            });            
        }})
        $(el).each(function (key, value) {
            var file = {name: value.original, size: value.size};
            myDropzone.options.addedfile.call(myDropzone, file);
            myDropzone.options.thumbnail.call(myDropzone, file,  value.path);
            myDropzone.emit("complete", file);
        });

        
    }

    if($(document).find('form').hasClass('uploadsFilesGallery') == true){

    	show_images = ($(this).find('input[name="show_exist_attachment"]').val() !== undefined) ? JSON.parse($(this).find('input[name="show_exist_attachment"]').val()) : '';
    	dropzone_file_upload(show_images);
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

$(document).on('click', '#editsaveGallery', function() {

    if($('input[name="albumImageRemove"]').val()==''){
        $('input[name="albumImageRemove"]').prop('required',true);
    }    

});