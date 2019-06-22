function buttonLogbookClick(event) {
  event.preventDefault();
  btn = $(this)
  table = btn.data('table')
  tr = $(this).closest('tr')
  $("#modal_logbook").data('table',table)
  appraisal_id = btn.val(); // button has id of appraisal
  btn_loading(btn)
  // ajax
  var url = ajax_logbook_url
  $.ajax({
    url: url,
    type: 'get',
    data: {'appraisal_id':appraisal_id,'table':table},
    error: function () {
        alert("Error al abrir la bitacora.");
        return false;
    },
    success: function (data) {
      $('#modal_logbook').html($.trim(data));
      $("#in_appraisal_id").val(appraisal_id); // hidden input
      $("input#table_id").attr("value",table);
      tr.removeClass("notification")
      $('#modal_logbook').modal('show');
      if (table == "not_accepted") {
        $('#modal_logbook').find('#div_event').hide()
        $('#modal_logbook').find('#div_comment_btn').hide()
        $('#modal_logbook').find('#div_datetime').hide()
        $('#modal_logbook').find('#div_accept_reject').show()
      }
      if (table == "archive") {
        $('#modal_logbook').find('#logbook_flow').hide()
        $('#modal_logbook').find('#logbook_event').hide()
      }
    },
    complete: function (data) {
      btn_idle(btn)
      assignLogbookModalActions();
      if (table != "not_accepted") {
        $("#id_event").trigger("change")
      }
    }
  });
}

function logbookClose(event) {
  // When the logbook modal is closed, we delete the notifications
  // related to this appraisal. We also save the form.
  console.log("logbookClose")
  var appraisal_id = $("#in_appraisal_id").val();
  var url = ajax_logbook_close_url
  var form = $('#logbook_form')
  $.ajax({
    url: url,
    type: 'post',
    data: form.serialize(),
    error: function () {
        alert("Error al cerrar la bitacora.");
        return false;
    },
    success: function (data) {
      // everything is done in the view
    },
    complete: function (data) {
      // everything is done in the view
    }
  });
  return false;
}

