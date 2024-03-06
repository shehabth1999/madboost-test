// spans = document.querySelectorAll('span');
// for (var j = 0; j < spans.length; j++) {
//     spans[j].classList.add('d-block');
// }

labels = document.querySelectorAll('label');

for (var i = 0; i < labels.length; i++) {
    labels[i].classList.add('form-label', 'custom-label');
    labels[i].classList.add('mt-3')
}

// Add specific styling for labels associated with checkboxes
checkboxLabels = document.querySelectorAll('label input[type="checkbox"]');
for (var i = 0; i < checkboxLabels.length; i++) {
    var checkboxLabel = checkboxLabels[i].parentNode;
    checkboxLabel.classList.add('checkbox-label');
}

// Remove unnecessary classes for checkbox labels
$('.checkbox-label').removeClass('form-label mt-3');

$('.custom-label[for="image-clear_id"]').removeClass('form-label')
$('.custom-label[for="image-clear_id"]').removeClass('mt-3')

textArea=document.querySelectorAll('textarea');
for (var i = 0; i < textArea.length; i++) {
    textArea[i].classList.add('form-control', 'custom-textarea');
    textArea[i].setAttribute('rows', '3');
}

inputs = document.querySelectorAll('input');
for (var i = 0; i < inputs.length; i++) {
    inputs[i].classList.add('form-control', 'custom-input');
    inputs[i].removeAttribute('required');
}

selects= document.querySelectorAll('select')
  
  for (var d =0; d < selects.length; d++){
    selects[d].classList.add('form-control', 'custom-select');
}

divs = document.getElementsByClassName("form_element")
for (var d =0; d < divs.length; d++){
    divs[d].classList.add('mb-3')
}

checkboxex=document.querySelectorAll('input[type="checkbox"]')
for (var d =0; d < checkboxex.length; d++){
    checkboxex[d].classList.remove('form-control')
}

errors = document.querySelectorAll('ul.errorlist')
for (var m=0 ; m < errors.length; m++){
    errors[m].classList.add('text-danger','mb-0', 'p-0')
    errors[m].querySelector('li').classList.add('list-group-item')
}

var inputs = document.querySelectorAll('input.form-control');
for (var i = 0; i < inputs.length; i++) {
  var input = inputs[i];
  var errorList = input.previousElementSibling;
  if (errorList && errorList.classList.contains('errorlist')) {
    input.parentNode.insertBefore(errorList, input.nextSibling);
  }
}