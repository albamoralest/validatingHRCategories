/**
 * 
 */
$.extend( true, $.fn.dataTable.defaults, {
    "searching": false
} );
$(document).ready(function () {
  $("#table_informative").DataTable({
	  "orderFixed": [[ 3, "desc" ]],
	  "lengthChange": false,
	  "pageLength": 5
  });
  console.log( "ready!" );
});