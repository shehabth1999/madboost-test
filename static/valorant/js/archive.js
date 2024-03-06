function getDivisionPrice() {
  const startRank = ((current_rank - 1) * 3) + current_division;
  const endRank = ((desired_rank - 1) * 3) + desired_division - 1;
  const slicedArray = sliceArray(divisionPrices, startRank, endRank);
  const result = slicedArray.reduce((accumulator, currentValue) => accumulator + currentValue, 0);

  let result_with_mark = result

  if (result !== 0) {
    result_with_mark = result - number_of_mark;
  }

  // Apply extra charges to the result
  result_with_mark += result_with_mark * total_Percentage;
  // Apply promo code 
  result_with_mark -= result_with_mark * (discount_amount/100 )

  result_with_mark = parseFloat(result_with_mark.toFixed(2)); 

  // Look Here:- We Change Everything Should Change Depend On Current & Desired Element
  $('.current-rank-selected-img').attr('src', $(currentElement).data('img'))
  $('.desired-rank-selected-img').attr('src', $(desiredElement).data('img'))

  $('.current-selected-info').html(`${current_rank_name} ${current_division_name} ${mark == 0 ? '0-20' : mark == 1 ? '21-40' : mark == 2 ? '41-60' : mark == 3 ? '61-80' : '81-100'} RR`);
  $('.desired-selected-info').html(`${desired_rank_name} ${desired_division_name}`)

  $('.current').removeClass().addClass(`current ${current_rank_name}`)
  $('.desired').removeClass().addClass(`desired ${desired_rank_name}`)

  $('.total-price #price').text(`$${result_with_mark}`)

  // From Value
  if ($('.division-boost input[name="game_type"]').val() == 'D') {
    $('.division-boost input[name="current_rank"]').val(current_rank);
    $('.division-boost input[name="current_division"]').val(current_division);
    $('.division-boost input[name="marks"]').val(mark);
    $('.division-boost input[name="desired_rank"]').val(desired_rank);
    $('.division-boost input[name="desired_division"]').val(desired_division);
    $('.division-boost input[name="server"]').val(selectedDivsionServer);
    $('.division-boost input[name="price"]').val(result_with_mark);
  }
}




var total_Percentage = 0;
// Assume you have a reference to the HTML element
// const orderContainer = document.getElementById('order-container');
// const urlParams = new URLSearchParams(window.location.search);
// const extend_order = urlParams.get('extend');

// Access the data attribute and convert it to a JavaScript variable
// const orderValue = orderContainer.dataset.order;

// const valuesAsList = orderValue.split(',')
// const list1 = valuesAsList.slice(0, 5);
// const list2 = valuesAsList.slice(5, 9);

// const valuesToSet = list1.map(function(item) {
//   return parseInt(item, 10); // Use parseFloat if you have decimal numbers
// });

// const valuesToSetAdditional = list2.map(value => JSON.parse(value.toLowerCase()));
// console.log(valuesAsList)
// console.log(valuesToSetAdditional)
// console.log(valuesToSet);

const radioButtonsCurrent = document.querySelectorAll('input[name="radio-group-current"]');
const radioButtonsDesired = document.querySelectorAll('input[name="radio-group-desired"]');
const radioButtonsCurrentDivision = document.querySelectorAll('input[name="radio-group-current-division"]');
const radioButtonsDesiredDivision = document.querySelectorAll('input[name="radio-group-desired-division"]');
const makrs_on_current_rank_checked = document.querySelectorAll('input[name="radio-group-current-mark"]');

const makrs_on_current_rank = document.querySelectorAll('.current-mark-container');

function setRadioButtonStateWithDisable(radioButtons, values) {
  radioButtons.forEach((radio, index) => {
    // Assuming values in the specified order correspond to radio button indices
    radio.checked = (index === values);
    radio.disabled = true;
  });
}
function setRadioButtonState(radioButtons, values) {
radioButtons.forEach((radio, index) => {
  radio.checked = (index === values);
  if (index<values){
    radio.disabled = true;
  }
});
}
function setRadioButtonStateForDesiredDivision(radioButtons, values) {
radioButtons.forEach((radio, index) => {
    radio.checked = (index === values);
});
}

