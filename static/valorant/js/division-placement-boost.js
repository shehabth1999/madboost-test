// Array For Names 
const ranksNames = ['unrank', 'iron', 'bronze', 'silver', 'gold', 'platinum', 'diamond', 'ascendant', 'immortal'];

const divisionNames = [0, 'I', 'II', 'III']
// --------- If Customer Come After Choose Booster or For Extend Order ---------
// Get Params
// Assume you have a reference to the HTML element
const orderContainer = document.getElementById('order-container');
const urlParams = new URLSearchParams(window.location.search);
const extend_order = urlParams.get('extend');
let discount_amount = 0

// Access the data attribute and convert it to a JavaScript variable
const orderValue = orderContainer.dataset.order;

const valuesAsList = orderValue.split(',')
const list1 = valuesAsList.slice(0, 5);
const list2 = valuesAsList.slice(5, 10);

const valuesToSet = list1.map(function(item) {
  return parseInt(item, 10); // Use parseFloat if you have decimal numbers
});

const valuesToSetAdditional = list2.map(value => JSON.parse(value.toLowerCase()));

// Get the 'choose-booster' query parameter value from the URL
const chooseBoosterValue = urlParams.get('choose_booster');
let chooseBoosterInt = 0
let autoSelectBooster = $('input#select-booster');
if (chooseBoosterValue != null) {
  chooseBoosterInt = parseInt(chooseBoosterValue, 10);
  autoSelectBooster.val(true)
}
// Set the value of the input field to the obtained 'choose-booster' value
document.getElementById('chooseBoosterInput').value = chooseBoosterInt;

// Additional Initial Percent
var total_Percentage = 0;

// ----------------------------- Division Boost ---------------------------------

// Buttons
const radioButtonsCurrent = document.querySelectorAll('input[name="radio-group-current"]');
const radioButtonsDesired = document.querySelectorAll('input[name="radio-group-desired"]');
const radioButtonsCurrentDivision = document.querySelectorAll('input[name="radio-group-current-division"]');
const radioButtonsDesiredDivision = document.querySelectorAll('input[name="radio-group-desired-division"]');
const makrs_on_current_rank_selected = document.querySelector('.current-marks-select');
const division_server_select_element = document.querySelector('.division-servers-select');

// Disable Functions
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

// Slice Function
function sliceArray(array, start, end) {
  return array.slice(start, end + 1);
}

// Initail Values
const initiallyCheckedIndexCurrent = Array.from(radioButtonsCurrent).findIndex(radio => radio.checked) + 1;
const initiallyCheckedIndexDesired = Array.from(radioButtonsDesired).findIndex(radio => radio.checked) + 1;

const initiallyCheckedIndexCurrentDivision = Array.from(radioButtonsCurrentDivision).findIndex(radio => radio.checked) + 1;
const initiallyCheckedIndexDesiredDivision = Array.from(radioButtonsDesiredDivision).findIndex(radio => radio.checked) + 1;
const initiallyCheckedIndexMark = makrs_on_current_rank_selected.value;

