function search_appraisals(table_id,field,val) {
  if (!val || val == "") {
    return
  }
  val = val.toLowerCase()
  // Cycle through all appraisal fields of table
  $('#'+table_id+' tr.appraisal').each(function() {
    var field_value = $(this).find("."+field).html().trim();
    field_value = field_value.toLowerCase()
    if (field_value.indexOf(val) < 0) {
      $(this).hide()
    }
  });
}

function search_all(input) {
  // First show all rows (and then hide them)
  $("tr.appraisal").each(function() {
    $(this).show()
  })
  // Cycle through all search fields of the current table
  table = input.closest('table')
  table_id = table.attr('id')
  table.find('input.search').each(function(index) {
    // Field that this search field corresponds to
    field = $(this).data('field')
    // Value of current search field is key to search for
    key = $(this).val()
    search_appraisals(table_id,field,key)
  })
}

$("input.search").on('keyup change',function() {
  search_all($(this))
})