const initiallyCheckedIndexCurrent = Array.from(radioButtonsCurrent).findIndex(radio => radio.checked) + 1;
const initiallyCheckedIndexDesired = Array.from(radioButtonsDesired).findIndex(radio => radio.checked) + 1;

const initiallyCheckedIndexCurrentDivision = Array.from(radioButtonsCurrentDivision).findIndex(radio => radio.checked) + 1;
const initiallyCheckedIndexDesiredDivision = Array.from(radioButtonsDesiredDivision).findIndex(radio => radio.checked) + 1;
const initiallyCheckedIndexMark = Array.from(makrs_on_current_rank_checked).findIndex(radio => radio.checked);

if (initiallyCheckedIndexCurrent !== -1 && initiallyCheckedIndexDesired !== -1 && initiallyCheckedIndexCurrentDivision !== -1
  && initiallyCheckedIndexDesiredDivision !== -1) {
  console.log('Initially checked index For Current:', initiallyCheckedIndexCurrent);
  console.log('Initially checked index For Desired:', initiallyCheckedIndexDesired);
  console.log('Initially checked index For CurrentDivision :', initiallyCheckedIndexCurrentDivision);
  console.log('Initially checked index For CurrentDivision:', initiallyCheckedIndexDesiredDivision);
} else {
  console.log('No radio buttons is initially checked.');
}


function sliceArray(array, start, end) {
  return array.slice(start, end + 1);
}

