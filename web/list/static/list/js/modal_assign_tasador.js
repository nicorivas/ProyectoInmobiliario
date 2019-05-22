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
        if ("alert" in data) {
          $("#modal_assign_tasador").find("#alert_message").html(data["error"])
          $("#modal_assign_tasador").find("#alert").show()
          btn.removeClass('running')
          btn.prop('disabled', false);
        } else {
          removeRow("table_not_assigned",appraisal_id)
          replaceTable("table_not_accepted",data)
          assignTableActions()
          $("#modal_assign_tasador").modal('hide')
          btn.removeClass('running')
          btn.prop('disabled', false);
        }
      }
    });
  });
}

function btn_unassign_tasador() {
  $("#btn_unassign_tasador").unbind()
  $("#btn_unassign_tasador").off()
  $("#btn_unassign_tasador").on("click", function (event) {
    // Button clicked in the modal. Call an AJAX to unassign the tasador
    // of the appraisal, and returns the 'not_assigned' table back,
    // to be replaced.
    event.preventDefault()
    var appraisal_id = $('#modal_assign_tasador_appraisal_id').val();
    var url = ajax_unassign_tasador_url
    btn = $(this);
    btn.addClass('running');
    btn.prop('disabled', true);
    $.ajax({
      url: url,
      type: 'get',
      data: {'appraisal_id':appraisal_id},
      error: function () {
        alert("Error al desasignar tasador.");
        return false;
      },
      success: function (data) {
        btn.removeClass('running');
        btn.prop('disabled', false);
        removeRow("active",appraisal_id)
        replaceTable("not_assigned",data)
        assignTableActions()
        $("#modal_unassign_tasador").modal('hide')
      }
    });
  });
}

btn_assign_tasador()
btn_unassign_tasador()
