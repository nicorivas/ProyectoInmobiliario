function load_sidebar() {
  /*
  Loads the sidebar, via an ajax request.
  1. Sets the loading state of the sidebar
  2. Calls teh ajax.
  */
  var url = $("#properties_data").data("ajax_load_sidebar_url")
  $("#properties_list").find("#loading").show()
  $("#properties_list").find("#list").hide()
  data = {}
  data['appraisal_id'] = $("#appraisal_data").data("appraisal_id")
  $.ajax({
    url: url,
    type: 'get',
    data: data,
    error: function () {
        alert("Error al cargar propiedades.");
        return false;
    },
    success: function (ret) {
      $("#properties_list").html($.trim(ret));
      set_properties_list_actions();
    }
  });
}

function show_modal(modal_name) {
  // Deactivate call, so that actions are resetted
  $(".btn_"+modal_name+"_modal").unbind()
  $(".btn_"+modal_name+"_modal").off()
  // Actual event
  $(".btn_"+modal_name+"_modal").on('click', function() {
    event.preventDefault() // Don't really know if it's needed
    var btn = $(this)
    var data = {}
    data["appraisal_id"] = $("#appraisal_data").data("appraisal_id")
    data["real_estate_id"] = btn.closest(".real_estate_data").data("real_estate_id")
    var url = $('#properties_data').data("ajax_"+modal_name+"_modal_url")
      $.ajax({
      url: url,
      type: 'get',
      data: data,
      error: function () {
          alert("Error al cargar modal '"+modal_name+"'");
          return false;
      },
      success: function (ret) {
        $("#modal_"+modal_name).html($.trim(ret));
        $("#modal_"+modal_name).modal("show");
      }
    });
  })
}

function set_properties_list_actions() {

  $(".btn_property").unbind()
  $(".btn_property").off()
  $('.btn_property').on('click', function() {
    
    event.preventDefault()

    if (!$('#no_form').length) {
      save_property()
    }

    var btn = $(this)
    var data = {}
    data["property_type"] = btn.data('property_type')
    data["property_id"] = btn.data('property_id')

    var url = $("#properties_data").data("ajax_show_property_url")

    btn.addClass('building_list_item_selected')

    $.ajax({
      url: url,
      type: 'get',
      data: data,
      error: function () {
          alert("Error al cargar información de la propiedad.");
          return false;
      },
      success: function (ret) {
        $("#properties_data").data(data)
        $("#properties_list").find(".property_list_item").each(function() {
          $(this).removeClass("property_list_item_active")
        })
        btn.closest(".property_list_item").addClass('property_list_item_active')
        $("#property_info").html($.trim(ret));
        $('#property_info').show();
        set_property_view_actions();
      }
    });
  })

  show_modal("edit_address")

  /*
  $("#btn_edit_address_modal").ubind()
  $("#btn_edit_address_modal").off()
  $('#btn_edit_address_modal').on('click', function() {
    event.preventDefault()
    var btn = $(this)
    var data = {}
    data['appraisal_id'] = $("#appraisal_data").data("appraisal_id")
    var url = $('#properties_data').data('ajax_edit_address_modal_url')
    $.ajax({
      url: url,
      type: 'get',
      data: data,
      error: function () {
          alert("Error al cargar modal para editar direcciones.");
          return false;
      },
      success: function (ret) {
        $("#modal_edit_address").html($.trim(ret));
        $("#modal_edit_address").modal("show");
      }
    });
  }
  */

  $("#btn_add_property_modal").unbind()
  $("#btn_add_property_modal").off()
  $('#btn_add_property_modal').on('click', function() {
    event.preventDefault()
    var btn = $(this)
    var data = {}
    data['appraisal_id'] = $("#appraisal_data").data("appraisal_id")
    var url = $('#properties_data').data('ajax_add_property_modal_url')
    $.ajax({
      url: url,
      type: 'get',
      data: data,
      error: function () {
          alert("Error al cargar modal para agregar propiedad.");
          return false;
      },
      success: function (ret) {
        $("#properties_data").data(data)
        $("#modal_add_property").html($.trim(ret));
        $("#modal_add_property").modal("show")
        set_modal_actions_properties()
      }
    });
  })

  $("#btn_add_apartment_modal").unbind()
  $("#btn_add_apartment_modal").off()
  $('#btn_add_apartment_modal').on('click', function() {
    event.preventDefault()
    var btn = $(this)
    var data = properties_data()
    data["building_id"] = btn.closest('.building_list_item').data('building_id')
    data["property_id"] = btn.data('value')
    var url = $('#properties_data').data('ajax_add_apartment_modal_url')
    $.ajax({
      url: url,
      type: 'get',
      data: data,
      error: function () {
          alert("Error al cargar modal para agregar departamento.");
          return false;
      },
      success: function (ret) {
        $("#properties_data").data(data)
        $("#modal_add_apartment").html($.trim(ret));
        $("#modal_add_apartment").modal("show")
        set_modal_actions_properties()
      }
    });
  })

  $(".btn_edit_property_modal").unbind()
  $(".btn_edit_property_modal").off()
  $('.btn_edit_property_modal').on('click', function() {
    event.preventDefault()
    btn = $(this)
    data = properties_data()
    data['terrain_id'] = btn.data("terrain_id")
    data['building_id'] = btn.data("building_id")
    data['apartment_id'] = btn.data("apartment_id")
    var url = $("#properties_data").data("ajax_edit_property_modal_url")
    $.ajax({
      url: url,
      type: 'get',
      data: data,
      error: function () {
          alert("Error al cargar modal para editar propiedad.");
          return false;
      },
      success: function (data) {
        $('properties_data').data(btn.data("terrain_id"))
        $('properties_data').data(btn.data("building_id"))
        $('properties_data').data(btn.data("apartment_id"))
        $("#modal_edit_property").html($.trim(data));
        $("#modal_edit_property").modal("show")
        set_modal_actions_properties()
      }
    });
  });

  $(".btn_remove_property").unbind()
  $(".btn_remove_property").off()
  $(".btn_remove_property").on('click', function() {
    var btn = $(this)
    btn.closest("div.list-group-item").addClass("loading")
    var url = $("#properties_data").data("ajax_remove_property_url")
    var data = {}
    data['appraisal_id'] = $("#appraisal_data").data("appraisal_id")
    data["property_type"] = btn.data('property_type')
    data["property_id"] = btn.data('property_id')
    $.ajax({
      url: url,
      type: 'get',
      data: data,
      error: function () {
          alert("Error al remover propiedad.");
          return false;
      },
      success: function (ret) {
        console.log("ret")
        btn.closest("div.list-group-item").slideUp()
        console.log(btn.find("li"))
      }
    });
  })

}

