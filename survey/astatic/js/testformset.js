function addLeaveRow() {
  var totalFormsField = $('#id_form-TOTAL_FORMS');
  var nextFormNum = parseInt(totalFormsField.val());

  $('#add_leave_row').addClass('disabled');
  $('#loading').show();

  $.ajax({
      url: '/leave/leave-form/' + nextFormNum + '/',
      type: 'GET'
  }).done(function(response) {
      $('#leaveRows').append(response);
      totalFormsField.val(nextFormNum + 1);
      updateLeaveTotal();
      $('#add_leave_row').removeClass('disabled');
      $('#loading').hide();
  }).fail(function(response, status, error) {
      alert(status + ': ' + error);
      $('#add_leave_row').removeClass('disabled');
      $('#loading').hide();
  });
}
function deleteLeaveRow(deleteLink) {
  var totalFormsField = $('#id_form-TOTAL_FORMS');
  var totalForms = parseInt(totalFormsField.val()) - 1;
  totalFormsField.val(totalForms);

  $(deleteLink).closest('.leaveForm').remove();

  // for formset functionality to work properly, need to update all existing form ids so they're sequential
  updateFormElementIndices('leaveForm');

  // Have to destroy and rebind all the datepicker elements, otherwise they will be bound to the wrong
  // form element as rows are added and removed.
  $('.datepicker').each(function() {
      $(this).datepicker('destroy');
      $(this).datepicker({altFormat:"yy-mm-dd"});
  });

  if (totalForms == 0) {
      $('#requestLeaveButton').addClass('disabled');
  }

  updateLeaveTotal();
}
function updateFormElementIndices(formClass) {
  var forms = $('.' + formClass);

  forms.each(function(i, el) {
      var curIndex = $(el).attr('id').match(/\d+/)[0];

      $(el).attr('id', $(el).attr('id').replace(curIndex, i));

      var inputs = $(el).find('.' + formClass + 'Input');

      inputs.each(function(j, input) {
          $(input).attr('id', $(input).attr('id').replace(curIndex, i));
          $(input).attr('name', $(input).attr('name').replace(curIndex, i));
      });
  });
}