// Read Values From Json File
let divisionPrices = [0];
let marks_price = [[0, 0, 0, 0, 0]];
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
  // Variable That I Use
  var current_rank = initiallyCheckedIndexCurrent;
  var desired_rank = initiallyCheckedIndexDesired;
  var current_division = initiallyCheckedIndexCurrentDivision;
  var desired_division = initiallyCheckedIndexDesiredDivision;
  var current_rank_name = ranksNames[initiallyCheckedIndexCurrent];
  var desired_rank_name = ranksNames[initiallyCheckedIndexDesired];
  var current_division_name = divisionNames[initiallyCheckedIndexCurrentDivision];
  var desired_division_name = divisionNames[initiallyCheckedIndexDesiredDivision];
  var number_of_mark = marks_price[current_rank][initiallyCheckedIndexMark];
  var mark = 0;
  var selectedDivsionServer = division_server_select_element.value;

  // Look Here:- I Want Get The Current & Desired Element Not Index
  let currentElement = Array.from(radioButtonsCurrent).find(radio => radio.checked);
  let desiredElement = Array.from(radioButtonsDesired).find(radio => radio.checked);

  // Extend
  if (extend_order) {
    let orderID = parseInt(extend_order, 10);
    document.getElementById('extendOrder').value = orderID; 

    // Set the checked state for each group of radio buttons using the specified order
    setRadioButtonStateWithDisable(radioButtonsCurrent, valuesToSet[0]-1);
    setRadioButtonStateWithDisable(radioButtonsCurrentDivision, valuesToSet[1]-1);
    setRadioButtonState(radioButtonsDesired, valuesToSet[3]-1, true);
    setRadioButtonStateForDesiredDivision(radioButtonsDesiredDivision, valuesToSet[4]-1);
    makrs_on_current_rank_selected.disabled = true
    division_server_select_element.disabled = true
    current_rank = valuesToSet[0];
    current_division = valuesToSet[1];
    desired_rank = valuesToSet[3];
    desired_division = valuesToSet[4];
    var current_rank_name = ranksNames[current_rank];
    var desired_rank_name = ranksNames[desired_rank];
    var current_division_name = divisionNames[current_division];
    var desired_division_name = divisionNames[desired_division];

    // Checkbox
    let extraOptions = document.querySelectorAll('input[name="extra-checkbox"]');

    // Solo Or Duo Boosting Change
    if (valuesToSetAdditional[0]) {
      document.querySelector('input[name="switch-between-solo-duo"][value="duo"]').checked = true;
      $('input#duoBoosting').val(true)
    } else {
      document.querySelector('input[name="switch-between-solo-duo"][value="solo"]').checked = true;
      $('input#duoBoosting').val(false)
    }

    // Disable Extra
    document.querySelector('input[name="switch-between-solo-duo"][value="duo"]').disabled = true;
    document.querySelector('input[name="switch-between-solo-duo"][value="solo"]').disabled = true;

    // Extra Buttons
    extraOptions.forEach(function (checkbox, index) {
      if (checkbox.value === "selectBooster" && valuesToSetAdditional[1]) {
        checkbox.checked = true
        $(`input#${checkbox.value}`).val(true)
        
      } else if (checkbox.value === "turboBoost" && valuesToSetAdditional[2]) {
        checkbox.checked = true
        $(`input#${checkbox.value}`).val(true)
      } else if (checkbox.value === "streaming" && valuesToSetAdditional[3]) {
        checkbox.checked = true
        $(`input#${checkbox.value}`).val(true)
      } else if (checkbox.value === "boosterChampions" && valuesToSetAdditional[4]) {
        checkbox.checked = true
        $(`input#${checkbox.value}`).val(true)
      } else {
        checkbox.checked = false
        $(`input#${checkbox.value}`).val(false)
      }
      // Disable Extra
      $(checkbox).prop('disabled', true)
    })

  }

  if(extend_order) {
    function getDivisionPrice() {
      const startRank = ((valuesToSet[3] - 1) * 3) + valuesToSet[4];
      const endRank = ((desired_rank - 1) * 3) + desired_division-1;
      const slicedArray = sliceArray(divisionPrices, startRank, endRank);
      const sum = slicedArray.reduce((accumulator, currentValue) => accumulator + currentValue, 0);

      let result_with_mark = sum

      if (sum !== 0) {
        result_with_mark = sum - number_of_mark;
      }

      // Apply extra charges to the result
      result_with_mark += result_with_mark * total_Percentage;
      // Apply promo code 
      result_with_mark -= result_with_mark * (discount_amount/100 )

      result_with_mark = parseFloat(result_with_mark.toFixed(2)); 

      let currentElement = Array.from(radioButtonsCurrent).find(radio => (radio.getAttribute('data-name')).toLowerCase() === (ranksNames[valuesToSet[3]]).toLowerCase());

      // Look Here:- We Change Everything Should Change Depend On Current & Desired Element
      $('.division-boost .current-rank-selected-img').attr('src', $(currentElement).data('img'))
      $('.division-boost .desired-rank-selected-img').attr('src', $(desiredElement).data('img'))

      $('.division-boost .current-selected-info').html(`${ranksNames[valuesToSet[3]]} ${divisionNames[valuesToSet[4]]} ${mark == 0 ? '0-20' : mark == 1 ? '21-40' : mark == 2 ? '41-60' : mark == 3 ? '61-80' : '81-100'} RR`);
      $('.division-boost .desired-selected-info').html(`${desired_rank_name} ${desired_division_name}`)

      $('.current').removeClass().addClass(`current ${ranksNames[valuesToSet[3]]}`)
      $('.desired').removeClass().addClass(`desired ${desired_rank_name}`)

      $('.total-price #division-boost-price').text(`$${result_with_mark}`)

      // From Value
      $('.division-boost input[name="current_rank"]').val(current_rank);
      $('.division-boost input[name="current_division"]').val(current_division);
      $('.division-boost input[name="marks"]').val(mark);
      $('.division-boost input[name="desired_rank"]').val(desired_rank);
      $('.division-boost input[name="desired_division"]').val(desired_division);
      $('.division-boost input[name="server"]').val(selectedDivsionServer);
      $('.division-boost input[name="price"]').val(result_with_mark);
    }
  } else {
    // Get Result Function
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
      $('.division-boost .current-rank-selected-img').attr('src', $(currentElement).data('img'))
      $('.division-boost .desired-rank-selected-img').attr('src', $(desiredElement).data('img'))

      $('.division-boost .current-selected-info').html(`${current_rank_name} ${current_division_name} ${mark == 0 ? '0-20' : mark == 1 ? '21-40' : mark == 2 ? '41-60' : mark == 3 ? '61-80' : '81-100'} RR`);
      $('.division-boost .desired-selected-info').html(`${desired_rank_name} ${desired_division_name}`)

      $('.current').removeClass().addClass(`current ${current_rank_name}`)
      $('.desired').removeClass().addClass(`desired ${desired_rank_name}`)

      $('.total-price #division-boost-price').text(`$${result_with_mark}`)
  
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
  }

  // Get Result 
  getDivisionPrice();

  // Current Rank Change
  radioButtonsCurrent.forEach(function (radio, index) {
    radio.addEventListener('change', function () {
      const selectedIndex = Array.from(radioButtonsCurrent).indexOf(radio);
      current_rank = selectedIndex + 1;
      current_rank_name = ranksNames[current_rank];

      // Look Here:- When Current Rank Change Change Value So Image Changed 
      currentElement = Array.from(radioButtonsCurrent).find(radio => radio.checked);

      makrs_on_current_rank_selected.value = 0; // make 0 mark is check
      getDivisionPrice();
    });
  });

  // Desired Rank Change
  radioButtonsDesired.forEach(function (radio, index) {
    radio.addEventListener('change', function () {
      const selectedIndex = Array.from(radioButtonsDesired).indexOf(radio);
      desired_rank = selectedIndex + 1;
      desired_rank_name = ranksNames[desired_rank]

      // Look Here:- When Desired Rank Change Change Value So Image Changed 
      desiredElement = Array.from(radioButtonsDesired).find(radio => radio.checked);
      
      getDivisionPrice();
    });
  });

  // Current Division Change
  radioButtonsCurrentDivision.forEach(function (radio, index) {
    radio.addEventListener('change', function () {
      const selectedIndex = Array.from(radioButtonsCurrentDivision).indexOf(radio);
      current_division = selectedIndex + 1;
      current_division_name = divisionNames[current_division]
      getDivisionPrice();
    });
  })

  // Desired Division Change
  radioButtonsDesiredDivision.forEach(function (radio, index) {
    radio.addEventListener('change', function () {
      const selectedIndex = Array.from(radioButtonsDesiredDivision).indexOf(radio);
      desired_division = selectedIndex + 1;
      desired_division_name = divisionNames[desired_division]
      getDivisionPrice()
    });
  });

  // Mark Changes
  makrs_on_current_rank_selected.addEventListener("change", function() {
    const selectedIndex = this.value;
    number_of_mark = marks_price[current_rank][selectedIndex];
    mark = selectedIndex
    getDivisionPrice();
  });

  // Server Changes
  division_server_select_element.addEventListener("change", function() {
    selectedDivsionServer = this.value
    getDivisionPrice();
  });

  
  // ----------------------------- Placments Boost ---------------------------------
  const placementsRanks = $('input[name="placement-ranks"]');
  const gameCountInput = $("#game-count");
  const steps = $('.step-indicator .step');
  const gameCounterInitial = Number(gameCountInput.val())
  const initiallyCheckedIndexRank = $('input[name="placement-ranks"]').index($('input[name="placement-ranks"]:checked'));
  const initiallyCheckedRank = $('input[name="placement-ranks"]').eq(initiallyCheckedIndexRank);
  const initiallyCheckedIndexRankPrice = initiallyCheckedRank.data('price');
  const placement_server_select_element = $('.placement-servers-select');
  
  let perviousElement = Array.from(placementsRanks).find(radio => radio.checked);
  
  let pervious_rank = initiallyCheckedIndexRank
  let pervious_rank_name = ranksNames[pervious_rank]
  let rank_price = initiallyCheckedIndexRankPrice
  let gameCounter = gameCounterInitial
  let selectedPlacementServer = placement_server_select_element.val()
  
  const getPlacementPrice = () => {
    let price = (rank_price * gameCounter);
    // Apply extra charges to the result
    price = price + (price * total_Percentage)
    // Apply promo code 
    price -= price * (discount_amount / 100 )
  
    price = parseFloat(price.toFixed(2))
  
    // Look Here:- We Change Everything Should Change Depend On Current & Desired Element
    $('.placements-boost .pervious-rank-selected-img').attr('src', $(perviousElement).data('img'))
    $('.num-of-match').text(gameCounter);

    $('.placements-boost .pervious-selected-info').html(`${pervious_rank_name}`)
    $('.placements-boost .game_count-selected-info').html(`${gameCounter} Matches`)
  
    $('.pervious').removeClass().addClass(`pervious ${pervious_rank_name}`);

    $('.total-price #placements-boost-price').text(`$${price}`)
  
    const pricee = $('.price-data.placements-boost').eq(0);
    pricee.html(`
    <p class='fs-5 text-uppercase my-4'>Boosting of <span class='fw-bold'>${gameCounter} Placement Games</span></p>
    <h4>$${price}</h4>
    `);
  
    if ($('.placements-boost input[name="game_type"]').val() == 'P') {
      $('.placements-boost input[name="last_rank"]').val(pervious_rank);
      $('.placements-boost input[name="number_of_match"]').val(gameCounter);
      $('.placements-boost input[name="server"]').val(selectedPlacementServer);
      $('.placements-boost input[name="price"]').val(price);
    }
  }

  getPlacementPrice()
  
  placementsRanks.each(function (index, radio) {
    $(radio).on('change', function () {
      const selectedIndex = placementsRanks.index(radio);
      pervious_rank = selectedIndex;
      pervious_rank_name = ranksNames[pervious_rank]
      rank_price = $(radio).data('price');

      // Look Here:- When Desired Rank Change Change Value So Image Changed 
      perviousElement = Array.from(placementsRanks).find(radio => radio.checked);

      getPlacementPrice()
    });
  });
  
  gameCountInput.on("input", function (event) {
    gameCounter = Number(event.target.value);
    
    const progress = ((gameCounter - 1) / (gameCountInput.prop("max") - 1)) * 100;
  
    gameCountInput.css({
      "background": `linear-gradient(to right, #F36E3F ${progress}%, #251D16 ${progress}%)`
    });
  
    steps.each((step, index) => {
      var $step = $(step);
      if (index < gameCounter) {
        $step.addClass('selected');
      } else {
        $step.removeClass('selected');
      }
    });
  
    getPlacementPrice()
  
  })

  // Server Changes
  placement_server_select_element.on("change", function() {

    selectedPlacementServer = $(this).val();
    getPlacementPrice();
  });

  // ----------------------------- Others ---------------------------------
  // Extra Charges Part
  // Additional Initial Percent
  let percentege = {
    duoBoosting: 0.65,
    selectBooster: 0.10,
    turboBoost: 0.20,
    streaming: 0.15,
    boosterAgents: 0.0
  }

  // Checkbox
  let soloOrDuoBoosting = document.querySelectorAll('input[name="switch-between-solo-duo"]');
  let extraOptions = document.querySelectorAll('input[name="extra-checkbox"]');

  // Solo Or Duo Boosting Change
  soloOrDuoBoosting.forEach(function (radio, index) {
    radio.addEventListener('change', function () {
      if (this.value === "duo") {
        total_Percentage += percentege.duoBoosting;
        $('input#duoBoosting').val(true)
      } else {
        total_Percentage -= percentege.duoBoosting;
        $('input#duoBoosting').val(false)
      }

      getDivisionPrice()
      getPlacementPrice()
    }) 
  })

  // Extra Buttons
  extraOptions.forEach(function (checkbox, index) {
    checkbox.addEventListener('change', function () {
      if (this.checked) {
        total_Percentage += percentege[this.value];
        $(`input#${this.value}`).val(true)
      } else {
        total_Percentage -= percentege[this.value];
        $(`input#${this.value}`).val(false)
      }
    
      getDivisionPrice()
      getPlacementPrice()
    })
  });
  
 
  const form = document.querySelector('.discount form');

  form.addEventListener('submit', function(event) {
    event.preventDefault();

    const discountInput = document.querySelector('input[name="discount"]');
    const discountCode = discountInput.value.trim();
    const promoDetails = $('#promo-details h6');
    $('input[id="promo_send"]').val(discountCode);

    if (discountCode) {
      const csrfToken = getCookie('csrftoken');
      $.ajax({
        url: '/accounts/promo-codes/',
        type: 'POST',
        headers: {
          'X-CSRFToken': csrfToken
        },
        contentType: 'application/json',
        data: JSON.stringify({ code: discountCode }),
        success: function(data) {
          promoDetails.css('visibility', 'visible');
          promoDetails.text(data.description);
          promoDetails.css('color', 'green');
          discount_amount = data.discount_amount;
          getDivisionPrice();
          getPlacementPrice()
        },
        error: function(xhr, textStatus, errorThrown) {
          promoDetails.css('visibility', 'visible');
          promoDetails.text(xhr.responseJSON.error);
          promoDetails.css('color', 'red');
          discount_amount = 0;
          getDivisionPrice();
          getPlacementPrice();
        }
      });
        
    } else {
      $('input[id="promo_send"]').val('null');
      promoDetails.css('visibility', 'visible');
      promoDetails.text('Please enter a discount code');
      promoDetails.css('color', 'red');
      discount_amount = 0;
      getDivisionPrice();
      getPlacementPrice();
    }
  });

  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        // Check if the cookie name matches the CSRF cookie name
        if (cookie.startsWith(name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
});