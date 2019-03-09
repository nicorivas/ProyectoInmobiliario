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
    var table = 'table_'+$("#logbook").data('table')
    //$('#logbook').find('#loading').show()
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
          $('#logbook').modal('hide');
          moveRow('table_in_appraisal','table_in_revision',appraisal_id)
          assignTableActions();
        }
        if (event == comment_class['EVENT_ENTREGADO_AL_CLIENTE']) {
          $('#logbook').modal('hide');
          moveRow('table_in_revision','table_sent',appraisal_id)
          assignTableActions();
        }
        if (event == comment_class['EVENT_INCIDENCIA']) {
          $('div#conflict').slideDown();
          console.log($("#tr_"+table+"-"+appraisal_id))
          $("#tr_"+table+"-"+appraisal_id).addClass('conflict')
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
    var table = $("#logbook").data('table')
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
          $('#logbook').modal('hide');
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

  $(".btn_accept").unbind()
  $(".btn_accept").off()
  $(".btn_accept").on("click", function (event) {
    // Button to accept an appraisals that has been requested.
    var appraisal_id = $(this).val(); // button has id of appraisal
    var url = ajax_accept_appraisal_url
    var btn = $(this)
    var form = document.getElementById('form_comment');
    var formData = new FormData(form);
    btn.find('.ld').toggle();
    btn.find('#icon').toggle();
    btn.prop('disabled', true);
    $.ajax({
      url: url,
      type: 'post',
      data: formData,
      processData: false,
      contentType: false,
      error: function() {
        alert("Error al aceptar tasación.");
        btn.find('.ld').toggle();
        btn.find('#icon').toggle();
        btn.prop('disabled',false);
        return false;
      },
      success: function (data) {
        removeRow("table_not_accepted",appraisal_id)
        replaceTable("table_in_appraisal",data)
        assignTableActions();
      },
      complete: function (data) {
        btn.find('.ld').toggle();
        btn.find('#icon').toggle();
        btn.prop('disabled', false);
        $('#logbook').modal('hide');
      }
    })
  });

  $(".btn_reject").unbind()
  $(".btn_reject").off()
  $(".btn_reject").on("click", function (event) {
    // Button to reject an appraisals that has been requested.
    var appraisal_id = $(this).val(); // button has id of appraisal
    var url = ajax_reject_appraisal_url
    var btn = $(this)
    var form = document.getElementById('form_comment');
    var formData = new FormData(form);
    event.preventDefault();
    btn.find('.ld').toggle();
    btn.find('#icon').toggle();
    btn.prop('disabled', true);
    $.ajax({
      url: url,
      type: 'post',
      data: formData,
      processData: false,
      contentType: false,
      error: function() {
        alert("Error al rechazar tasación.");
        btn.find('.ld').toggle();
        btn.find('#icon').toggle();
        btn.prop('disabled', false);
        return false;
      },
      success: function (data) {
        removeRow("table_not_accepted",appraisal_id)
        replaceTable("table_not_assigned",data)
        assignTableActions();
      },
      complete: function (data) {
        btn.find('.ld').toggle();
        btn.find('#icon').toggle();
        btn.prop('disabled', false);
        $('#logbook').modal('hide');
      }
    })
  });

  $(".btn_enviar_a_visador").unbind()
  $(".btn_enviar_a_visador").off()
  $(".btn_enviar_a_visador").on("click", function (event) {
    // Button to accept an appraisals that has been requested.
    var appraisal_id = $(this).val(); // button has id of appraisal
    var url = ajax_enviar_a_visador_url
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
        alert("Error al enviar tasación a revisión.");
        return false;
      },
      success: function (data) {
        btn_idle(btn);
        $('#logbook').modal('hide');
        moveRow("table_in_appraisal","table_in_revision",appraisal_id)
      }
    })
  });

  $(".btn_devolver_a_tasador").unbind()
  $(".btn_devolver_a_tasador").off()
  $(".btn_devolver_a_tasador").on("click", function (event) {
    // Button to accept an appraisals that has been requested.
    var appraisal_id = $(this).val(); // button has id of appraisal
    var url = ajax_devolver_a_tasador_url
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
        alert("Error al devolver la tasación al tasador.");
        return false;
      },
      success: function (data) {
        btn_idle(btn);
        $('#logbook').modal('hide');
        moveRow("table_in_revision","table_in_appraisal",appraisal_id)
      }
    })
  });

  $(".btn_enviar_a_cliente").unbind()
  $(".btn_enviar_a_cliente").off()
  $(".btn_enviar_a_cliente").on("click", function (event) {
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
        $('#logbook').modal('hide');
        moveRow("table_in_revision","table_sent",appraisal_id)
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
        $('#logbook').modal('hide');
        moveRow("table_sent","table_in_revision",appraisal_id)
      }
    })
  });

  $("#btn_solve_conflict").unbind()
  $("#btn_solve_conflict").off()
  $("#btn_solve_conflict").on("click", function (event) {
    var url = ajax_solve_conflict_url;
    var btn = $(this);
    var appraisal_id = btn.val(); // button has id of appraisal
    var table = 'table_'+$("#logbook").data('table')
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
}