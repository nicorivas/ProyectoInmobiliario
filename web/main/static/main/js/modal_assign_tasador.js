function btn_assign_tasador_modal() {
  // Open the modal to assign tasadores.
  $(".btn_assign_tasador_modal").unbind()
  $(".btn_assign_tasador_modal").off()
  $(".btn_assign_tasador_modal").on("click", function (event) {
    console.log('holi')
    // Assigns to a hidden input in the tasador modal the value of the
    // appraisal, to have in the post request.
    var url = ajax_assign_tasador_modal_url
    var appraisal_id = $(this).val();
    $("#modal_assign_tasador").find("#ld-alert").show();
    $("#modal_assign_tasador").find("#table").hide();
    $("#modal_assign_tasador").find("#tasador_buscar").hide();
    $("#modal_assign_tasador").modal('show');
    $.ajax({
      url: url,
      type: 'get',
      data: {'appraisal_id':appraisal_id},
      error: function () {
        alert("Error al desplegar modal de tasador.");
        $("#modal_assign_tasador").modal('hide');
        return false;
      },
      success: function (data) {
        $("#modal_assign_tasador").html(data)
        $("#modal_assign_tasador").find("#ld-alert").hide();
        $("#modal_assign_tasador").find("#tasador_buscar").show();
        $("#modal_assign_tasador").find("#table").show();
        $('#modal_assign_tasador_appraisal_id').val(appraisal_id);
        assignTableActions();
      }
    });
  });
}

function btn_assign_tasador() {
  $("#btn_assign_tasador").unbind()
  $("#btn_assign_tasador").off()
  $("#btn_assign_tasador").on("click", function (event) {
    // Button clicked in the modal. Call an AJAX to assign a tasador
    // to the appraisal, and returns the 'not_accepted' table back,
    // to be replaced.
    var url = ajax_assign_tasador_url
    var appraisal_id = $('#modal_assign_tasador_appraisal_id').val();
    var formData = $('#form_assign_tasador').serialize();
    btn = $(this)
    btn.addClass('running')
    btn.prop('disabled', true);
    $.ajax({
      url: url,
      type: 'post',
      data: formData,
      error: function () {
        alert("Error al asignar tasador.");
        btn.removeClass('running')
        btn.prop('disabled', false);
        return false;
      },
      success: function (data) {
        removeRow("table_not_assigned",appraisal_id)
        replaceTable("table_not_accepted",data)
        assignTableActions()
        $("#modal_assign_tasador").modal('hide')
        btn.removeClass('running')
        btn.prop('disabled', false);
      }
    });
  });
}