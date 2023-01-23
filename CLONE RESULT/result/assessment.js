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
            url: "/admin/assessment_attachment_images",
            addRemoveLinks: true,
            // acceptedFiles: "image/*,.xls,.xlsx,.csv,application/doc,application/pdf,application/txt,'text/csv,application/vnd.ms-excel',application/ppt,application/pptx,application/docx",
            dictRemoveFile: 'Remove',
            params: {
                _token: token
        },
        success: function(file,done) {
            $('div#mydropzone').css('border', '1px solid rgba(33, 33, 33, 0.12)');
            $('#mydropzone').parent().find('.help-block').html('');
            attachment.push(done.success.original);
            $('#eventimages').val(attachment);
            this.emit('removedfile',file);
            var mockup = {name: done.success.original, size: done.success.size};
            this.emit('addedfile', mockup);
            var filename = (file.name); // Get extension
            var newimage = "";

            var filename = filename.toLowerCase();
            var ext = filename.split('.').pop();

            // Check extension
            if(ext != 'png' && ext != 'jpg' && ext != 'jpeg'){
                newimage = "/images/contract.png"; // default image path

                this.emit('thumbnail', mockup, newimage);
            }else{
                this.emit('thumbnail', mockup, '/files/' + done.success.original);
            }

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
            var assessment_id = ($('input[name="assessment_id"]').val() !== undefined) ? $('input[name="assessment_id"]').val() : '';
            $.ajax({
                type: 'POST',
                url: '/admin/assessment_remove_images',
                dataType: "json",
                data: { FileName: file.name, _token: token, assessment_id: assessment_id },
                success: function (result) {

                }
            });
        }})
        $(el).each(function (key, value) {
            var file = {name: value.original, size: value.size};
            myDropzone.options.addedfile.call(myDropzone, file);

            var filename = (file.name); // Get extension
            var newimage = "";

            var filename = filename.toLowerCase();
            var ext = filename.split('.').pop();

            // Check extension
            if(ext != 'png' && ext != 'jpg' && ext != 'jpeg'){

                newimage = "/images/contract.png";
                myDropzone.options.thumbnail.call(myDropzone, file, newimage);

            }else{
                myDropzone.options.thumbnail.call(myDropzone, file, value.path);
            }


            myDropzone.emit("complete", file);
        });


    }

    if($(document).find('form').hasClass('uploadsFilesAssessment') == true){

    	show_images = ($(this).find('input[name="show_exist_attachment"]').val() !== undefined) ? JSON.parse($(this).find('input[name="show_exist_attachment"]').val()) : '';
    	dropzone_file_upload(show_images);
	}


});


$('body').on('change', '#class_id,#schoolClassId', function(){

    var class_id = $(this).val();

    if(class_id!=''){
        var token = $('input[name="_token"]').val();

        $.ajax({
            type: 'POST',
            url: '/admin/class_subjects',
            dataType: "json",
            data: { class_id: class_id, _token: token },
            success: function (result) {
                $('#subject_id').html(result.subjects)
                $('#subject_id').selectpicker('refresh');
            }
        });
    }else{
        $('#subject_id').html('<option value="">Select Subject </option>')
        $('#subject_id').selectpicker('refresh');

        $('#teacher_id').html('<option value="">Select Teacher </option>')
        $('#teacher_id').selectpicker('refresh');
    }

});


$('body').on('change', '#subject_id', function(){

    var subject_id = $(this).val();

    if(class_id!=''){
        var token = $('input[name="_token"]').val();

        $.ajax({
            type: 'POST',
            url: '/admin/subject_teacher',
            dataType: "json",
            data: { subject_id: subject_id, _token: token },
            success: function (result) {
                $('#teacher_id').html(result.teacher)
                $('#teacher_id').selectpicker('refresh');
            }
        });
    }else{

        $('#teacher_id').html('<option value="">Select Teacher </option>')
        $('#teacher_id').selectpicker('refresh');
    }

});

// Function that handles Dropdown Change on Add Attendance
function handleAttendanceInputsChange() {
    var class_id = $('#classStudent').val();
    var session_id = $('#attendanceSession').val();
    var attendanceDate = $('#attendanceDate').val();

    if(class_id !='' && session_id != '' && attendanceDate != ''){

        $('#attendanceStudent').show();
        var token = $('input[name="_token"]').val();

        $.ajax({
            type: 'POST',
            url: '/admin/classStudents',
            dataType: "json",
            data: { class_id: class_id, session_id: session_id, attendanceDate: attendanceDate, _token: token },
            success: function (result) {
                $('#studentsList').html(result.students)
                // Attendacne Timepicker Initializer
                $('.attendance_time').datetimepicker({
                    format: 'LT',
                });
                $('.attendance_time').css({'width': '110px'});
            }
        });
    }else{
        $('#attendanceStudent').hide();
        $('#studentsList').html('No Student');
    }
}

