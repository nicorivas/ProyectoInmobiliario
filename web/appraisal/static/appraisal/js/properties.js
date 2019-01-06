function properties_data() {
  var data = {}
  data['appraisal_id'] = $("#properties_data").data("appraisal_id")
  data['real_estate_id'] = $("#properties_data").data("real_estate_id")
  data['terrain_id'] = $("#properties_data").data("terrain_id")
  data['building_id'] = $("#properties_data").data("building_id")
  data['apartment_id'] = $("#properties_data").data("apartment_id")
  return data
}

function btn_loading(btn) {
  btn.addClass('running');
  btn.find('.ld').show();
  btn.find('.icon').show();
  btn.prop('disabled', true);
}

function btn_idle(btn) {
  btn.removeClass('running');
  btn.find('.ld').hide();
  btn.find('.icon').hide();
  btn.prop('disabled', false);
}

function set_address_list_actions() {

  $('#btn_add_address_modal').unbind()
  $('#btn_add_address_modal').off()
  $('#btn_add_address_modal').on('click', function() {
    /*
    Button (as link) to open the modal to add an address to the list.
    Loads corresponding data. The AJAX view returns the modal with the
    corresponding data.
    */
    var btn = $(this)
    var data = properties_data()
    var url = $("#properties_data").data("ajax_add_address_modal_url")
    btn_loading(btn)
    $.ajax({
      url: url,
      type: 'get',
      data: data,
      error: function () {
          alert("Error al cargar modal para agregar una dirección.");
          btn.find('.ld').toggle();
          btn.prop('disabled', false);
          return false;
      },
      success: function (ret) {
        btn_idle(btn);
        $("#modal_add_address").html($.trim(ret));
        $("#modal_add_address").modal('show')
        set_modal_actions_properties()
        set_address_list_actions()
      }
    });
  })

  $('#btn_edit_address_modal').unbind()
  $('#btn_edit_address_modal').off()
  $('#btn_edit_address_modal').on('click', function() {
    /*
    Button to open the modal to edit the currently selected address.
    Loads corresponding data. The AJAX view returns the modal with the
    corresponding data.
    */
    var btn = $(this)
    var data = properties_data()
    data['real_estate_id'] = $('#select_realestate').find(":selected").val();
    var url = $("#properties_data").data("ajax_edit_address_modal_url")
    btn_loading(btn)
    $.ajax({
      url: url,
      type: 'get',
      data: data,
      error: function () {
          alert("Error al cargar modal para editar dirección.");
          btn_idle(btn)
          return false;
      },
      success: function (ret) {
        btn_idle(btn)
        $("#properties_data").data(data)
        $('#modal_edit_address').html($.trim(ret));
        $("#modal_edit_address").modal('show')
        set_modal_actions_properties()
        set_address_list_actions()
      }
    });
  })

  $('#select_realestate').unbind()
  $('#select_realestate').off()
  $('#select_realestate').on('change', function() {
    /*
    Triggered when an element from the list of address is selected.
    */
    var data = properties_data()
    data["real_estate_id"] = $(this).val()
    var url = $("#properties_data").data("ajax_load_realestate_url")
    $.ajax({
      url: url,
      type: 'get',
      data: data,
      error: function () {
          alert("Error al cargar dirección.");
          return false;
      },
      success: function (ret) {
        $("#properties_data").data(data)
        $("#property_info").fadeOut();
        $("#property_list").html($.trim(ret));
        set_property_list_actions();
      }
    });
  })
}

