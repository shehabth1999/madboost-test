// Array For Names 
const ranksNames = ['unrank', 'bronze', 'silver', 'gold', 'platinum', 'diamond', 'champion', 'grand champion', 'supersonic legend']

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
const list2 = valuesAsList.slice(5, 9);

const valuesToSet = list1.map(function(item) {
  return parseInt(item, 10); // Use parseFloat if you have decimal numbers
});

const valuesToSetAdditional = list2.map(value => JSON.parse(value.toLowerCase()));
console.log(valuesAsList)
console.log(valuesToSetAdditional)
console.log(valuesToSet);

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
let total_Percentage = 0;

// ----------------------------- Division Boost ---------------------------------

//  Buttons
const radioButtonsCurrent = document.querySelectorAll('input[name="radio-group-current"]');
const radioButtonsDesired = document.querySelectorAll('input[name="radio-group-desired"]');
const radioButtonsCurrentDivision = document.querySelectorAll('input[name="radio-group-current-division"]');
const radioButtonsDesiredDivision = document.querySelectorAll('input[name="radio-group-desired-division"]');
const queue_type_selected = document.querySelector('.queue-type-select');
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
// 
const initiallyCheckedIndexCurrent = Array.from(radioButtonsCurrent).findIndex(radio => radio.checked) + 1;
const initiallyCheckedIndexDesired = Array.from(radioButtonsDesired).findIndex(radio => radio.checked) + 1;

const initiallyCheckedIndexCurrentDivision = Array.from(radioButtonsCurrentDivision).findIndex(radio => radio.checked) + 1;
const initiallyCheckedIndexDesiredDivision = Array.from(radioButtonsDesiredDivision).findIndex(radio => radio.checked) + 1;

