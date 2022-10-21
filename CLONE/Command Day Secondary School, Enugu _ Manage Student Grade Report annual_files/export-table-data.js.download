/*Export Table Init*/

"use strict";


function updateDataTableSelectAllCtrl(table){
	// console.log(table);
	var $table = table.table().node();
  	var chkbox_all        = $('tbody input[type="checkbox"]', $table);
    var chkbox_checked    = $('tbody input[type="checkbox"]:checked', $table);
    var chkbox_select_all = $('thead input[type="checkbox"]', $table).get(0);
    // console.log(chkbox_all);
    // console.log(chkbox_checked);
   // If none of the checkboxes are checked
   if(chkbox_checked.length === 0){
      	chkbox_select_all.checked = false;
      	if('indeterminate' in chkbox_select_all){
         	chkbox_select_all.indeterminate = false;
      	}

   // If all of the checkboxes are checked
   } else if (chkbox_checked.length === chkbox_all.length){
      	chkbox_select_all.checked = true;
      	if('indeterminate' in chkbox_select_all){
         	chkbox_select_all.indeterminate = false;
      	}

   // If some of the checkboxes are checked
   } else {
      	chkbox_select_all.checked = true;
      	if('indeterminate' in chkbox_select_all){
         	chkbox_select_all.indeterminate = true;
      	}
   }
}