$(document).on('change', '#attendanceSession', function () {
    var session_id = $(this).val();
    var token = $('input[name="_token"]').val();
    if( session_id){
        $.ajax({
            type: 'POST',
            url: '/admin/sessiontermdata',
            async: false,
            dataType: "json",
            data: { session_id:session_id, _token: token },

            success:function(res){
                if(res){
                    if (res['termhtml']) {
                        $("#attendanceTerm").html(res['termhtml']);
                        $('#attendanceTerm').removeAttr("disabled");
                        $('#attendanceTerm').selectpicker('refresh');
                    }
                }
            }, error: function(err){

            }
        });
    }else{
        $("#gradeAttedanceTerm").html('<option value="">Select Term</option>');
        $('#gradeAttedanceTerm').attr("disabled");
        $('#gradeAttedanceTerm').selectpicker('refresh');
    }
});

// When Class Changes
$('body').on('change', '#classStudent', function(){
    handleAttendanceInputsChange();
});

// When Date Changes
$('body').on('dp.change', '#attendanceDate', function(){
    handleAttendanceInputsChange();
});

$('body').on('change', '#attendanceSession', function(){
    var session_id = $(this).val();
    var class_id = $('#classStudent').val();
    var attendanceDate = $('#attendanceDate').val();

    if(class_id != '' && session_id != '' && attendanceDate != ''){
        $('#attendanceStudent').show();
        var token = $('input[name="_token"]').val();

        $.ajax({
            type: 'POST',
            url: '/admin/classStudents',
            dataType: "json",
            data: { class_id: class_id, session_id: session_id, attendanceDate: attendanceDate, _token: token },
            success: function (result) {
                $('#studentsList').html(result.students)
            }
        });
    }else{
        $('#attendanceStudent').hide();

        $('#studentsList').html('No Student');
    }
});

$('body').on('change', '#schoolSessionId', function(){
    var session_id = $(this).val();
    var class_id = $('#class_Student').val();
    if(class_id!=''){
        $('#attendanceStudent').show();
        var token = $('input[name="_token"]').val();

        $.ajax({
            type: 'POST',
            url: '/admin/getstudents',
            dataType: "json",
            data: { session_id: session_id, class_id: class_id, _token: token },
            success: function (res) {
                if(res){

                    var html='<option value="all">All</option>';
                    $.each(res,function(key,value){
                        html += '<option value="'+key+'">'+value+'</option>';
                    });

                    $('#students_List').html(html);
                    $("#students_List").selectpicker('refresh');
                }else{
                    $('#students_List').html('<option value="">Select Student</option>');
                    $("#students_List").selectpicker('refresh');
                }
            }
        });
    }else{
        $('#attendanceStudent').hide();

        $('#studentsList').html('No Student');
    }

});


$('body').on('change', '#class_Student', function(){

    var class_id = $(this).val();
    var session_id = $('select[name=session_id]').val();
    var isAttendance = false;
    if($(document).find('.attendance-report-container').length){
        isAttendance = true;
    }

    if(class_id!='' && session_id !=''){
        var token = $('input[name="_token"]').val();

        $.ajax({
            type: 'POST',
            url: '/admin/getstudents',
            dataType: "json",
            data: { class_id: class_id,session_id:session_id, _token: token, isAttendance: isAttendance },
            success:function(res){
                if(res){

                    var html='<option value="all">All</option>';
                    $.each(res,function(key,value){
                        html += '<option value="'+key+'">'+value+'</option>';
                    });

                    $('#students_List').html(html);
                    $("#students_List").selectpicker('refresh');
                }else{

                    $('#students_List').html('<option value="">Select Student</option>');
                    $("#students_List").selectpicker('refresh');

                }
            },error:function(err){

            }
        });
    }else{

        $('#students_List').html('<option value="">Select Student</option>');
        $("#students_List").selectpicker('refresh');

    }

});


$(document).on('click', '.checkinTime', function(e){
    e.preventDefault();
    var TimeUp = $(this).parent();
    var checkInTimepickerValue = $(this).parent().find('.attendance_time').val();
    if(checkInTimepickerValue != '') {
        TimeUp.html('<input type="hidden" value="' + checkInTimepickerValue + '" name="checkInTime[]"/>' + checkInTimepickerValue)
    }
    else {
        $.ajax({
            type: 'GET',
            url: '/admin/currentTime',
            dataType: "json",
            success: function (result) {
                TimeUp.html('<input type="hidden" value="' + result.time + '" name="checkInTime[]"/>' + result.time)
            }
        });
    }

    return false;

});

$(document).on('click', '.checkoutTime', function(e){
    e.preventDefault();
    var TimeUp = $(this).parent();
    var checkOutTimepickerValue = $(this).parent().find('.attendance_time').val();
    if(checkOutTimepickerValue != '') {
        TimeUp.html('<input type="hidden" value="' + checkOutTimepickerValue + '" name="checkOutTime[]"/>' + checkOutTimepickerValue)
    }
    else {
        $.ajax({
            type: 'GET',
            url: '/admin/currentTime',
            dataType: "json",
            success: function (result) {
                TimeUp.html('<input type="hidden" value="' + result.time + '" name="checkOutTime[]"/>' + result.time)
            }
        });
    }

    return false;

});
