function btn_loading(btn,hide_text) {
  // Remove notifications
  btn.removeClass('btn-not');
  btn.find('.notification').fadeOut();
  // Add circle
  btn.addClass('running');
  btn.find('.ld').show();
  btn.find('.icon').hide();
  // Disable
  btn.prop('disabled', true);
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
}

function removeRow(table_name, appraisal_id) {
  // Remove row from table. Takes into account if this is
  // the last row remaining, in that case it hides the whole
  // table and shows the no elements alert div.
  var nrows = $("#"+table_name+" tr").length;
  if (nrows > 3) {
    $("#tr_"+table_name+"-"+appraisal_id).fadeOut()
  } else {
    $("#"+table_name).fadeOut()
    $("#div_alert_"+table_name).fadeToggle()
  }
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