function search_appraisals(field,val) {
  val = val.toLowerCase()
  if (!val) {
    return
  }
  var row_class = ["tr.not_assigned","tr.not_accepted","tr.in_appraisal","tr.finished"];
  for (var i=0; i<row_class.length; i++) {
    $(row_class[i]).each(function() {
      var field_value = $(this).find("."+field).html().trim();
      console.log(field_value)
      field_value = field_value.toLowerCase()
      if (field_value.indexOf(val) < 0) {
        $(this).hide()
      }
    });
  }
}

function search_all() {
  $("tr.not_assigned").each(function() {
    $(this).show()
  })
  $("tr.not_accepted").each(function() {
    $(this).show()
  })
  $("tr.in_appraisal").each(function() {
    $(this).show()
  })
  $("tr.finished").each(function() {
    $(this).show()
  })
  val = $("#buscar_id").val()
  search_appraisals('id',val)
  val = $("#buscar_solicitante").val()
  search_appraisals('solicitante',val)
  val = $("#buscar_solicitanteCodigo").val()
  search_appraisals('solicitanteCodigo',val)
  val = $("#buscar_address").val()
  search_appraisals('address',val)
  val = $("#buscar_tasador").val()
  search_appraisals('tasador',val)
  val = $("#buscar_visador").val()
  search_appraisals('visador',val)
}
$("#buscar_id").on('keyup',function() {
  search_all()
})
$("#buscar_solicitante").on('keyup',function() {
  search_all()
})
$("#buscar_solicitante").on('change',function() {
  search_all()
})
$("#buscar_solicitanteCodigo").on('keyup',function() {
  search_all()
})
$("#buscar_solicitanteCodigo").on('change',function() {
  search_all()
})
$("#buscar_address").on('keyup',function() {
  search_all()
})
$("#buscar_address").on('change',function() {
  search_all()
})
$("#buscar_tasador").on('keyup',function() {
  search_all()
})
$("#buscar_tasador").on('change',function() {
  search_all()
})
$("#buscar_visador").on('keyup',function() {
  search_all()
})
$("#buscar_visador").on('change',function() {
  search_all()
})