$(document).ready(function() {
	 var buttonCommon = {
        exportOptions: {
            format: {
                body: function ( data, row, column, node ) {
                    // Strip $ from salary column to make it numeric
                    return column === 3 ?
                        data.replace( /[$,]/g, '' ) :
                        data;
                }
            }
        }
    };

    $('#example5').DataTable( {

        dom: 'Bfrtip',
        buttons: [
            $.extend( true, {}, buttonCommon, {
                extend: 'copyHtml5'
            } ),
            $.extend( true, {}, buttonCommon, {
                extend: 'excelHtml5'
            } ),
            $.extend( true, {}, buttonCommon, {
                extend: 'pdfHtml5'
            } )
        ]
    } );
	// $.fn.dataTable.moment(["DD/MM", "MM-DD", true]);
	var table = $('#example').DataTable( {
		dom: 'Bfrtip',
		buttons: [
			'copy', 'csv', 'excel', 'pdf', 'print'
		],
		language: {
			"emptyTable": "No Records Available"
		},
		// fnDrawCallback: function(oSettings) {
	 //        if ($('#example tr').length < 11) {
	 //            $('.dataTables_paginate').hide();
	 //        }
	 //    }
	} );


	// remove pagination from edit permission page

	var table1 = $('#example2').DataTable( {
	  	"paging":   false,
		dom: 'Bfrtip',
		language: {
			"emptyTable": "No Records Available"
		},
		buttons: [
			'copy', 'csv', 'excel', 'pdf', 'print'
		],
		// fnDrawCallback: function(oSettings) {
	 //        if ($('#example tr').length < 11) {
	 //            $('.dataTables_paginate').hide();
	 //        }
	 //    }
	 } );


		var table2 = $('#currency_export').DataTable({

		dom: 'Bfrtip',
		'lengthChange': false,
			"columnDefs": [ {
				"targets": 0,
				"orderable": false
			} ],

		// fnDrawCallback: function(oSettings) {
	 //        if ($('#customExport tr').length < 11) {
	 //            $('.dataTables_paginate').hide();
	 //        }
	 //    },

		language: {
			"emptyTable": "No Records Available"
		},

		// buttons: [
		// 	'csv', 'excel', 'pdf', 'print'
		// ],

		buttons: [
		{
			extend: 'csv',
			footer: false,
			exportOptions: {
				columns: "thead th:not(.noExport)"
			}
		},
		{
			extend: 'excel',
			footer: false,
			exportOptions: {
				columns: "thead th:not(.noExport)"
			}
		},

		{
			extend: 'pdfHtml5',
			// orientation: 'landscape',
            // pageSize: 'LEGAL',
			footer: false,
			exportOptions: {
				columns: "thead th:not(.noExport)"
			},
			customize : function(doc){
	            var colCount = new Array();
	            var length = $("#currency_export").find('tbody tr:first-child td').length ;
	            var perSize = 800/length;

	            $("#currency_export").find('tbody tr:first-child td').each(function(){

	                	colCount.push(perSize);

	            });
	            doc.content[1].table.widths = colCount;
	           doc.styles.tableHeader.alignment="left";
	        }
		},
		{
			extend: 'print',
			footer: false,
			exportOptions: {
				columns: "thead th:not(.noExport)"
			}
		}

		]
	});


	var table2 = $('#customExport').DataTable({
		dom: 'Bfrtip',
		'lengthChange': false,
			"columnDefs": [ {
				"targets": 0,
				"orderable": false
			} ],

		// fnDrawCallback: function(oSettings) {
	 //        if ($('#customExport tr').length < 11) {
	 //            $('.dataTables_paginate').hide();
	 //        }
	 //    },

		language: {
			"emptyTable": "No Records Available"
		},

		// buttons: [
		// 	'csv', 'excel', 'pdf', 'print'
		// ],

		buttons: [
		{
			extend: 'csv',
			footer: false,
			exportOptions: {
				columns: "thead th:not(.noExport)"
			}
		},
		{
			extend: 'excel',
			footer: false,
			exportOptions: {
				columns: "thead th:not(.noExport)"
			}
		},

		{
			extend: 'pdfHtml5',
			orientation: 'landscape',
            // pageSize: 'LEGAL',
			footer: false,
			exportOptions: {
				columns: "thead th:not(.noExport)"
			},
			customize : function(doc){
				/*console.log(doc);
	            var colCount = new Array();
	            var length = $("#customExport").find('tbody tr:first-child td').length ;
	            var perSize = 550/length;
	            var temp = 0;
	            $("#customExport").find('tbody tr:first-child td').each(function(){
	                if(temp!=0 && temp != 9){
	                	colCount.push(perSize);
	                }else if(temp == 9){
	                	colCount.push(perSize+25);
	                }
	                else{
	                	colCount.push(15);
	                }
	                temp++;
	            });
	            doc.content[1].table.widths = colCount;*/

	        }
		},
		{
			extend: 'print',
			footer: false,
			exportOptions: {
				columns: "thead th:not(.noExport)"
			}
		}

		]
    });


    //virtual classroom table
    //copied from above table
    var virtualClassroomTable = $('#virtualClassroomTable').DataTable({

		dom: 'Bfrtip',
		'lengthChange': false,
			"columnDefs": [ {
				"targets": 0,
				"orderable": false
			} ],

		// fnDrawCallback: function(oSettings) {
	 //        if ($('#customExport tr').length < 11) {
	 //            $('.dataTables_paginate').hide();
	 //        }
	 //    },

		language: {
			"emptyTable": "No Records Available"
		},



		buttons: []
	});


	var table5 = $('#customExportAttendance').DataTable({

		dom: 'Blfrtip',
		'lengthChange': false,
			"columnDefs": [ {
				"targets": 0,
				"orderable": false
			} ],



		language: {
			"emptyTable": "No Records Available"
		},


		buttons: [
		{
			extend: 'csv',
			footer: false,
			/*exportOptions: {
				columns: "thead th:not(.noExport)"
			}*/
		},
		{
			extend: 'excel',
			footer: false,
			/*exportOptions: {
				columns: "thead th:not(.noExport)"
			}*/
		},
		{
			extend: 'pdfHtml5',
			orientation: 'landscape',
            pageSize: 'A0'
			/*exportOptions: {
				columns: "thead th:not(.noExport)"
			}*/
		}

		]
	});

	var table = $('#customExportGrade').DataTable({

		dom: 'Blfrtip',
		'lengthChange': false,
			"columnDefs": [ {
				"targets": 0,
				"orderable": false
			} ],



		language: {
			"emptyTable": "No Records Available"
		},


		buttons: [
		{
			extend: 'csv',
			footer: false,
			/*exportOptions: {
				columns: "thead th:not(.noExport)"
			}*/
		},
		{
			extend: 'excel',
			footer: false,
			/*exportOptions: {
				columns: "thead th:not(.noExport)"
			}*/
		},
		{
			extend: 'pdfHtml5',
			orientation: 'landscape',
            pageSize: 'A0'
			/*exportOptions: {
				columns: "thead th:not(.noExport)"
			}*/
		}

		]
	});

	var table4 = $('#schoolList').DataTable({
		"iDisplayLength": 100,
		dom: 'Blfrtip',
		'lengthChange': false,


			"columnDefs": [ {

				"targets": 0,
				"orderable": false
			} ],

		// fnDrawCallback: function(oSettings) {
	 //        if ($('#example tr').length < 11) {
	 //            $('.dataTables_paginate').hide();
	 //        }
	 //    },

		language: {
			"emptyTable": "No Records Available"
		},

		// buttons: [
		// 	'csv', 'excel', 'pdf', 'print'
		// ],

		buttons: [
		{
			extend: 'csv',
			type: 'string',

			footer: false,
			exportOptions: {
				columns: "thead th:not(.noExport)"
			}
		},
		{
			extend: 'excel',
			footer: false,
			exportOptions: {
				columns: "thead th:not(.noExport)"
			}
		},
		{
			extend: 'pdf',
			 orientation: 'landscape',
                pageSize: 'LEGAL',
			footer: false,
			exportOptions: {
				columns: "thead th:not(.noExport)"
			}
		},
		{
			extend: 'print',
			footer: false,
			exportOptions: {
				columns: "thead th:not(.noExport)"
			}
		}

		]
	});
// 	$('#example').DataTable( {
//   dom: 'Bfrtip',
//   buttons: [{
//    extend: 'pdfHtml5',
//    title: 'My title' + '\n' + 'a new line',
//    customize: function(doc) {
//      doc.styles.title = {
//        color: 'red',
//        fontSize: '40',
//        background: 'blue',
//        alignment: 'center'
//      }
//    }
//  }]
// })

	var table8 = $('#reportList').DataTable({
		 // "paging": true,
		"iDisplayLength": 100,
		dom: 'Blfrtip',
		'lengthChange': false,


			"columnDefs": [ {

				"targets": 0,
				"orderable": false
			} ],

		// fnDrawCallback: function(oSettings) {
	 //        if ($('#example tr').length < 11) {
	 //            $('.dataTables_paginate').hide();
	 //        }
	 //    },

		language: {
			"emptyTable": "No Records Available"
		},

		// buttons: [
		// 	'csv', 'excel', 'pdf', 'print'
		// ],

		buttons: [
		// {
		// 	extend: 'csv',
		// 	footer: false,
		// 	exportOptions: {
		// 		columns: "thead th:not(.noExport)"
		// 	}
		// },
		{
			extend: 'excel',
			footer: false,
			exportOptions: {
				columns: "thead th:not(.noExport)"
			}
		},
		{
			extend: 'pdf',
			 orientation: 'landscape',
                pageSize: 'LEGAL',
			footer: false,
			exportOptions: {
				columns: "thead th:not(.noExport)"
			},
			customize: function(pdfDocument) {
	            pdfDocument.content[1].table.headerRows = 2;
	            var firstHeaderRow = [];
	            $('#reportList').find("thead>tr:first-child>th").each(
	              function(index, element) {
	                var colSpan = element.getAttribute("colSpan");
	                firstHeaderRow.push({
	                  text: element.innerHTML != '&nbsp;' ? element.innerHTML :"" ,
	                  style: "tableHeader",
	                  colSpan: colSpan
	                });
	                for (var i = 0; i < colSpan - 1; i++) {
	                  firstHeaderRow.push({});
	                }
	              });
	            pdfDocument.content[1].table.body.unshift(firstHeaderRow);

	          }
		},
		{
			extend: 'print',
			footer: false,
			exportOptions: {
				columns: "thead th:not(.noExport)"
			}
		}

		]
	});

	var table3 = $('#customReportExport').DataTable({
		'paging'      : false,
		'lengthChange': false,
		'searching'   : true,
		'ordering'    : true,
		'info'        : true,
		'autoWidth'   : true,
	    // 'searching'   : false,
     	'bInfo'       : false ,
     	// "ordering": false,
		"columnDefs": [
		{ "orderable": false, "targets": 0 }
		],
		language: {
			"emptyTable": "No Records Available"
		},
		fnDrawCallback: function(oSettings) {
	        if ($('#example tr').length < 11) {
	            $('.dataTables_paginate').hide();
	        }
	    },
		dom: 'Bfrtip',

		// buttons: [
		// 	'csv', 'excel', 'pdf', 'print'
		// ]
		 // buttons: [
   //          {
   //              extend: 'pdfHtml5',
   //              orientation: 'landscape',
   //              pageSize: 'LEGAL'
   //          }
   //      ]



	});


	var gradeTable = $('#gradecustomExport').DataTable({
		dom: 'Blfrtip',
		"paging":   false,
		'lengthChange': false,
			"columnDefs": [ {
				"targets": 0,
				"orderable": false
			} ],
		language: {
			"emptyTable": "No Records Available"
		},
		buttons: [
		{
			extend: 'csv',
			footer: false,
			exportOptions: {
				columns: "thead th:not(.noExport)"
			}
		},
		{
			extend: 'excel',
			footer: false,
			exportOptions: {
				columns: "thead th:not(.noExport)"
			}
		},
		{
			extend: 'pdfHtml5',
			orientation: 'landscape',
            pageSize: 'LEGAL',
			footer: false,
			exportOptions: {
				columns: "thead th:not(.noExport)"
			}
		},
		{
			extend: 'print',
			footer: false,
			exportOptions: {
				columns: "thead th:not(.noExport)"
			}
		}

		]
	});
	$('#gradecustomExport_info').hide();
	$('#gradecustomExport_filter').hide();

	var timetable_lectures = $('#customFields_timetable').DataTable({
		dom: 'Blfrtip',
		"paging":   false,
		'lengthChange': false,
			"columnDefs": [ {
				"targets": 0,
				"orderable": false
			} ],
		language: {
			"emptyTable": "No Records Available"
		},
		buttons: [
		{
			extend: 'csv',
			footer: false,
			exportOptions: {
				columns: "thead th:not(.noExport)"
			}
		},
		{
			extend: 'excel',
			footer: false,
			exportOptions: {
				columns: "thead th:not(.noExport)"
			}
		},
		{
			extend: 'pdfHtml5',
			orientation: 'landscape',
            pageSize: 'LEGAL',
			footer: false,
			exportOptions: {
				columns: "thead th:not(.noExport)"
			}
		},
		{
			extend: 'print',
			footer: false,
			exportOptions: {
				columns: "thead th:not(.noExport)"
			}
		}

		]
	});

	if($('#timetable-view').length >0){
        $('#timetable-view').DataTable({
          'paging'      : false,
          'lengthChange': false,
          'searching'   : false,
          'ordering'    : false,
          'info'        : false,
          'autoWidth'   : true,
          dom: 'Blfrtip'
    //         buttons: [
    //             {
    //                extend: 'csv',
    //                footer: false

    //             },
    //             {
    //                extend: 'excel',
    //                footer: false
    //             },
				// {
				// 	extend: 'print',
				// 	footer: false,
				// 	exportOptions: {
				// 		columns: "thead th:not(.noExport)"
				// 	}
				// },
				// {
				// 	extend: 'pdfHtml5',
				// 	orientation: 'landscape',
		  //           pageSize: 'LEGAL',
				// 	footer: false,
				// 	exportOptions: {
				// 		columns: "thead th:not(.noExport)"
				// 	}
				// }
    //         ]
        });
    }

	table.on('draw', function(){
			// Update state of "Select all" control
			updateDataTableSelectAllCtrl(table);
	});

	table1.on('draw', function(){
			// Update state of "Select all" control
			updateDataTableSelectAllCtrl(table);
	});

	table2.on('draw', function(){
			// Update state of "Select all" control
			updateDataTableSelectAllCtrl(table);
	});

	table3.on('draw', function(){
			// Update state of "Select all" control
			updateDataTableSelectAllCtrl(table);
	});

	$('table th input[type="checkbox"]').click(function(event) {  //on click
	    var checked = this.checked;
	    example.column(0).nodes().to$().each(function(index) {
	        if (checked) {
	            $(this).find('input[type="checkbox"]').prop('checked', 'checked');
	        } else {
	            $(this).find('input[type="checkbox"]').removeProp('checked');
	        }
	    });
    });


} );