// Read Values From Json File
let divisionPrices = [0];
Promise.all([
  new Promise(function (resolve, reject) {
    $.getJSON('/static/rocketLeague/data/divisions_data.json', function (data) {
      divisionPrices = divisionPrices.concat(...data);
      resolve();
    });
  })
]).then(function () {
  // Variable That I Use 
  let current_rank = initiallyCheckedIndexCurrent;
  let desired_rank = initiallyCheckedIndexDesired;
  let current_division = initiallyCheckedIndexCurrentDivision;
  let desired_division = initiallyCheckedIndexDesiredDivision;
  let current_rank_name = ranksNames[initiallyCheckedIndexCurrent];
  let desired_rank_name = ranksNames[initiallyCheckedIndexDesired];
  let current_division_name = divisionNames[initiallyCheckedIndexCurrentDivision];
  let desired_division_name = divisionNames[initiallyCheckedIndexDesiredDivision];
  let queue_type = queue_type_selected.value
  let selectedDivsionServer = division_server_select_element.value;

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
    queue_type_selected.disabled = true
    division_server_select_element.disabled = true
    current_rank = valuesToSet[0];
    current_division = valuesToSet[1];
    desired_rank = valuesToSet[3];
    desired_division = valuesToSet[4];
    current_rank_name = ranksNames[current_rank];
    desired_rank_name = ranksNames[desired_rank];
    current_division_name = divisionNames[current_division];
    desired_division_name = divisionNames[desired_division];

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

  if (extend_order) {
    function getDivisionPrice() {
      const startRank = ((valuesToSet[3] - 1) * 3) + valuesToSet[4];
      const endRank = ((desired_rank - 1) * 3) + desired_division-1;
      const slicedArray = sliceArray(divisionPrices, startRank, endRank);
      const sum = slicedArray.reduce((accumulator, currentValue) => accumulator + currentValue, 0);

      let result = sum

      // Apply extra charges to the result
      result += result * total_Percentage;
      // Apply promo code 
      result -= result * (discount_amount/100 )

      result = parseFloat(result.toFixed(2)); 

      let currentElement = Array.from(radioButtonsCurrent).find(radio => (radio.getAttribute('data-name')).toLowerCase() === (ranksNames[valuesToSet[3]]).toLowerCase());

      // Look Here:- We Change Everything Should Change Depend On Current & Desired Element
      $('.division-boost .current-rank-selected-img').attr('src', $(currentElement).data('img'))
      $('.division-boost .desired-rank-selected-img').attr('src', $(desiredElement).data('img'))

      $('.division-boost .current-selected-info').html(`${ranksNames[valuesToSet[3]]} ${divisionNames[valuesToSet[4]]}`);
      $('.division-boost .desired-selected-info').html(`${desired_rank_name} ${desired_division_name}`)

      $('.current').removeClass().addClass(`current ${ranksNames[valuesToSet[3]].replace(/\s+/g, '-')}`)
      $('.desired').removeClass().addClass(`desired ${desired_rank_name.replace(/\s+/g, '-')}`)

      $('.total-price #division-boost-price').text(`$${result}`)

      // From Value
      $('.division-boost input[name="current_rank"]').val(current_rank);
      $('.division-boost input[name="current_division"]').val(current_division);
      $('.division-boost input[name="queue_type"]').val(queue_type);
      $('.division-boost input[name="desired_rank"]').val(desired_rank);
      $('.division-boost input[name="desired_division"]').val(desired_division);
      $('.division-boost input[name="server"]').val(selectedDivsionServer);
      $('.division-boost input[name="price"]').val(result);
    }
  } else {
    // Get Result Function
    function getDivisionPrice() {
      const startRank = ((current_rank - 1) * 3) + current_division;
      const endRank = ((desired_rank - 1) * 3) + desired_division - 1;
      const slicedArray = sliceArray(divisionPrices, startRank, endRank);
      const sum = slicedArray.reduce((accumulator, currentValue) => accumulator + currentValue, 0);
  
      let result = sum
  
      // Apply extra charges to the result
      result += result * total_Percentage;
      // Apply promo code 
      result -= result * (discount_amount/100 )

      result = parseFloat(result.toFixed(2)); 

      // Look Here:- We Change Everything Should Change Depend On Current & Desired Element
      $('.division-boost .current-rank-selected-img').attr('src', $(currentElement).data('img'))
      $('.division-boost .desired-rank-selected-img').attr('src', $(desiredElement).data('img'))

      $('.division-boost .current-selected-info').html(`${current_rank_name} ${current_division_name}`);
      $('.division-boost .desired-selected-info').html(`${desired_rank_name} ${desired_division_name}`)

      $('.current').removeClass().addClass(`current ${current_rank_name.replace(/\s+/g, '-')}`)
      $('.desired').removeClass().addClass(`desired ${desired_rank_name.replace(/\s+/g, '-')}`)

      $('.total-price #division-boost-price').text(`$${result}`)
  
      // From Value
      if ($('.division-boost input[name="game_type"]').val() == 'D') {
        $('.division-boost input[name="current_rank"]').val(current_rank);
        $('.division-boost input[name="current_division"]').val(current_division);
        $('.division-boost input[name="queue_type"]').val(queue_type);
        $('.division-boost input[name="desired_rank"]').val(desired_rank);
        $('.division-boost input[name="desired_division"]').val(desired_division);
        $('.division-boost input[name="server"]').val(selectedDivsionServer);
        $('.division-boost input[name="price"]').val(result);
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

  // Current Division  Change
  radioButtonsCurrentDivision.forEach(function (radio, index) {
    radio.addEventListener('change', function () {
      const selectedIndex = Array.from(radioButtonsCurrentDivision).indexOf(radio);
      current_division = selectedIndex + 1;
      current_division_name = divisionNames[current_division]
      getDivisionPrice();
    });
  })

  // Desired Division  Change
  radioButtonsDesiredDivision.forEach(function (radio, index) {
    radio.addEventListener('change', function () {
      const selectedIndex = Array.from(radioButtonsDesiredDivision).indexOf(radio);
      desired_division = selectedIndex + 1;
      desired_division_name = divisionNames[desired_division]
      getDivisionPrice()
    });
  });

  // Mark Changes
  queue_type_selected.addEventListener("change", function() {
    queue_type = this.value;
    getDivisionPrice();
  });

  // Server Changes
  division_server_select_element.addEventListener("change", function() {
    selectedDivsionServer = this.value;
    getDivisionPrice();
  });

  // ----------------------------- Others ---------------------------------
  // Extra Charges Part
  // Additional Initial Percent
  let percentege = {
    duoBoosting: 0.65,
    selectBooster: 0.10,
    turboBoost: 0.20,
    streaming: 0.15,
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
        },
        error: function(xhr, textStatus, errorThrown) {
          promoDetails.css('visibility', 'visible');
          promoDetails.text(xhr.responseJSON.error);
          promoDetails.css('color', 'red');
          discount_amount = 0;
          getDivisionPrice();
        }
      });
        
    } else {
      $('input[id="promo_send"]').val('null');
      promoDetails.css('visibility', 'visible');
      promoDetails.text('Please enter a discount code');
      promoDetails.css('color', 'red');
      discount_amount = 0;
      getDivisionPrice();
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

// ----------------------------- Placments Boost ---------------------------------
const placementRank = $('input[name="radio-group-placement-ranks"]');
const gameCountSlider = $("#game-count");
const gameCountValue = $(".game-count-value");
const gameCounterInitial = Number(gameCountSlider.val())
const initiallyPlacementCheckedIndexRank = $('input[name="radio-group-placement-ranks"]').index($('input[name="radio-group-placement-ranks"]:checked'));
const initiallyPlacementCheckedRank = $('input[name="radio-group-placement-ranks"]').eq(initiallyPlacementCheckedIndexRank);
const initiallyPlacementCheckedIndexRankPrice = initiallyPlacementCheckedRank.data('price');

let last_rank = initiallyPlacementCheckedIndexRank + 1
let placementRankPrice = initiallyPlacementCheckedIndexRankPrice
let gameCounter = gameCounterInitial

const getPlacementPrice = () => {
  let price = (placementRankPrice * gameCounter);
  price = parseFloat(price + (price * total_Percentage)).toFixed(2)
  const priceDiv = $('.price-data.placements-boost').eq(0);
  priceDiv.html(`
  <p class='fs-5 text-uppercase my-4 text-secondary'>Boosting of <span class='fw-bold text-white'>${gameCounter} Placement Games</span></p>
  <h4>$${price}</h4>
  `);

  if ($('.placements-boost input[name="game_type"]').val() == 'P') {
    $('.placements-boost input[name="last_rank"]').val(last_rank);
    $('.placements-boost input[name="number_of_match"]').val(gameCounter);
    $('.placements-boost input[name="price"]').val(price);
  }
}
getPlacementPrice()

placementRank.each(function (index, radio) {
  $(radio).on('change', function () {
    const selectedIndex = placementRank.index(radio) + 1;
    last_rank = selectedIndex;
    placementRankPrice = $(radio).data('price');
    getPlacementPrice()
  });
});

gameCountSlider.on("input", function (event) {
  gameCounter = Number(event.target.value);

  gameCountValue.text(gameCounter);

  const progress = (gameCounter / gameCountSlider.prop("max")) * 100;

  gameCountSlider.css("background", `linear-gradient(to right, var(--main-color) ${progress}%, #ccc ${progress}%)`);

  gameCountSlider.css("--thumb-rotate", `${(gameCounter / 100) * 2160}deg`);

  getPlacementPrice()
});

// ----------------------------- Seasonal Reward ---------------------------------
const seasonalRank = $('input[name="radio-group-seasonal-ranks"]');
const numberWinSlider = $("#num-win");
const numberWinValue = $(".number-win-value");
const numberWinInitial = Number(numberWinSlider.val())
const initiallySeasonalCheckedIndexRank = $('input[name="radio-group-seasonal-ranks"]').index($('input[name="radio-group-seasonal-ranks"]:checked'));
const initiallySeasonalCheckedRank = $('input[name="radio-group-seasonal-ranks"]').eq(initiallySeasonalCheckedIndexRank);
const initiallySeasonalCheckedIndexRankPrice = initiallySeasonalCheckedRank.data('price');

let current_rank = initiallySeasonalCheckedIndexRank + 1
let seasonalRankPrice = initiallySeasonalCheckedIndexRankPrice
let numberWin = numberWinInitial

const getSeasonalPrice = () => {
  let price = (seasonalRankPrice * numberWin);
  price = parseFloat(price + (price * total_Percentage)).toFixed(2)
  const priceDiv = $('.price-data.seasonal-reward').eq(0);
  priceDiv.html(`
  <p class='fs-5 text-uppercase my-4 text-secondary'>Seasonal Reward Boosting by <span class='fw-bold text-white'>${numberWin} Wins</span></p>
  <h4>$${price}</h4>
  `);

  if ($('.seasonal-reward input[name="game_type"]').val() == 'S') {
    $('.seasonal-reward input[name="current_rank"]').val(current_rank);
    $('.seasonal-reward input[name="number_of_wins"]').val(numberWin);
    $('.seasonal-reward input[name="price"]').val(price);
  }
}
getSeasonalPrice()

seasonalRank.each(function (index, radio) {
  $(radio).on('change', function () {
    const selectedIndex = seasonalRank.index(radio) + 1;
    current_rank = selectedIndex;
    seasonalRankPrice = $(radio).data('price');
    getSeasonalPrice()
  });
});

numberWinSlider.on("input", function (event) {
  numberWin = Number(event.target.value);

  numberWinValue.text(numberWin);

  const progress = (numberWin / numberWinSlider.prop("max")) * 100;

  numberWinSlider.css("background", `linear-gradient(to right, var(--main-color) ${progress}%, #ccc ${progress}%)`);

  numberWinSlider.css("--thumb-rotate", `${(numberWin / 100) * 2160}deg`);

  getSeasonalPrice()
});

// ----------------------------- Tournament Boost ---------------------------------
const tournamentRank = $('input[name="radio-group-tournament-ranks"]');
const initiallyTournamentCheckedIndexRank = $('input[name="radio-group-tournament-ranks"]').index($('input[name="radio-group-tournament-ranks"]:checked'));
const initiallyTournamentCheckedRank = $('input[name="radio-group-tournament-ranks"]').eq(initiallyTournamentCheckedIndexRank);
const initiallyTournamentCheckedIndexRankPrice = initiallyTournamentCheckedRank.data('price');

let current_league = initiallyTournamentCheckedIndexRank + 1
let tournamentRankPrice = initiallyTournamentCheckedIndexRankPrice

const getTournamentPrice = () => {
  let price = tournamentRankPrice;
  price = parseFloat(price + (price * total_Percentage)).toFixed(2)
  const priceDiv = $('.price-data.tournament-boost').eq(0);
  priceDiv.html(`
  <p class='fs-5 text-uppercase my-4 text-secondary'>${ranksNames[current_league]} League <span class='fw-bold text-white'>Tournament Win</span></p>
  <h4>$${price}</h4>
  `);

  if ($('.tournament-boost input[name="game_type"]').val() == 'T') {
    $('.tournament-boost input[name="current_league"]').val(current_league);
    $('.tournament-boost input[name="price"]').val(price);
  }
}
getTournamentPrice()

tournamentRank.each(function (index, radio) {
  $(radio).on('change', function () {
    const selectedIndex = tournamentRank.index(radio) + 1;
    current_league = selectedIndex;
    tournamentRankPrice = $(radio).data('price');
    getTournamentPrice()
  });
});