function btn_assign_visador() {
  
  $("#btn_assign_visador").unbind()
  $("#btn_assign_visador").off()
  $("#btn_assign_visador").on("click", function (event) {
    // Button clicked in the modal. Call an AJAX to assign a visador
    // to the appraisal, and returns the 'not_assigned' table back,
    // to be replaced.
    var source_table = $('#modal_assign_visador').data("parent");
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

  $("#btn_unassign_visador").unbind()
  $("#btn_unassign_visador").off()
  $("#btn_unassign_visador").on("click", function (event) {
    // Button clicked in the modal. Call an AJAX to assign a visador
    // to the appraisal, and returns the 'not_assigned' table back,
    // to be replaced.
    btn = $(this)
    btn_loading(btn)
    data = {}
    data["appraisal_id"] = $('#modal_assign_visador').data("appraisal_id");
    data["parent"] = $('#modal_assign_visador').data("parent");
    data["current_visador_id"] = $("#modal_assign_visador_appraisal_visador_id").val();
    $("#modal_assign_visador").find("#alert_already_chosen").hide()
    var url = ajax_unassign_visador_url;
    $.ajax({
      url: url,
      type: 'get',
      data: data,
      error: function (ret) {
        btn_idle(btn)
        if ("alert" in data.responseJSON) {
          $("#modal_assign_visador").find("#alert_message").html(data.responseJSON["alert"])
          $("#modal_assign_visador").find("#alert").show()
        } else {
          alert("Error al desasignar visador.");
        }
        return false;
      },
      success: function (ret) {
        btn_idle(btn)
        replaceRow(data["parent"],data["appraisal_id"],ret)
        assignTableActions()
        $("#modal_assign_visador").find("#"+data["current_visador_id"]).removeClass("selected")
        $("#modal_assign_visador").find("#"+data["current_visador_id"]+" input").removeAttr('checked');
      }
    });
  });

  $(".visador_radio").on("click", function () {
    $("#modal_assign_visador").find("#alert_already_chosen").hide()
  })
}
    
btn_assign_visador();