function assignLogbookModalActions() {

  $("#id_event").unbind()
  $("#id_event").off()
  $("#id_event").on("change", function (event) {
    $("#div_datetime").slideUp()
    $("#div_warning_entregada").slideUp()
    $("#div_warning_incidencia").slideUp()
    if ($(this).val() == comment_class['EVENT_VISITA_ACORDADA']) {
      $("#div_datetime").slideDown()
      $("#id_datetime").val('')
    } else if ($(this).val() == comment_class['EVENT_PROPIEDAD_VISITADA']) {
      $("#div_datetime").slideDown()
      var date = new Date().toLocaleDateString('es-CL').replace(/-/g,'/');
      var time = new Date().toLocaleTimeString('es-CL', { hour12: false, hour: "numeric", minute: "numeric"});
      $("#id_datetime").val(date+' '+time)
    } else if ($(this).val() == comment_class['EVENT_ENTREGADO_AL_CLIENTE']) {
      $("#div_datetime").slideUp()
      $("#div_warning_entregada").slideDown()
    } else if ($(this).val() == comment_class['EVENT_INCIDENCIA']) {
      $("#div_datetime").slideUp()
      $("#div_warning_incidencia").slideDown()
    } else {
      $("#div_datetime").slideUp()
      $("#div_warning_entregada").slideUp()
      $("#div_warning_incidencia").slideUp()
    }
  })

  $("#btn_comment").unbind()
  $("#btn_comment").off()
  $("#btn_comment").on("click", function (event) {
    // Click of comment button in comment form.
    event.preventDefault();
    btn = $(this)
    btn_loading(btn,hide_text=true)
    var form = document.getElementById('form_comment');
    var formData = new FormData(form);
    var url = $("#form_comment").attr("data-comment-url");
    var appraisal_id = $("#in_appraisal_id").val()
    var event = $("#id_event").val()
    var table = 'table_'+$("#modal_logbook").data('table')
    $.ajax({
      url: url,
      type: 'post',
      data: formData,
      processData: false,
      contentType: false,
      error: function () {
        btn_idle(btn)
        alert("Error al comentar.");
        return false;
      },
      success: function (data) {
        var element = $($.parseHTML(data))
        element.hide()
        $("#comment_list").prepend(element);
        element.slideDown()
        btn_idle(btn)
        if (event == comment_class['EVENT_VISITA_ACORDADA'] || event == comment_class['EVENT_PROPIEDAD_VISITADA'] ||
            event == comment_class['EVENT_ENVIADA_A_VISADOR'] || event == comment_class['EVENT_ENTREGADO_AL_CLIENTE']) {
          $("#id_event option[value='"+event+"']").remove();
        }
        $("#id_text").val("")
        $("#id_event").trigger('change')
        if (event == comment_class['EVENT_ENVIADA_A_VISADOR']) {
          $('#modal_logbook').modal('hide');
          moveRow('table_in_appraisal','table_in_revision',appraisal_id)
          assignTableActions();
        }
        if (event == comment_class['EVENT_ENTREGADO_AL_CLIENTE']) {
          $('#modal_logbook').modal('hide');
          moveRow('table_in_revision','table_sent',appraisal_id)
          assignTableActions();
        }
        if (event == comment_class['EVENT_INCIDENCIA']) {
          $('div#conflict').slideDown();
          $("#tr_"+table+"-"+appraisal_id).addClass('conflict')
        }
        if (event == comment_class['EVENT_ABORTADO']) {
          $("tr[id$=-"+appraisal_id+"]").remove();
        }
      },
      complete: function (data) {
        assignLogbookModalActions();
      }
    });
  });







  $(".btn_validate").unbind()
  $(".btn_validate").off()
  $(".btn_validate").on("change", function (event) {
    // Click of comment button in comment form.
    //if (this.checked) {
      checked = this.checked
      event.preventDefault();
      var btn = $(this)
      var url = ajax_validate_cliente_url
      var appraisal_id = $("#in_appraisal_id").val()
      var type = btn.data('type')
      var data = {'appraisal_id':appraisal_id,'type':type}
      $.ajax({
        url: url,
        type: 'get',
        data: data,
        error: function () {
          btn_idle(btn)
          alert("Error al validar cliente.");
          return false;
        },
        success: function (data) {
          // Add event to the event list
          var element = $($.parseHTML(data))
          element.hide()
          $("#comment_list").prepend(element);
          element.slideDown()
          if (type == "1") {
            $(".edit_contact_cliente").prop('disabled', checked);
          } else if (type == "2") {
            $(".edit_contact_contacto").prop('disabled', checked);
          }
          //
          assignLogbookModalActions()
        }
      });
    //}
  });
  
  $(".btn_delete_comment").unbind()
  $(".btn_delete_comment").off()
  $(".btn_delete_comment").on('click',function() {
    var btn = $(this)
    btn_loading(btn)
    var comment_id = $(this).data('comment_id');
    var event = $(this).data('event');
    var appraisal_id = $("#in_appraisal_id").val();
    var url = $(this).data('delete-comment-url');
    var table = $("#modal_logbook").data('table')
    $.ajax({
      url: url,
      type: 'get',
      data: {'comment_id':comment_id,'appraisal_id':appraisal_id,'table':table},
      error: function () {
        btn_idle(btn)
        alert("Error al eliminar comentario.");
        return false;
      },
      success: function (data) {
        btn_idle(btn)
        // Reset options in list
        $('#id_event').empty()
        for (var i=0; i<data.choices.length; i++) {
          $('#id_event').append($("<option></option>")
                  .attr("value",data.choices[i][0])
                  .text(data.choices[i][1]));
        }
        // Some things particular to events
        if (event == comment_class['EVENT_ENTREGADO_AL_CLIENTE']) {
          $('#modal_logbook').modal('hide');
          moveRow('table_sent','table_in_revision',appraisal_id)
          $("#id_event").trigger("change")
        } else if (event == comment_class['EVENT_CONTACTO_VALIDADO'] || 
                   event == comment_class['EVENT_CLIENTE_VALIDADO'] ||
                   event == comment_class['EVENT_CONTACTO_INVALIDADO'] ||
                   event == comment_class['EVENT_CLIENTE_INVALIDADO']) {
          if (event == comment_class['EVENT_CONTACTO_VALIDADO']) {
            btn = $("#btn_validate_contacto")
          } else {
            btn = $("#btn_validate_cliente")
          }
          btn.find(".validated_check").hide()
          btn.addClass('btn-dark')
          btn.removeClass('btn-outline-success')
          btn.find('.text').html("Validar")
          btn.prop('disabled', false)
        } else {
          $("#id_event").trigger("change")
        }
        // Remove the comment
        $('#comment_'+data.comment_id).slideUp()
      }
    });
  })

  $("#btn_solve_conflict").unbind()
  $("#btn_solve_conflict").off()
  $("#btn_solve_conflict").on("click", function (event) {
    var url = ajax_solve_conflict_url;
    var btn = $(this);
    var appraisal_id = btn.val(); // button has id of appraisal
    var table = 'table_'+$("#modal_logbook").data('table')
    btn_loading(btn,hide_text=true);
    $.ajax({
      url: url,
      type: 'get',
      data: {'appraisal_id':appraisal_id,'table':table},
      error: function() {
        btn_idle(btn);
        alert("Error al resolver conflicto.");
        return false;
      },
      success: function (data) {
        btn_idle(btn);
        $("#tr_"+table+'-'+appraisal_id).removeClass('conflict')
        $('div#conflict').slideUp();
        //moveRow("table_sent","table_in_revision",appraisal_id)
      }
    })
  });

  $("input#report").change(function () {
    var url = ajax_upload_report_url;
    //var btn = $(this);
    //btn_loading(btn,hide_text=true);
    var form = $("#form_report")
    var form_data = new FormData(form[0]);
    var table = $("#table_id").val()
    $.ajax({
      url: url,
      type: 'post',
      data: form_data,
      processData: false,
      contentType: false,
      error: function() {
        //btn_idle(btn);
        alert("Error al adjuntar reporte.");
      },
      success: function (data) {
        //btn_idle(btn);
        $('#modal_logbook').find('.modal-body').html($.trim(data));
        assignLogbookModalActions();
        $("#in_appraisal_id").val(appraisal_id); // hidden input
        $("#table_id").attr("value",table);
        if (table == "not_accepted") {
          $('#modal_logbook').find('#div_event').hide()
          $('#modal_logbook').find('#div_comment_btn').hide()
          $('#modal_logbook').find('#div_datetime').hide()
          $('#modal_logbook').find('#div_accept_reject').show()
        } else {
          $("#id_event").trigger("change")
        }
      }
    })
  });

  // FLOW. Actions that change the state of appraisals.

  $(".btn_accept").unbind()
  $(".btn_accept").off()
  $(".btn_accept").on("click", function (event) {
    // Button to accept an appraisals that has been requested.
    var url = ajax_accept_appraisal_url
    var btn = $(this)
    btn_loading(btn)
    var data = {}
    data["appraisal_id"] = btn.val()
    btn_loading(btn)
    $.ajax({
      url: url,
      type: 'get',
      data: data,
      error: function() {
        btn_idle(btn)
        alert("Error al aceptar tasación.");
      },
      success: function (ret) {
        btn_idle(btn)
        $('#modal_logbook').modal('hide');
        moveRow("table_not_accepted","table_in_appraisal",data["appraisal_id"])
      }
    })
  });

  $(".btn_reject").unbind()
  $(".btn_reject").off()
  $(".btn_reject").on("click", function (event) {
    // Button to reject an appraisals that has been requested.
    var url = ajax_reject_appraisal_url
    var btn = $(this)
    btn_loading(btn)
    var data = {}
    data["appraisal_id"] = btn.val()
    $.ajax({
      url: url,
      type: 'get',
      data: data,
      error: function() {
        btn_idle(btn)
        alert("Error al rechazar tasación.");
      },
      success: function (ret) {
        btn_idle(btn)
        $('#modal_logbook').modal('hide');
        moveRow("table_not_accepted","table_not_assigned",data["appraisal_id"])
      }
    })
  });

  $(".btn_enviar_a_visador").unbind()
  $(".btn_enviar_a_visador").off()
  $(".btn_enviar_a_visador").on("click", function (event) {
    var url = ajax_enviar_a_visador_url
    var btn = $(this)
    btn_loading(btn)
    var data = {}
    data["appraisal_id"] = btn.val()
    $.ajax({
      url: url,
      type: 'get',
      data: data,
      error: function() {
        btn_idle(btn);
        alert("Error al enviar tasación a revisión.");
        return false;
      },
      success: function (ret) {
        btn_idle(btn);
        $('#modal_logbook').modal('hide');
        moveRow("table_in_appraisal","table_in_revision",data["appraisal_id"])
      }
    })
  });

  $(".btn_devolver_a_tasador").unbind()
  $(".btn_devolver_a_tasador").off()
  $(".btn_devolver_a_tasador").on("click", function (event) {
    // Button to accept an appraisals that has been requested.
    var url = ajax_devolver_a_tasador_url
    var btn = $(this)
    btn_loading(btn)
    var data = {}
    data["appraisal_id"] = btn.val()
    $.ajax({
      url: url,
      type: 'get',
      data: data,
      error: function() {
        btn_idle(btn);
        alert("Error al devolver la tasación al tasador.");
        return false;
      },
      success: function (ret) {
        btn_idle(btn);
        $('#modal_logbook').modal('hide');
        moveRow("table_in_revision","table_in_appraisal",data["appraisal_id"])
      }
    })
  });

  $(".btn_enviar_a_cliente").unbind()
  $(".btn_enviar_a_cliente").off()
  $(".btn_enviar_a_cliente").on("click", function (event) {
    // Button to accept an appraisals that has been requested.
    var url = ajax_enviar_a_cliente_url
    var btn = $(this)
    btn_loading(btn)
    var data = {}
    data["appraisal_id"] = btn.val()
    $.ajax({
      url: url,
      type: 'get',
      data: data,
      error: function() {
        btn_idle(btn);
        alert("Error al enviar la tasación al cliente.");
        return false;
      },
      success: function (ret) {
        btn_idle(btn);
        $('#modal_logbook').modal('hide');
        moveRow("table_in_revision","table_sent",data["appraisal_id"])
      }
    })
  });

  $(".btn_enviar_a_cliente_again").unbind()
  $(".btn_enviar_a_cliente_again").off()
  $(".btn_enviar_a_cliente_again").on("click", function (event) {
    // Button to accept an appraisals that has been requested.
    var appraisal_id = $(this).val(); // button has id of appraisal
    var url = ajax_enviar_a_cliente_url
    var btn = $(this)
    var form = document.getElementById('form_comment');
    var formData = new FormData(form);
    btn_loading(btn)
    $.ajax({
      url: url,
      type: 'post',
      data: formData,
      processData: false,
      contentType: false,
      error: function() {
        btn_idle(btn);
        alert("Error al enviar la tasación al cliente.");
        return false;
      },
      success: function (data) {
        btn_idle(btn);
        $('#modal_logbook').modal('hide');
        moveRow("table_returned","table_sent",appraisal_id)
      }
    })
  });

  $(".btn_devolver_a_visador").unbind()
  $(".btn_devolver_a_visador").off()
  $(".btn_devolver_a_visador").on("click", function (event) {
    // Button to accept an appraisals that has been requested.
    var appraisal_id = $(this).val(); // button has id of appraisal
    var url = ajax_devolver_a_visador_url
    var btn = $(this)
    var form = document.getElementById('form_comment');
    var formData = new FormData(form);
    btn_loading(btn)
    $.ajax({
      url: url,
      type: 'post',
      data: formData,
      processData: false,
      contentType: false,
      error: function() {
        btn_idle(btn);
        alert("Error al devolver la tasación al visador.");
        return false;
      },
      success: function (data) {
        btn_idle(btn);
        $('#modal_logbook').modal('hide');
        moveRow("table_sent","table_in_revision",appraisal_id)
      }
    })
  });

  $(".btn_mark_as_returned").unbind()
  $(".btn_mark_as_returned").off()
  $(".btn_mark_as_returned").on("click", function (event) {
    var appraisal_id = $(this).val(); // button has id of appraisal
    var url = ajax_mark_as_returned_url
    var btn = $(this)
    var form = document.getElementById('form_comment');
    var formData = new FormData(form);
    btn_loading(btn)
    $.ajax({
      url: url,
      type: 'post',
      data: formData,
      processData: false,
      contentType: false,
      error: function() {
        btn_idle(btn);
        alert("Error al marcar tasación como devuelta.");
        return false;
      },
      success: function (data) {
        btn_idle(btn);
        $('#modal_logbook').modal('hide');
        moveRow("table_sent","table_returned",appraisal_id)
      }
    })
  });
}