let divisionPrices = [0];
let marks_price = [[0, 0, 0, 0, 0, 0]];
Promise.all([
  new Promise(function (resolve, reject) {
    $.getJSON('/static/valorant/data/divisions_data.json', function (data) {
      divisionPrices = divisionPrices.concat(...data);
      resolve();
    });
  }),
  new Promise(function (resolve, reject) {
    $.getJSON('/static/valorant/data/marks_data.json', function (data) {
      marks_price = marks_price.concat(data.slice(0));
      resolve();
    });
  })
]).then(function () {
  const divisionRanks = ['', 'iron', 'bronze', 'silver', 'gold', 'platinum', 'emerald', 'diamond', 'master'];

  const divisionNames = [0, 'I', 'II', 'III']

  var current_rank = initiallyCheckedIndexCurrent;
  var desired_rank = initiallyCheckedIndexDesired;
  var current_division = initiallyCheckedIndexCurrentDivision;
  var desired_division = initiallyCheckedIndexDesiredDivision;
  var current_rank_name = divisionRanks[initiallyCheckedIndexCurrent];
  var desired_rank_name = divisionRanks[initiallyCheckedIndexDesired];
  var current_division_name = divisionNames[initiallyCheckedIndexCurrentDivision];
  var desired_division_name = divisionNames[initiallyCheckedIndexDesiredDivision];
  var number_of_mark = marks_price[current_rank][initiallyCheckedIndexMark];
  var mark = 0

  $.getJSON('/static/wildRift/data/marks_data.json', function (data) {
    marks_price = marks_price.concat(data.slice(1));
    number_of_mark = marks_price[current_rank][initiallyCheckedIndexMark];
    getResult();
  });

// ################################# Extra Charges Part #################################
const buttons = {
  duoBoosting: document.querySelector('#duoBoostingButton'),
  selectBooster: document.querySelector('#selectBoosterButton'),
  turboBoost: document.querySelector('#turboBoostButton'),
  streaming: document.querySelector('#streamingButton'),
};

  const contents = {
    duoBoosting: document.querySelector('.duoBoostingContent'),
    selectBooster: document.querySelector('.selectBoosterContent'),
    turboBoost: document.querySelector('.turboBoostContent'),
    streaming: document.querySelector('.streamingContent'),
  };

  const Applybuttons = {
    duoBoosting: document.querySelector('#duoBoostingApplyButton'),
    selectBooster: document.querySelector('#selectBoosterApplyButton'),
    turboBoost: document.querySelector('#turboBoostApplyButton'),
    streaming: document.querySelector('#streamingApplyButton'),
  };

  // Toggle Function
  function toggleContent(content) {
    for (const key in contents) {
      contents[key].style.display = key === content && contents[key].style.display !== 'block' ? 'block' : 'none';
    }
  }

  // Toggle click event
  function setupButtonClickEvent(button, content) {
    button.addEventListener('click', function () {
      toggleContent(content);
    });
  }

  function updateTotalPercentage(percentage, add = true, button) {
    let buttonOldName = buttons[button].innerHTML
    if (add) {
      total_Percentage += percentage;
      $(`#${button}`).val(true);
      buttons[button].innerHTML = '<i class="fa-solid fa-check"></i>' + buttonOldName;
      Applybuttons[button].innerHTML = 'Cancel'
      Applybuttons[button].classList.remove('applyButton');
      Applybuttons[button].classList.add('cancelButton');
    } else {
      $(`#${button}`).val(false);
      total_Percentage -= percentage;
      buttons[button].innerHTML = buttonOldName.replace('<i class="fa-solid fa-check"></i>', '');
      Applybuttons[button].innerHTML = 'Apply'
      Applybuttons[button].classList.remove('cancelButton');
      Applybuttons[button].classList.add('applyButton');
    }
  }

  // Apply Button
  function setupApplyButtonClickEvent(button, percentage) {
    Applybuttons[button].addEventListener('click', function () {
      updateTotalPercentage(percentage, !Applybuttons[button].classList.contains('cancelButton'), button);
      getResult();
      getPrices();
    });
  }

  // Setup click events for each button
  for (const key in buttons) {
    setupButtonClickEvent(buttons[key], key);
  }
  setupApplyButtonClickEvent('duoBoosting', 0.65);
  setupApplyButtonClickEvent('selectBooster', 0.05);
  setupApplyButtonClickEvent('turboBoost', 0.20);
  setupApplyButtonClickEvent('streaming', 0.15);

  // Get the 'choose-booster' query parameter value from the URL
  // const chooseBoosterValue = urlParams.get('choose_booster');
  // let chooseBoosterInt = 0
  // let autoSelectBooster = document.getElementById('selectBoosterApplyButton')
  // if (chooseBoosterValue != null){
  //   chooseBoosterInt = parseInt(chooseBoosterValue, 10);
  //   autoSelectBooster.click()
  // }
  // Set the value of the input field to the obtained 'choose-booster' value
  // document.getElementById('chooseBoosterInput').value = chooseBoosterInt;

  // if (extend_order) {
  //   let orderID = parseInt(extend_order, 10);
  //   document.getElementById('extendOrder').value = orderID; 

  //   // Set the checked state for each group of radio buttons using the specified order
  //   setRadioButtonStateWithDisable(radioButtonsCurrent, valuesToSet[0]-1);
  //   setRadioButtonStateWithDisable(radioButtonsCurrentDivision, valuesToSet[1]-1);
  //   setRadioButtonStateWithDisable(makrs_on_current_rank_checked, valuesToSet[2]);
  //   setRadioButtonState(radioButtonsDesired, valuesToSet[3]-1, true);
  //   setRadioButtonStateForDesiredDivision(radioButtonsDesiredDivision, valuesToSet[4]-1);
  //   current_rank = valuesToSet[0];
  //   current_division = valuesToSet[1];
  //   desired_rank = valuesToSet[3];
  //   desired_division = valuesToSet[4];
  //   var current_rank_name = divisionRanks[current_rank];
  //   var desired_rank_name = divisionRanks[desired_rank];
  //   var current_division_name = divisionNames[current_division];
  //   var desired_division_name = divisionNames[desired_division];

  //   let duoBoostingApply= document.getElementById('duoBoostingApplyButton')
  //   let turboBoostApply = document.getElementById('turboBoostApplyButton')
  //   let streamingApply = document.getElementById('streamingApplyButton')

  //   // Function to set checkbox state based on values
  //   function setCheckboxState(checkbox, value) {
  //     if (value === true){
  //       checkbox.click();
  //       console.log("hi")
  //     }
  //   }
  //   // Set the state of each checkbox based on the values list
  //   setCheckboxState(duoBoostingApply, valuesToSetAdditional[0]);
  //   setCheckboxState(autoSelectBooster, valuesToSetAdditional[1]);
  //   setCheckboxState(turboBoostApply, valuesToSetAdditional[2]);
  //   setCheckboxState(streamingApply, valuesToSetAdditional[3]);
  // }

  // if(extend_order) {
  //   function getResult() {
  //     // console.log('Hi')
  //     const startt = ((valuesToSet[3] - 1) * 4) + valuesToSet[4];
  //     const endd = ((desired_rank - 1) * 4) + desired_division-1;
  //     const slicedArray = sliceArray(divisionPrices, startt, endd);
  //     const summ = slicedArray.reduce((accumulator, currentValue) => accumulator + currentValue, 0);
  //     console.log(slicedArray)
  //     console.log(divisionPrices)

  //     let result_with_mark = summ

  //     if (summ !== 0) {
  //       result_with_mark = summ - number_of_mark;
  //     }

  //     // Apply extra charges to the result
  //     result_with_mark += result_with_mark * total_Percentage;
  //     result_with_mark = parseFloat(result_with_mark.toFixed(2)); 

  //     const pricee = document.querySelector('.price-data.division-boost');
  //     pricee.innerHTML = `
  //     <p class='fs-5 text-uppercase my-4'>Boosting <span class='fw-bold'>From ${current_rank_name} ${current_division_name} Marks ${valuesToSet[2]} to ${divisionRanks[valuesToSet[3]]} ${divisionNames[valuesToSet[4]] != 'master' ? divisionNames[valuesToSet[4]] : ''} </span></p>
  //     <p class='fs-5 text-uppercase my-4'>Extend <span class='fw-bold'>From ${divisionRanks[valuesToSet[3]]} ${divisionNames[valuesToSet[4]]} Marks ${mark} to ${desired_rank_name} ${desired_rank_name != 'master' ? desired_division_name : ''} </span></p>
  //     <span class='fs-5 text-uppercase fw-bold'>Extra Cost: $${result_with_mark}</span>
  //   `;

  //     // From Value
  //     $('input[name="current_rank"]').val(current_rank);
  //     $('input[name="current_division"]').val(current_division);
  //     $('input[name="marks"]').val(mark);
  //     $('input[name="desired_rank"]').val(desired_rank);
  //     $('input[name="desired_division"]').val(desired_division);
  //     $('input[name="price"]').val(result_with_mark);
  //   }
  // }
  // else{
    function getResult() {
      const startt = ((current_rank - 1) * 4) + current_division;
      const endd = ((desired_rank - 1) * 4) + desired_division-1;
      const slicedArray = sliceArray(divisionPrices, startt, endd);
      const summ = slicedArray.reduce((accumulator, currentValue) => accumulator + currentValue, 0);

      let result_with_mark = summ

      if (summ !== 0) {
        result_with_mark = summ - number_of_mark;
      }

      // Apply extra charges to the result
      result_with_mark += result_with_mark * total_Percentage;
      result_with_mark = parseFloat(result_with_mark.toFixed(2)); 

      const pricee = document.querySelector('.price-data.division-boost');
      pricee.innerHTML = `
      <p class='fs-5 text-uppercase my-4'>Boosting <span class='fw-bold'>From ${current_rank_name} ${current_division_name} Marks ${mark} to ${desired_rank_name} ${desired_rank_name != 'master' ? desired_division_name : ''} </span></p>
      <span class='fs-5 text-uppercase fw-bold'>Total Cost: $${result_with_mark}</span>
    `;

      // From Value
      $('input[name="current_rank"]').val(current_rank);
      $('input[name="current_division"]').val(current_division);
      $('input[name="marks"]').val(mark);
      $('input[name="desired_rank"]').val(desired_rank);
      $('input[name="desired_division"]').val(desired_division);
      $('input[name="price"]').val(result_with_mark);
    }
  // }

  getResult();


  function setMarkNumber() {
    let number_of_marks = -1; // num of marks
    switch (current_rank) {
      case 1:
        number_of_marks = 2;
        break;
      case 2:
      case 3:
        number_of_marks = 3;
        break;
      case 4:
      case 5:
        number_of_marks = 4;
        break;
      case 6:
        number_of_marks = 5;
        break;
      case 7:
        number_of_marks = -1;
        break;
      default:
        number_of_marks = -1;
    }
    makrs_on_current_rank.forEach(function (element, index) {
      if (index <= number_of_marks) {
        element.classList.remove('d-none');
      } else {
        element.classList.add('d-none');
      }
    });

  }
  setMarkNumber();

  radioButtonsCurrent.forEach(function (radio, index) {
    radio.addEventListener('change', function () {
      const selectedIndex = Array.from(radioButtonsCurrent).indexOf(radio);
      current_rank = selectedIndex + 1;
      current_rank_name = divisionRanks[current_rank];
      makrs_on_current_rank_checked[0].checked = true; // make 0 mark is check
      setMarkNumber();
      getResult();
    });
  });

  radioButtonsDesired.forEach(function (radio, index) {
    radio.addEventListener('change', function () {
      const selectedIndex = Array.from(radioButtonsDesired).indexOf(radio);
      desired_rank = selectedIndex + 1;
      desired_rank_name = divisionRanks[desired_rank]
      const desired_division_to_hide = document.getElementById('desired-division');
      if (desired_rank == 8) {
        desired_division_to_hide.classList.add('d-none');
        let desired_division_IV = document.getElementById("desired-division0")
        desired_division_IV.checked = true;
      }
      else {
        desired_division_to_hide.classList.remove('d-none');
      }
      getResult();
    });
  });

  radioButtonsCurrentDivision.forEach(function (radio, index) {
    radio.addEventListener('change', function () {
      const selectedIndex = Array.from(radioButtonsCurrentDivision).indexOf(radio);
      current_division = selectedIndex + 1;
      current_division_name = divisionNames[current_division]
      getResult();
    });
  });

  radioButtonsDesiredDivision.forEach(function (radio, index) {
    radio.addEventListener('change', function () {
      const selectedIndex = Array.from(radioButtonsDesiredDivision).indexOf(radio);
      desired_division = selectedIndex + 1;
      desired_division_name = divisionNames[desired_division]
      getResult()
    });
  });

  makrs_on_current_rank_checked.forEach(function (radio, index) {
    radio.addEventListener('change', function () {
      const selectedIndex = Array.from(makrs_on_current_rank_checked).indexOf(radio);
      number_of_mark = marks_price[current_rank][selectedIndex];
      mark = selectedIndex
      getResult();
    });
  });
});


