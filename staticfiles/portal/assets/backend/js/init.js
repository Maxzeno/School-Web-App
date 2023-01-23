$(document).ajaxComplete(function() {
	$('[data-toggle="tooltip"]').tooltip();
});

function initDataTable(tableId) {
	$("#"+tableId).DataTable({
		keys: !0,
		language: {
			paginate: {
				previous: "<i class='mdi mdi-chevron-left'>",
				next: "<i class='mdi mdi-chevron-right'>"
			}
		},
		drawCallback: function() {
			$(".dataTables_paginate > .pagination").addClass("pagination-rounded");
		},
		"fnRowCallback": function (nRow, aData, iDisplayIndex) {
		    var info = $(this).DataTable().page.info();
		    $("td:nth-child(1)", nRow).html(info.start + iDisplayIndex + 1);
		    return nRow;
		}
	});
}

// For initializing multiple datatables
function initDataTables(tableIds) {
	for(i = 0; i < tableIds.length; i++){
		$(tableIds[i]).DataTable({
			keys: !0,
			language: {
				paginate: {
					previous: "<i class='mdi mdi-chevron-left'>",
					next: "<i class='mdi mdi-chevron-right'>"
				}
			},
			drawCallback: function() {
				$(".dataTables_paginate > .pagination").addClass("pagination-rounded")
			}
		});
	}
}

function initDateRangePicker(ids) {
	for(i = 0; i < ids.length; i++){
		$(ids[i]).daterangepicker({
			locale: {
				format: 'D/MM/Y'
			}
		});
	}

}

function initDatePicker(ids) {
	for(i = 0; i < ids.length; i++){
		$(ids[i]).datepicker({
			locale: {
				format: 'D/MM/Y'
			}
		});
	}

}

function initSelect2(ids) {
	for(i = 0; i < ids.length; i++){
		$(ids[i]).select2();
	}
}

function initTimepicker() {
	var defaultOptions = {
		"showSeconds": true,
		"icons": {
			"up": "mdi mdi-chevron-up",
			"down": "mdi mdi-chevron-down"
		}
	};

	// time picker
	$('[data-toggle="timepicker"]').each(function (idx, obj) {
		var objOptions = $.extend({}, defaultOptions, $(obj).data());
		$(obj).timepicker(objOptions);
	});
}

function initSummerNote(ids) {
	for(i = 0; i < ids.length; i++){
		! function(o) {
			"use strict";
			var e = function() {
				this.$body = o("body")
			};
			e.prototype.init = function() {
				o(ids[i]).summernote({
					placeholder: "",
					height: 230,
					callbacks: {
						onInit: function(e) {
							o(e.editor).find(".custom-control-description").addClass("custom-control-label").parent().removeAttr("for")
						}
					},
				});
			}, o.Summernote = new e, o.Summernote.Constructor = e
		}(window.jQuery),
		function(o) {
			"use strict";
			o.Summernote.init()
		}(window.jQuery);
	}
}

function changeTitleOfImageUploader(photoElem) {
	var fileName = $(photoElem).val().replace(/C:\\fakepath\\/i, '');
	$(photoElem).siblings('label').text(fileName);
}

function initImageUpload(box) {
	let uploadField = box.querySelector('.image-upload');

	uploadField.addEventListener('change', getFile);

	function getFile(e){
		let file = e.currentTarget.files[0];
		checkType(file);
	}

	function previewImage(file){
		let thumb = box.querySelector('.js--image-preview'),
		reader = new FileReader();
		reader.onload = function() {
			thumb.style.backgroundImage = 'url(' + reader.result + ')';
		}
		reader.readAsDataURL(file);
		thumb.className += ' js--no-default';
	}

	function checkType(file){
		let imageType = /image.*/;
		if (!file.type.match(imageType)) {
			throw 'Datei ist kein Bild';
		} else if (!file){
			throw 'Kein Bild gewählt';
		} else {
			previewImage(file);
		}
	}

}

// initialize box-scope
var boxes = document.querySelectorAll('.box');

for (let i = 0; i < boxes.length; i++) {
	let box = boxes[i];
	initDropEffect(box);
	initImageUpload(box);
}



/// drop-effect
function initDropEffect(box){
	let area, drop, areaWidth, areaHeight, maxDistance, dropWidth, dropHeight, x, y;

	// get clickable area for drop effect
	area = box.querySelector('.js--image-preview');
	area.addEventListener('click', fireRipple);

	function fireRipple(e){
		area = e.currentTarget
		// create drop
		if(!drop){
			drop = document.createElement('span');
			drop.className = 'drop';
			this.appendChild(drop);
		}
		// reset animate class
		drop.className = 'drop';

		// calculate dimensions of area (longest side)
		areaWidth = getComputedStyle(this, null).getPropertyValue("width");
		areaHeight = getComputedStyle(this, null).getPropertyValue("height");
		maxDistance = Math.max(parseInt(areaWidth, 10), parseInt(areaHeight, 10));

		// set drop dimensions to fill area
		drop.style.width = maxDistance + 'px';
		drop.style.height = maxDistance + 'px';

		// calculate dimensions of drop
		dropWidth = getComputedStyle(this, null).getPropertyValue("width");
		dropHeight = getComputedStyle(this, null).getPropertyValue("height");

		// calculate relative coordinates of click
		// logic click coordinates relative to page - parent's position relative to page - half of self height/width to make it controllable from the center
		x = e.pageX - this.offsetLeft - (parseInt(dropWidth, 10)/2);
		y = e.pageY - this.offsetTop - (parseInt(dropHeight, 10)/2) - 30;

		// position drop and animate
		drop.style.top = y + 'px';
		drop.style.left = x + 'px';
		drop.className += ' animate';
		e.stopPropagation();

	}
}


