function btn_assign_tasador_tasadores(data) {
    var url = "ajax/assign_tasador_tasadores";
    $.ajax({
        url: url,
        data: data,
        type: 'get',
        error: function () {
            alert("Error al cargar tasadores.");
            return false;
        },
        success: function (ret) {
            $("#tasadores").html(ret)
            $("#modal_assign_tasador").find("#ld-alert").hide()
        }
    });
}

function btn_assign_visador_visadores(data) {
    var url = "ajax/assign_visador_visadores";
    $.ajax({
        url: url,
        data: data,
        type: 'get',
        error: function () {
            alert("Error al cargar visadores.");
            return false;
        },
        success: function (ret) {
            $("#visadores").html(ret)
            $("#modal_assign_visador").find("#ld-alert").hide()
        }
    });
}


function show_modal(modal_name, data = {}, success_function = null, parent = null) {
    // Deactivate call, so that actions are resetted
    $(".btn_" + modal_name + "_modal").unbind()
    $(".btn_" + modal_name + "_modal").off()
    // Actual event
    $(".btn_" + modal_name + "_modal").on('click', function () {
        event.preventDefault() // Don't really know if it's needed
        // Add to data all the data in the button
        var btn = $(this)
        var btn_data = btn.data()
        for (var key in btn_data) {
            data[key] = btn_data[key]
        }
        if (parent != null) {
            data['parent'] = $(this).closest(parent).attr("id")
        }
        var url = "ajax/" + modal_name + "_modal"
        btn_loading(btn)
        $.ajax({
            url: url,
            type: 'get',
            data: data,
            error: function () {
                btn_idle(btn)
                alert("Error al cargar modal '" + modal_name + "'");
                return false;
            },
            success: function (ret) {
                btn_idle(btn)
                $("#modal_" + modal_name).html($.trim(ret));
                $("#modal_" + modal_name).modal("show");
                // If there are hidden inputs and data with the same name,
                // change the value of the input. For POST requests inside the modal.
                $("#modal_" + modal_name + " input:hidden").each(function (index) {
                    for (var key in data) {
                        if (key == $(this).attr("name")) {
                            $(this).val(data[key])
                        }
                    }
                })
                // Data is assigned to the modal
                $("#modal_" + modal_name).data(data)
                if (success_function != null) {
                    success_function(data)
                }
            }
        });
    })
}

function assignTableActions() {

    $(".btn_logbook").unbind()
    $(".btn_logbook").off()
    $(".btn_logbook").on("click", buttonLogbookClick)

    show_modal("expenses")

    show_modal("assign_tasador", {}, success_function = btn_assign_tasador_tasadores, parent = ".table-appraisals")

    show_modal("assign_visador", {}, success_function = btn_assign_visador_visadores, parent = ".table-appraisals")

    $(".btn_unassign_tasador_modal").unbind()
    $(".btn_unassign_tasador_modal").off()
    $(".btn_unassign_tasador_modal").on("click", function (event) {
        // Show the modal (via bootsrap), and set the corresponding variable inside the modal
        // to the appraisal id, which is the value of the button clicked.
        var id = $(this).val();
        $('#modal_unassign_tasador_appraisal_id').val(id);
    });

    show_modal("evaluate")

    show_modal("edit_address",{"ajax_edit_address_url":"/appraisal/ajax/edit_address/","source":"list"},null,parent = ".table-appraisals")

    $(".btn_archive_appraisal_modal").unbind()
    $(".btn_archive_appraisal_modal").off()
    $(".btn_archive_appraisal_modal").on("click", function (event) {
        // Called on click of delete button in the active table.
        var appraisal_id = $(this).data('appraisal_id');
        var source_table = $(this).closest('table').attr('id');
        $('#modal_archive').find('#appraisal_id').val(appraisal_id);
        $('#modal_archive').find('#source_table').val(source_table);
        $('#modal_archive').modal('show');
    });

}