function set_modal_actions_properties() {

  $("#btn_add_property").unbind()
  $("#btn_add_property").off()
  $("#btn_add_property").on('click', function() {
    var form = $('#form_add_property')
    if (form.valid()) {
      var btn = $(this)
      btn_loading(btn)
      var url = $("#properties_data").data("ajax_add_property_url")
      $.ajax({
        url: url,
        type: 'post',
        data: form.serialize(),
        error: function () {
            btn_idle(btn);
            alert("Error al agregar propiedad.");
            return false;
        },
        success: function (data) {
          btn_idle(btn);
          $("#modal_add_property").modal('hide')
          $('#property_info').fadeOut();
          load_sidebar();
        }
      });
    }
  })

  $("#btn_edit_property").unbind()
  $("#btn_edit_property").off()
  $('#btn_edit_property').on('click', function() {
    var btn = $(this)
    var form = $('#form_edit_property')
    var url = $("#properties_data").data("ajax_edit_property_url")
    btn_loading(btn)
    $.ajax({
      url: url,
      type: 'post',
      data: form.serialize(),
      error: function () {
          btn_idle(btn);
          alert("Error al editar propiedad.");
          return false;
      },
      success: function (data) {
        btn_idle(btn);
        $("#modal_edit_property").modal('hide')
        $('#properties_list').html($.trim(data));
        set_properties_list_actions();
      }
    });
  })

  $("#btn_remove_property").unbind()
  $("#btn_remove_property").off()
  $('#btn_remove_property').on('click', function() {
    var btn = $(this)
    var form = $('#form_edit_property')
    var url = $("#properties_data").data("ajax_remove_property_url")
    btn_loading(btn)
    $.ajax({
      url: url,
      type: 'post',
      data: form.serialize(),
      error: function () {
          btn_idle(btn);
          alert("Error al remover propiedad.");
          return false;
      },
      success: function (data) {
        btn_idle(btn);
        $("#modal_edit_property").modal('hide')
        $('#properties_list').html($.trim(data));
        set_properties_list_actions();
      }
    });
  })

  $("#btn_add_apartment").unbind()
  $("#btn_add_apartment").off()
  $('#btn_add_apartment').on('click', function() {
    var btn = $(this)
    var form = $('#form_add_apartment')
    var url = $("#properties_data").data("ajax_add_apartment_url")
    btn_loading(btn)
    $.ajax({
      url: url,
      type: 'post',
      data: form.serialize(),
      error: function () {
          btn_idle(btn);
          alert("Error al agregar departamento.");
          return false;
      },
      success: function (data) {
        btn_idle(btn);
        $("#modal_add_apartment").modal('hide')
        $('#properties_list').html($.trim(data));
        set_properties_list_actions();
      }
    });
  })

  $("#btn_add_rol").unbind()
  $("#btn_add_rol").off()
  $('#btn_add_rol').on('click', function() {
    var btn = $(this)
    var form = $('#form_add_rol')
    data = join_data(form,$("#properties_data"))
    var url = $("#properties_data").data("ajax_add_rol_url")
    btn_loading(btn)
    $.ajax({
      url: url,
      type: 'post',
      data: $.param(data),
      error: function () {
          btn_idle(btn);
          alert("Error al agregar rol.");
          return false;
      },
      success: function (data) {
        btn_idle(btn);
        $('#line_roles').html($.trim(data));
        $("#modal_add_rol").modal('hide')
        $('#select_roles').val($('#select_roles option:last').val());
        set_property_view_actions()
      }
    })
  });

  $("#btn_edit_rol").unbind()
  $("#btn_edit_rol").off()
  $('#btn_edit_rol').on('click', function() {
    var btn = $(this)
    var form = $('#form_add_rol')
    data = join_data(form,$("#properties_data"))
    var url = $("#properties_data").data("ajax_edit_rol_url")
    btn_loading(btn)
    $.ajax({
      url: url,
      type: 'post',
      data: $.param(data),
      error: function () {
          btn_idle(btn);
          alert("Error al editar rol.");
          return false;
      },
      success: function (data) {
        btn_idle(btn);
        $('#line_roles').html($.trim(data));
        $("#modal_add_rol").modal('hide')
        $('#select_roles').val($('#select_roles option:last').val());
        set_property_view_actions()
      }
    })
  });

  $("#btn_remove_rol").unbind()
  $("#btn_remove_rol").off()
  $('#btn_remove_rol').on('click', function() {
    var btn = $(this)
    var form = $('#form_add_rol')
    data = join_data(form,$("#properties_data"))
    var url = $("#properties_data").data("ajax_remove_rol_url")
    btn_loading(btn)
    $.ajax({
      url: url,
      type: 'post',
      data: $.param(data),
      error: function () {
          btn_idle(btn);
          alert("Error al remover rol.");
          return false;
      },
      success: function (data) {
        btn_idle(btn);
        $('#line_roles').html($.trim(data));
        $("#modal_add_rol").modal('hide')
        $('#select_roles').val($('#select_roles option:last').val());
        set_property_view_actions()
      }
    })
  });
}

