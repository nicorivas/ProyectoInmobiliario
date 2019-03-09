function btn_loading(btn,hide_text,disable=true) {
  // Remove notifications
  btn.removeClass('btn-not');
  btn.find('.notification').fadeOut();
  // Add circle
  btn.addClass('running');
  btn.find('.ld').show();
  btn.find('.icon').hide();
  // Disable
  if (disable) {
    btn.prop('disabled', true);
  }
  if (hide_text) {
    btn.find('.text').hide()
    btn.find('.loading_text').show()
  }
}

function btn_idle(btn) {
  btn.removeClass('running');
  btn.find('.ld').hide();
  btn.find('.icon').show();
  btn.prop('disabled', false);
  btn.find('.text').show()
  btn.find('.loading_text').hide()
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

function addRow(table_name, appraisal_id, html) {
  // Remove row from table. Takes into account if this is
  // the last row remaining, in that case it hides the whole
  // table and shows the no elements alert div.
  $("<tr class='"+table_name+"' id='tr_"+table_name+"-"+appraisal_id+"' style='display:none;'>"+html+"</tr>").appendTo($('#'+table_name)).fadeIn()
  //$("#tr_"+table_name+"-"+appraisal_id).slideDown()
  $("#div_alert_"+table_name).fadeOut()
  $("#"+table_name).fadeIn()
  if (table_name == "table_returned") {
    $("#div_returned").slideDown()
  }
}

function removeRow(table_name, appraisal_id) {
  // Remove row from table. Takes into account if this is
  // the last row remaining, in that case it hides the whole
  // table and shows the no elements alert div.
  $("#tr_"+table_name+"-"+appraisal_id).fadeOut("normal", function() { $(this).remove(); })
  var nrows = $("#"+table_name+" tr.appraisal").length;
  console.log('nrows',nrows)
  if (nrows == 0) {
    if (table_name == "table_returned") {
      // Returned table is hidden when there are now appraisals left
      $("#div_returned").slideUp()
    } else {
      $("#"+table_name).fadeOut()
      $("#div_alert_"+table_name).fadeToggle()
    }
  }
}

function moveRow(table_from, table_to, appraisal_id) {
  var url = ajax_get_appraisal_row_url
  $.ajax({
    url: url,
    type: 'get',
    data: {'appraisal_id':appraisal_id,'table':table_to},
    error: function() {
      alert("Error al cambiar fila.");
    },
    success: function (ret) {
      removeRow(table_from,appraisal_id)
      addRow(table_to,appraisal_id,ret)
      assignTableActions();
    }
  })
}

function replaceRow(table_name, appraisal_id, html) {
  // Replace row
  $("#tr_"+table_name+"-"+appraisal_id).html(html)
}

function replaceTable(table_name,data) {
  // Replaces a table, usually from data from AJAX. Takes
  // into account the size of the table and hides the 
  // alert of no elements if the table returned has elements.
  $("#"+table_name).html($.trim(data))
  var nrows = $("#"+table_name+" tr").length;
  if (nrows == 0) {
    $("#"+table_name).fadeOut()
    $("#div_alert_"+table_name).fadeIn()
  } else {
    $("#"+table_name).fadeIn()
    $("#div_alert_"+table_name).fadeOut()
  }
}