function initImagePreviewer() {
	var boxes = document.querySelectorAll('.box');

	for (let i = 0; i < boxes.length; i++) {
		let box = boxes[i];
		initDropEffect(box);
		initImageUpload(box);
	}
}


function checkRequiredFields() {
	var pass = 1;
	$('form.required-form').find('input, select').each(function(){
		if($(this).prop('required')){
			if ($(this).val() === "") {
				pass = 0;
			}
		}
	});

	if (pass === 1) {
		$('form.required-form').submit();
	}else {
		error_required_field();
	}
}

function initCustomFileUploader() {
	//Reference:
	//https://www.onextrapixel.com/2012/12/10/how-to-create-a-custom-file-input-with-jquery-css3-and-php/
	;(function($) {

		// Browser supports HTML5 multiple file?
		var multipleSupport = typeof $('<input/>')[0].multiple !== 'undefined',
		isIE = /msie/i.test( navigator.userAgent );

		$.fn.customFile = function() {

			return this.each(function() {

				var $file = $(this).addClass('custom-file-upload-hidden'), // the original file input
				$wrap = $('<div class="file-upload-wrapper">'),
				$input = $('<input type="text" class="file-upload-input" />'),
				// Button that will be used in non-IE browsers
				$button = $('<button type="button" class="file-upload-button">Select a File</button>'),
				// Hack for IE
				$label = $('<label class="file-upload-button" for="'+ $file[0].id +'">Select a File</label>');

				// Hide by shifting to the left so we
				// can still trigger events
				$file.css({
					position: 'absolute',
					left: '-9999px'
				});

				$wrap.insertAfter( $file )
				.append( $file, $input, ( isIE ? $label : $button ) );

				// Prevent focus
				$file.attr('tabIndex', -1);
				$button.attr('tabIndex', -1);

				$button.click(function () {
					$file.focus().click(); // Open dialog
				});

				$file.change(function() {

					var files = [], fileArr, filename;

					// If multiple is supported then extract
					// all filenames from the file array
					if ( multipleSupport ) {
						fileArr = $file[0].files;
						for ( var i = 0, len = fileArr.length; i < len; i++ ) {
							files.push( fileArr[i].name );
						}
						filename = files.join(', ');

						// If not supported then just take the value
						// and remove the path to just show the filename
					} else {
						filename = $file.val().split('\\').pop();
					}

					$input.val( filename ) // Set the value
					.attr('title', filename);

				});

				$input.on({
					blur: function() { $file.trigger('blur'); },
					keydown: function( e ) {
						if ( e.which === 13 ) { // Enter
							if ( !isIE ) { $file.trigger('click'); }
						} else if ( e.which === 8 || e.which === 46 ) { // Backspace & Del
							// On some browsers the value is read-only
							// with this trick we remove the old input and add
							// a clean clone with all the original events attached
							$file.replaceWith( $file = $file.clone( true ) );
							$file.trigger('change');
							$input.val('');
						} else if ( e.which === 9 ){ // TAB
							return;
						} else { // All other keys
							return false;
						}
					}
				});

			});

		};

		// Old browser fallback
		if ( !multipleSupport ) {
			$( document ).on('change', 'input.customfile', function() {

				var $this = $(this),
				// Create a unique ID so we
				// can attach the label to the input
				uniqId = 'customfile_'+ (new Date()).getTime(),
				$wrap = $this.parent(),

				// Filter empty input
				$inputs = $wrap.siblings().find('.file-upload-input')
				.filter(function(){ return !this.value }),

				$file = $('<input type="file" id="'+ uniqId +'" name="'+ $this.attr('name') +'"/>');

				// 1ms timeout so it runs after all other events
				// that modify the value have triggered
				setTimeout(function() {
					// Add a new input
					if ( $this.val() ) {
						// Check for empty fields to prevent
						// creating new inputs when changing files
						if ( !$inputs.length ) {
							$wrap.after( $file );
							$file.customFile();
						}
						// Remove and reorganize inputs
					} else {
						$inputs.parent().remove();
						// Move the input so it's always last on the list
						$wrap.appendTo( $wrap.parent() );
						$wrap.find('input').focus();
					}
				}, 1);

			});
		}

	}(jQuery));

	$('input[type=file]').customFile();

}