function set_property_list_actions() {

  $(".btn_property").unbind()
  $(".btn_property").off()
  $('.btn_property').on('click', function() {
    
    event.preventDefault()

    if (!$('#no_form').length) {
      save_property()
    }

    var btn = $(this)
    var data = properties_data()
    data["building_id"] = btn.data('building_id')
    data["apartment_id"] = btn.data('apartment_id')
    data["terrain_id"] = btn.data('terrain_id')

    $("#in_appraisal_id").val(data["appraisal_id"])
    $("#in_real_estate_id").val(data["real_estate_id"])
    $("#in_building_id").val(data["building_id"])
    $("#in_apartment_id").val(data["apartment_id"])
    $("#in_terrain_id").val(data["terrain_id"])

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
        $("#property_list").find(".btn_property").each(function() {
          $(this).removeClass("btn-active")
        })
        btn.addClass('btn-active')
        $("#property_info").html($.trim(ret));
        $('#property_info').show();
        set_property_view_actions();
      }
    });
  })

  $("#btn_add_property_modal").unbind()
  $("#btn_add_property_modal").off()
  $('#btn_add_property_modal').on('click', function() {
    event.preventDefault()
    var btn = $(this)
    var data = properties_data()
    data["building_id"] = btn.closest('.building_list_item').data('building_id')
    data["property_id"] = btn.val()
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
}

function set_modal_actions_properties() {

  $("#btn_edit_address").unbind()
  $("#btn_edit_address").off()
  $('#btn_edit_address').on('click', function() {
    var btn = $(this)
    var form = $('#form_edit_address')
    var url = $("#properties_data").data("ajax_edit_address_url")
    btn_loading(btn)
    $.ajax({
      url: url,
      type: 'post',
      data: form.serialize(),
      error: function () {
          btn_idle(btn);
          alert("Error al guardar nueva dirección.");
          return false;
      },
      success: function (data) {
        if (data.error) {
          btn_idle(btn)
          $('#edit_address_alert').fadeIn()
          $('#edit_address_alert').html(data.error)
        } else {
          btn_idle(btn)
          $('#select_realestate').find(":selected").text(data.address);
          $("#modal_edit_address").modal('hide')
        }
      }
    });
  })

  $("#btn_add_address").unbind()
  $("#btn_add_address").off()
  $('#btn_add_address').on('click', function() {
    var btn = $(this)
    var form = $('#form_add_address')
    var url = $("#properties_data").data("ajax_add_address_url")
    btn_loading(btn)
    $.ajax({
      url: url,
      type: 'post',
      data: form.serialize(),
      error: function () {
          btn_idle(btn);
          alert("Error al agregar nueva dirección.");
          return false;
      },
      success: function (data) {
        if (data.error) {
          btn_idle(btn);
          $('#add_address_alert').fadeIn()
          $('#add_address_alert').html(data.error)
        } else {
          btn_idle(btn);
          $("#address_list").html($.trim(data));
          set_address_list_actions();
          $('#select_realestate').val($('#select_realestate option:last').val());
          $("#modal_add_address").modal('hide');
          $('#select_realestate').trigger('change');
        }
      }
    });
  })

  $("#btn_remove_address").unbind()
  $("#btn_remove_address").off()
  $('#btn_remove_address').on('click', function() {
    var btn = $(this)
    var form = $('#form_edit_address')
    var url = $("#properties_data").data("ajax_remove_address_url")
    btn_loading(btn)
    $.ajax({
      url: url,
      type: 'post',
      data: form.serialize(),
      error: function () {
          btn_idle(btn);
          alert("Error al remover dirección.");
          return false;
      },
      success: function (data) {
        btn_idle(btn);
        $('#select_realestate').find(":selected").remove();
        $('#select_realestate').val($('#select_realestate option:last').val());
        $('#select_realestate').trigger('change');
        $("#modal_edit_address").modal('hide')
      }
    });
  })

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
          $('#property_list').html($.trim(data));
          set_property_list_actions();
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
        $('#property_list').html($.trim(data));
        set_property_list_actions();
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
        $('#property_list').html($.trim(data));
        set_property_list_actions();
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
        $('#property_list').html($.trim(data));
        set_property_list_actions();
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

function join_data(form,element) {
  var data_form = form.serializeArray(); // convert form to array
  var data_html = element.data()
  for (var k in data_html) {
    var found = 0
    for (var i in data_form) {
      if (data_form[i].name == k) {
        data_form[i].value = data_html[k]
        found = 1
      }
    }
    if (!found) {
      data_form.push({'name':k,'value':data_html[k]})
    }
  }
  return data_form
}

function save_property() {
  if ($("#property_info").children().length > 1) {
    console.log('save')
    var form = $('#form_property')
    var url = $("#properties_data").data("ajax_save_property_url")
    data = join_data(form,$("#properties_data"))
    $.ajax({
      url: url,
      type: 'post',
      data: $.param(data),
      async: false,
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
    var data = properties_data()
    data['code'] = $("#select_roles").val()
    var url = $("#properties_data").data("ajax_edit_rol_modal_url");
    $.ajax({
      url: url,
      type: 'get',
      data: data,
      error: function () {
          alert("Error al cargar modal para editar rol.");
          return false;
      },
      success: function (data) {
        $("#modal_add_rol").html($.trim(data));
        $("#modal_add_rol").modal("show")
        set_modal_actions_properties()
      }
    });
  })
}