function save_property() {
  if ($("#property_info").children().length > 1) {
    var form = $('#form_property')
    var url = $("#properties_data").data("ajax_save_property_url")
    data = join_data(form,$("#properties_data"))
    $.ajax({
      url: url,
      type: 'post',
      data: $.param(data),
      error: function () {
          alert("Error al grabar.");
          return false;
      },
      success: function (data) {
        $("#property_info_alert").html($.trim(data));
        $('#property_info_alert').show();
      }
    });
  }
}

function set_property_view_actions() {

  $("#btn_add_rol_modal").unbind()
  $("#btn_add_rol_modal").off()
  $('#btn_add_rol_modal').on('click', function() {
    event.preventDefault()
    var btn = $(this)
    data = properties_data()
    var url = $("#properties_data").data("ajax_add_rol_modal_url");
    $.ajax({
      url: url,
      type: 'get',
      data: data,
      error: function () {
          alert("Error al cargar modal para agregar rol.");
          btn.find('.ld').toggle();
          btn.prop('disabled', false);
          return false;
      },
      success: function (data) {
        $("#modal_add_rol").html($.trim(data));
        $("#modal_add_rol").modal("show")
        set_modal_actions_properties()
      }
    });
  })

  $("#btn_edit_rol_modal").unbind()
  $("#btn_edit_rol_modal").off()
  $('#btn_edit_rol_modal').on('click', function() {
    event.preventDefault()
    var btn = $(this)
    btn_loading(btn)
    var data = properties_data()
    data['code'] = $("#select_roles").val()
    var url = $("#properties_data").data("ajax_edit_rol_modal_url");
    $.ajax({
      url: url,
      type: 'get',
      data: data,
      error: function () {
          btn_idle(btn)
          alert("Error al cargar modal para editar rol.");
          return false;
      },
      success: function (data) {
        btn_idle(btn)
        $("#modal_add_rol").html($.trim(data));
        $("#modal_add_rol").modal("show")
        set_modal_actions_properties()
      }
    });
  })
}