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