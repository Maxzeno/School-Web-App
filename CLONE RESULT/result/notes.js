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

    // Feed Dropzone
    dropzone_file_upload2 = function(el){
        if($('#myfeeddropzone').length == 0){
            return;
        }

        var panel = 'teacher' ;
        if($('.admin_add_lession').length){
            panel = 'admin' ;
        }

        var token = $('input[name="_token"]').val();
        Dropzone.autoDiscover = false;
        var myDropzone = new Dropzone("div#myfeeddropzone", {
            url: "/"+panel+"/attachmentimages",
            addRemoveLinks: true,
            // maxFiles: 1,
            acceptedFiles: ",image/*,.psd,.pdf",
            dictRemoveFile: 'Remove',
            params: {
                _token: token
        },
        success: function(file,done) {

            attachment.push(done.success.original);
            $('#studentsNotes').val(attachment);
            this.emit('removedfile',file);
            var mockup = {name: done.success.original, size: done.success.size};
            thumbImg = '/files/' + done.success.original
            this.emit('addedfile', mockup);
            var ext = file.name.split('.').pop();
            if (ext == "pdf") {
                thumbImg = '/images/pdf.png';
            } else if (ext.indexOf("doc") != -1) { thumbImg = '/images/pdf.png';
            } else if (ext.indexOf("xls") != -1) { thumbImg = '/images/pdf.png';
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
            var myString =  $(document).find('#studentsNotes').val().split(',');
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
            $(document).find('#studentsNotes').val(myString.toString());
            var note_id = ($('input[name="note_id"]').val() !== undefined) ? $('input[name="note_id"]').val() : '';
            $.ajax({
                type: 'POST',
                url: '/teacher/remove_noteimages',
                dataType: "json",
                data: { FileName: file.name, _token: token, note_id: note_id },
                success: function (result) {
                    // console.log(result);
                }
            });
        }})
        $(el).each(function (key, value) {
            var ext = value.original.split('.').pop();
            thumbImg = '/school/note/' + value.original
            if (ext == "pdf") {
                thumbImg = '/images/pdf.png';
            } else if (ext.indexOf("doc") != -1) { thumbImg = '/images/pdf.png';
            } else if (ext.indexOf("xls") != -1) { thumbImg = '/images/pdf.png';
            }
            var file = {name: value.original, size: value.size};
            myDropzone.options.addedfile.call(myDropzone, file);
            myDropzone.options.thumbnail.call(myDropzone, file, thumbImg);
            myDropzone.emit("complete", file);
        });
    }

    // Lesson note Dropzone for student's copy
    dropzone_file_upload3 = function(el){
        if($('#mylessondropzone').length == 0){
            return;
        }
        var userType = 'teacher';
        if($('.admin_add_lession').length){
            userType = 'admin' ;
        }

        var token = $('input[name="_token"]').val();
        Dropzone.autoDiscover = false;
        var myDropzone = new Dropzone("div#mylessondropzone", {
            url: `/${userType}/attachmentimages`,
            addRemoveLinks: true,
            // maxFiles: 1,
            acceptedFiles: ",image/*,.mp4,.mov,.avi,.mpeg, .flv, .mkv, mpg, .webm, .xls,.xlsx,.csv,.doc,.docx,.txt,application/doc,application/pdf,application/txt,'text/csv,application/vnd.ms-excel',application/ppt,application/pptx,application/docx",
            dictRemoveFile: 'Remove',
            params: {
                _token: token
        },
        success: function(file,done) {

            attachment.push(done.success.original);
            $('#studentsNotes').val(attachment);
            this.emit('removedfile',file);
            var mockup = {name: done.success.original, size: done.success.size};
            thumbImg = '/files/' + done.success.original
            this.emit('addedfile', mockup);
            var ext = file.name.split('.').pop();
            if (ext == "pdf") {
                thumbImg = '/images/pdf.png';
            }else if(ext == 'mp4' || ext == 'mov' || ext == 'avi'){
                thumbImg = "/images/video.png"; // default image path
            }else if(ext != 'png' && ext != 'jpg' && ext != 'jpeg'){
                thumbImg = "/images/contract.png"; // default image path
            }else{
                thumbImg = '/files/' + done.success.original;
            }

            this.emit('thumbnail', mockup, thumbImg);
            this.emit('complete', mockup)
        },
        removedfile: function(file) {
            var _ref;
            if (file.previewElement) {
                if ((_ref = file.previewElement) != null) {
                    _ref.parentNode.removeChild(file.previewElement);
                }
            }
            var myString =  $(document).find('#studentsNotes').val().split(',');
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
            $(document).find('#studentsNotes').val(myString.toString());
            var note_id = ($('input[name="note_id"]').val() !== undefined) ? $('input[name="note_id"]').val() : '';
            $.ajax({
                type: 'POST',
                url: `/${userType}/remove_noteimages`,
                dataType: "json",
                data: { FileName: file.name, _token: token, note_id: note_id, type: 'student' },
                success: function (result) {
                    console.log(result);
                }
            });
        }})
        $(el).each(function (key, value) {
            var ext = value.original.split('.').pop();
            thumbImg =  value.path;

            if (ext == "pdf") {
                thumbImg = '/images/pdf.png';
            }else if(ext == 'mp4' || ext == 'mov' || ext == 'avi'){
                thumbImg = "/images/video.png"; // default image path
            } else if(ext == null || !ext) {
                return;
            } else if(ext != 'png' && ext != 'jpg' && ext != 'jpeg'){
                thumbImg = "/images/contract.png"; // default image path
            }

            var file = {name: value.original, size: value.size};
            myDropzone.options.addedfile.call(myDropzone, file);
            myDropzone.options.thumbnail.call(myDropzone, file, thumbImg);
            myDropzone.emit("complete", file);
        });

    }

    dropzone_file_upload4 = function(el){
        let attach = [];
        if($('#mylessondropzone2').length == 0){
            return;
        }
        var userType = 'teacher';
        if($('.admin_add_lession').length){
            userType = 'admin';
        }

        var token = $('input[name="_token"]').val();
        Dropzone.autoDiscover = false;
        var myDropzone = new Dropzone("div#mylessondropzone2", {
            url: `/${userType}/attachmentimages`,
            addRemoveLinks: true,
            // maxFiles: 1,
            acceptedFiles: ",image/*,.mp4,.mov,.avi,.mpeg, .flv, .mkv, mpg, .webm, .xls,.xlsx,.csv,.doc,.docx,.txt,application/doc,application/pdf,application/txt,'text/csv,application/vnd.ms-excel',application/ppt,application/pptx,application/docx",
            dictRemoveFile: 'Remove',
            params: {
                _token: token
            },
            success: function(file,done) {
                attach.push(done.success.original);
                $('#teachersNotes').val(attach);
                this.emit('removedfile',file);
                var mockup = {name: done.success.original, size: done.success.size};
                thumbImg = '/files/' + done.success.original
                this.emit('addedfile', mockup);
                var ext = file.name.split('.').pop();
                if (ext == "pdf") {
                    thumbImg = '/images/pdf.png';
                }else if(ext == 'mp4' || ext == 'mov' || ext == 'avi'){
                    thumbImg = "/images/video.png"; // default image path
                }else if(ext != 'png' && ext != 'jpg' && ext != 'jpeg'){
                    thumbImg = "/images/contract.png"; // default image path
                }else{
                    thumbImg = '/files/' + done.success.original;
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
                var myString =  $(document).find('#teachersNotes').val().split(',');
                for( var i = 0; i < myString.length; i++){
                    if ( myString[i] === file.name) {
                        myString.splice(i, 1);
                    }
                }
                for( var i = 0; i < attach.length; i++){
                    if ( attach[i] === file.name) {
                        attach.splice(i, 1);
                    }
                }
                $(document).find('#teachersNotes').val(myString.toString());
                var note_id = ($('input[name="note_id"]').val() !== undefined) ? $('input[name="note_id"]').val() : '';
                $.ajax({
                    type: 'POST',
                    url: `/${userType}/remove_noteimages`,
                    dataType: "json",
                    data: { FileName: file.name, _token: token, note_id: note_id, type: 'teacher' },
                    success: function (result) {
                        console.log(result);
                    }
                });
            }})
        $(el).each(function (key, value) {
            var ext = value.original.split('.').pop();
            thumbImg =  value.path;

            if (ext == "pdf") {
                thumbImg = '/images/pdf.png';
            } else if(ext == 'mp4' || ext == 'mov' || ext == 'avi'){
                thumbImg = "/images/video.png"; // default image path
            } else if(ext == null || !ext) {
                return;
            } else if(ext != 'png' && ext != 'jpg' && ext != 'jpeg'){
                thumbImg = "/images/contract.png"; // default image path
            }
            var file = {name: value.original, size: value.size};
            myDropzone.options.addedfile.call(myDropzone, file);
            myDropzone.options.thumbnail.call(myDropzone, file, thumbImg);
            myDropzone.emit("complete", file);
        });

    }

    if($(document).find('form').hasClass('schoolDiarynotesValidate') == true){
        student_notes = ($(this).find('input[name="show_existing_student_attachment"]').val() !== undefined) ? JSON.parse($(this).find('input[name="show_existing_student_attachment"]').val()) : '';
        teacher_notes = ($(this).find('input[name="show_existing_teacher_attachment"]').val() !== undefined) ? JSON.parse($(this).find('input[name="show_existing_teacher_attachment"]').val()) : '';
        dropzone_file_upload3(student_notes);
        dropzone_file_upload4(teacher_notes);
    }
});
