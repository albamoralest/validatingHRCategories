/**
 * 
 */
$(document).ready(function () {
  $("#table_informative").DataTable({
	  "order": [[ 3, "desc" ]],
	  "lengthChange": false,
	  "pageLength": 10
  });
  
  $("#table_distinct").DataTable({
	  "order": [[ 3, "desc" ]],
	  "lengthChange": false,
	  "pageLength": 10
  });
  
  $("#table_details").DataTable({
	  "lengthChange": false,
	  "paging":   false,
      "ordering": false,
      "searching": false,
      "info": false
  });
  
  $("#table_results").DataTable({
	  "lengthChange": false,
	  "pageLength": 25
  });
  console.log( "ready!" );
});