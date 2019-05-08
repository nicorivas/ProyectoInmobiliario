/*
validation_config = {
  rules: {
    "addressStreet": "required",
    "addressNumber": "required",
    "addressCommune": "required"
  },
  messages: {
    "addressStreet": "Campo requerido",
    "addressNumber": "Requerido",
    "addressCommune": "Campo requerido"
  }
}
*/

function get_data(btn) {
  data = {}
  data["property_type"] = btn.closest(".property").data("property_type")
  data["property_id"] = btn.closest(".property").data("property_id")
  return data
}

function set_table_actions() {

  $('.btn_comparable_add_terrain_modal').unbind()
  $('.btn_comparable_add_terrain_modal').off()
  $(".btn_comparable_add_terrain_modal").on("click", function() {
    event.preventDefault()
    data = get_data($(this))
    console.log(data)
    url = $('#properties_data').data('ajax_add_property_comparable_modal_url')
    $.ajax({
      url: url,
      type: 'get',
      data: data,
      error: function () {
          alert("Error al cargar modal para agregar una propiedad.");
          return false;
      },
      success: function (ret) {
        $("#modal_add_property_comparable").html($.trim(ret));
        $("#modal_add_property_comparable").modal("show")
        $("#form_add_property_comparable").data(data)
        set_modal_actions()
      }
    });
  })

  $('.btn_edit_selected_property_modal').unbind()
  $('.btn_edit_selected_property_modal').off()
  $(".btn_edit_selected_property_modal").on("click", function() {
    event.preventDefault()
    data = getData($(this))
    data['property_selected_id'] = $(this).val()
    url = "{% url 'ajax_edit_property_similar_modal_url' %}"
    $.ajax({
      url: url,
      type: 'get',
      data: data,
      error: function () {
          alert("Error al cargar modal para agregar una propiedad.");
          return false;
      },
      success: function (ret) {
        $("#modal_add_property_similar").html($.trim(ret));
        $("#modal_add_property_similar").modal("show")
        $("#form_add_property_similar").data(data)
        set_modal_actions()
      }
    });
  })

  $('.btn_remove_selected_property').unbind()
  $('.btn_remove_selected_property').off()
  $('.btn_remove_selected_property').click(function() {
    event.preventDefault()
    data = getData($(this))
    data['property_selected_id'] = $(this).val()
    url = "{% url 'ajax_remove_property_similar_url' %}"
    $.ajax({
      url: url,
      type: 'get',
      data: data,
      error: function () {
          alert("Error al remover propiedad.");
          return false;
      },
      success: function (ret) {
        if (data.terrain_id) {
          $("#terrain_"+data.terrain_id).html($.trim(ret));
        }
        if (data.building_id) {
          $("#building_"+data.building_id).html($.trim(ret));
        }
        set_modal_actions()
        set_table_actions()
        tablesSelectedCompute()
      }
    });
  });

}

//$("#form_add_property_similar").validate(validation_config)

function set_modal_actions() {

  $("#btn_add_property_similar").unbind()
  $("#btn_add_property_similar").off()
  $("#btn_add_property_similar").on("click", function() {
    event.preventDefault()
    url = "{% url 'ajax_add_property_similar_url' %}"
    form = $("#form_add_property_similar")
    data = join_data(form,form)
    $.ajax({
      url: url,
      type: 'post',
      data: $.param(data),
      error: function () {
          alert("Error al agregar o editar propiedad.");
          return false;
      },
      success: function (ret) {
        data = data.reduce(function(map,obj) { map[obj.name] = obj.value; return map}, {});
        if (data.terrain_id) {
          $("#terrain_"+data.terrain_id).html($.trim(ret));
        }
        if (data.building_id) {
          $("#building_"+data.building_id).html($.trim(ret));
        }
        $("#modal_add_property_similar").modal("hide")
        set_modal_actions()
        set_table_actions()
        tablesSelectedCompute()
      }
    });
  })
}