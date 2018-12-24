function btn_assign_visador_modal() {
  $(".btn_assign_visador_modal").unbind()
  $(".btn_assign_visador_modal").off()
  $(".btn_assign_visador_modal").on("click", function (event) {
    // Assigns to a hidden input in the tasador modal the value of the
    // appraisal, to have in the post request.
    var url = ajax_assign_visador_modal_url;
    var appraisal_id = $(this).val();
    var source_table = $(this).closest('table').attr('id');
    $("#modal_assign_visador").find("#ld-alert").show();
    $("#modal_assign_visador").find("#table").hide();
    $("#modal_assign_visador").find("#visador_buscar").hide();
    $("#modal_assign_visador").find("#alert_already_chosen").hide()
    $("#modal_assign_visador").modal('show');
    $.ajax({
      url: url,
      type: 'get',
      data: {'appraisal_id':appraisal_id},
      error: function () {
        alert("Error al desplegar modal de visador.");
        $("#modal_assign_visador").modal('hide');
        return false;
      },
      success: function (data) {
        $("#modal_assign_visador").html(data)
        $("#modal_assign_visador").find("#ld-alert").hide();
        $("#modal_assign_visador").find("#table").show();
        $("#modal_assign_visador").find("#visador_buscar").show();
        $("#modal_assign_visador_appraisal_id").val(appraisal_id);
        $("#modal_assign_visador_source_table").val(source_table);
        assignTableActions();
      }
    });
  });
}

function btn_assign_visador() {
  $("#btn_assign_visador").unbind()
  $("#btn_assign_visador").off()
  $("#btn_assign_visador").on("click", function (event) {
    // Button clicked in the modal. Call an AJAX to assign a visador
    // to the appraisal, and returns the 'not_assigned' table back,
    // to be replaced.
    var source_table = $('#modal_assign_visador_source_table').val();
    var url = ajax_assign_visador_url;
    var formData = $('#form_assign_visador').serialize();
    var current_visador_id = $("#modal_assign_visador_appraisal_visador_id").val();
    if ($("input:checked").val() == current_visador_id) {
      $("#modal_assign_visador").find("#alert_already_chosen").show()
    } else {
      $("#modal_assign_visador").find("#alert_already_chosen").hide()
      $(this).addClass('running')
      $(this).prop('disabled', true);
      $.ajax({
        url: url,
        type: 'post',
        data: formData,
        error: function () {
          alert("Error al asignar visador.");
          $(this).removeClass('running')
          $(this).prop('disabled', false);
          return false;
        },
        success: function (data) {
          replaceTable(source_table,data)
          assignTableActions()
          $("#modal_assign_visador").modal('hide')
          $("#modal_assign_visador").find("#btn_assign_visador").removeClass('running')
          $("#modal_assign_visador").find("#btn_assign_visador").prop('disabled', false);
        }
      });  
    }
  });
}