// ################################ Placments Boost ################################
const radioButtonsRank = $('input[name="radio-group-ranks"]');
const sliderEl = $("#game-count");
const sliderValue = $(".value");
const gameCounterInitial = Number(sliderEl.val())
const initiallyCheckedIndexRank = $('input[name="radio-group-ranks"]').index($('input[name="radio-group-ranks"]:checked'));
const initiallyCheckedRank = $('input[name="radio-group-ranks"]').eq(initiallyCheckedIndexRank);
const initiallyCheckedIndexRankPrice = initiallyCheckedRank.data('price');

let rank = initiallyCheckedIndexRank
let rank_price = initiallyCheckedIndexRankPrice
let gameCounter = gameCounterInitial


const getPrices = () => {
let price = (rank_price * gameCounter);
price = parseFloat(price + (price * total_Percentage)).toFixed(2)
const pricee = $('.price-data.placements-boost').eq(0);
pricee.html(`
<p class='fs-5 text-uppercase my-4'>Boosting of <span class='fw-bold'>${gameCounter} Placement Games</span></p>
<h4>$${price}</h4>
`);
}
getPrices()

radioButtonsRank.each(function (index, radio) {
$(radio).on('change', function () {
  const selectedIndex = radioButtonsRank.index(radio);
  rank = selectedIndex;
  rank_price = $(radio).data('price');
  getPrices()
});
});


sliderEl.on("input", function (event) {
gameCounter = Number(event.target.value);

sliderValue.text(gameCounter);

const progress = (gameCounter / sliderEl.prop("max")) * 100;

sliderEl.css("background", `linear-gradient(to right, var(--main-color) ${progress}%, #ccc ${progress}%)`);

sliderEl.css("--thumb-rotate", `${(gameCounter / 100) * 2160}deg`);

getPrices()
});