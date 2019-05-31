function btn_assign_visador() {
  $("#btn_assign_visador").unbind()
  $("#btn_assign_visador").off()
  $("#btn_assign_visador").on("click", function (event) {
    // Button clicked in the modal. Call an AJAX to assign a visador
    // to the appraisal, and returns the 'not_assigned' table back,
    // to be replaced.
    console.log("data",$('#modal_assign_visador').data())
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

  $(".visador_radio").on("click", function () {
    $("#modal_assign_visador").find("#alert_already_chosen").hide()
  })
}
    
btn_assign_visador();