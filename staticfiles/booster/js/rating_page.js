$(document).ready(function () {

  function setInitialRating() {
    var initiallyCheckedInput = $('.rating-container input:checked');
    if (initiallyCheckedInput.length > 0) {
      var selectedRating = initiallyCheckedInput.attr('id').replace('rate', '');
      $('#rate').val(selectedRating).trigger('change');
    }
  }
  setInitialRating();
  
  $('.rating-container input').on('change', function () {
    var selectedRating = $(this).attr('id').replace('rate', '');
    $('#rate').val(selectedRating);
  });
});