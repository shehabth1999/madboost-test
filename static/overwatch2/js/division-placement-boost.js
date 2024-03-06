// Read Values From Json File

let divisionPrices = [0];
let marks_price = [[0, 0, 0, 0, 0]];
let role_price = 0
Promise.all([
  new Promise(function (resolve, reject) {
    $.getJSON('/static/overwatch2/data/divisions_data.json', function (data) {
      divisionPrices = divisionPrices.concat(...data);
      resolve();
    });
  }),
  new Promise(function (resolve, reject) {
    $.getJSON('/static/overwatch2/data/marks_data.json', function (data) {
      marks_price = marks_price.concat(data.slice(0));
      resolve();
    });
  })
]).then(function () {
  // Array For Names 
  const divisionRanks = ['','bronze', 'silver', 'gold', 'platinum', 'diamond', 'master', 'grand master', 'champion']

  const divisionNames = ['', 'V', 'IV', 'III', 'II', 'I']


  if(extend_order) {
    let orderID = parseInt(extend_order, 10);
    document.getElementById('extendOrder').value = orderID; 

    // Set the checked state for each group of radio buttons using the specified order
    setRadioButtonStateWithDisable(radioButtonsCurrent, valuesToSet[0]-1);
    setRadioButtonStateWithDisable(radioButtonsCurrentDivision, valuesToSet[1]-1);
    setRadioButtonState(radioButtonsDesired, valuesToSet[3]-1, true);
    setRadioButtonStateForDesiredDivision(radioButtonsDesiredDivision, valuesToSet[4]-1);
    makrs_on_current_rank_selected.disabled = true
    division_server_select_element.disabled = true


    // Solo Or Duo Boosting Change
    if (valuesToSetAdditional[0]) {
      duoBoosting.checked = true;
      $('input#duoBoosting').val(true)
      duoBoosting.disabled = true;
      soloBoosting.disabled = true;
    } else {
      soloBoosting.checked = true;
      $('input#duoBoosting').val(false)
    }

    // Extra Buttons
    extraOptions.forEach(function (checkbox, index) {
      if (checkbox.value === "selectBooster" && valuesToSetAdditional[1]) {
        checkbox.checked = true
        $(`input#${checkbox.value}`).val(true)
        $(checkbox).prop('disabled', true)
      } else if (checkbox.value === "turboBoost" && valuesToSetAdditional[2]) {
        checkbox.checked = true
        $(`input#${checkbox.value}`).val(true)
        $(checkbox).prop('disabled', true)
      } else if (checkbox.value === "streaming" && valuesToSetAdditional[3]) {
        checkbox.checked = true
        $(`input#${checkbox.value}`).val(true)
        $(checkbox).prop('disabled', true)
      } else if (checkbox.value === "boosterChampions" && valuesToSetAdditional[4]) {
        checkbox.checked = true
        $(`input#${checkbox.value}`).val(true)
        $(checkbox).prop('disabled', true)
      } else {
        checkbox.checked = false
        $(`input#${checkbox.value}`).val(false)
      } 
    })
  
    function getDivisionPrice() {
      const desired_rank = getSelectedValueForRadio(radioButtonsDesired)
      const desired_division = getSelectedValueForRadio(radioButtonsDesiredDivision)

      const current_rank = valuesToSet[0];
      const current_division = valuesToSet[1];
      const mark_index = valuesToSet[2];
      
      const current_rank_name = divisionRanks[current_rank];
      const desired_rank_name = divisionRanks[desired_rank];
      const current_division_name = divisionNames[current_division];
      const desired_division_name = divisionNames[desired_division];
      
      const startRank = ((valuesToSet[3] - 1) * 5) + valuesToSet[4];
      const endRank = ((desired_rank - 1) * 5) + desired_division-1;
      const slicedArr = sliceArray(divisionPrices, startRank, endRank);
      
      const sum = slicedArr.reduce((accumulator, currentValue) => accumulator + currentValue, 0);

      let result_with_mark = sum
      
      // Apply role extra value
      const total_Percentage_with_role_result = total_Percentage + role_price

      // Apply extra charges to the result
      result_with_mark += result_with_mark * total_Percentage_with_role_result;
      // Apply promo code 
      result_with_mark -= result_with_mark * (discount_amount/100 )
      
      result_with_mark = parseFloat(result_with_mark.toFixed(2)); 

      // Look Here:- We Change Everything Should Change Depend On Current & Desired Element
      $('.division-boost .current-rank-selected-img').attr('src', $(currentElement).data('img'))
      $('.division-boost .desired-rank-selected-img').attr('src', $(desiredElement).data('img'))

      $('.division-boost .current-selected-info').html(`${divisionRanks[valuesToSet[3]]} ${mark_index == 0 ? '0-19 %' : mark_index == 1 ? '20-39 %' : mark_index == 2 ? '40-59 %' : mark_index == 3 ? '60-79 %' : mark_index == 4 ? '80-99 %' : ''}`);
      $('.division-boost .desired-selected-info').html(`${desired_rank_name} ${desired_division_name}`)

      $('.current').removeClass().addClass(`current ${divisionRanks[valuesToSet[3]]}`)
      $('.desired').removeClass().addClass(`desired ${desired_rank_name}`)

      $('.total-price #division-boost-price').text(`$${result_with_mark}`)

      // From Value
      $('.division-boost input[name="current_rank"]').val(current_rank);
      $('.division-boost input[name="current_division"]').val(current_division);
      $('.division-boost input[name="marks"]').val(mark_index);
      $('.division-boost input[name="desired_rank"]').val(desired_rank);
      $('.division-boost input[name="desired_division"]').val(desired_division);
      $('.division-boost input[name="price"]').val(result_with_mark);
    }
  } else {
    // Get Result Function
    function getDivisionPrice() {

      const current_rank = getSelectedValueForRadio(radioButtonsCurrent);
      const desired_rank = getSelectedValueForRadio(radioButtonsDesired)
      const current_division = getSelectedValueForRadio(radioButtonsCurrentDivision)
      const desired_division = getSelectedValueForRadio(radioButtonsDesiredDivision)
      const current_rank_name = divisionRanks[current_rank];
      const desired_rank_name = divisionRanks[desired_rank];
      const current_division_name = divisionNames[current_division];
      const desired_division_name = divisionNames[desired_division];
      let mark_index = -1
      let number_of_mark = 0
      try {
        mark_index = getSelectedValueForDropList(makrs_on_current_rank_selected)
        number_of_mark = marks_price[current_rank][mark_index];
      } catch (error) {
        
      }
      // const role_index = getSelectedValueForDropList(role_selected);
      // console.log(role_index)

      const selectedDivsionServer = division_server_select_element.value;
      
      const startRank = ((current_rank - 1) * 5) + current_division;
      const endRank = ((desired_rank - 1) * 5) + desired_division - 1;
      const slicedArray = sliceArray(divisionPrices, startRank, endRank);
      console.log(startRank,endRank, slicedArray , number_of_mark)
      let result = slicedArray.reduce((accumulator, currentValue) => accumulator + currentValue, 0);
      let result_with_mark = result
  
      if (result > 0) {
        result_with_mark = result - number_of_mark;
      }
      
      //Apply role percent
      const total_Percentage_with_role_result = total_Percentage + role_price

      // Apply extra charges to the result
      result_with_mark += result_with_mark * total_Percentage_with_role_result;
      // Apply promo code 
      result_with_mark -= result_with_mark * (discount_amount/100 )



      result_with_mark = parseFloat(result_with_mark.toFixed(2)); 

      const currentElement = getSelectedElement(radioButtonsCurrent)
      const desiredElement = getSelectedElement(radioButtonsDesired)
      // Look Here:- We Change Everything Should Change Depend On Current & Desired Element
      $('.division-boost .current-rank-selected-img').attr('src', $(currentElement).data('img'))
      $('.division-boost .desired-rank-selected-img').attr('src', $(desiredElement).data('img'))



      $('.division-boost .current-selected-info').html(`${current_rank_name} ${current_division_name} ${mark_index == 0 ? '0-19 %' : mark_index == 1 ? '20-39 %' : mark_index == 2 ? '40-59 %' : mark_index == 3 ? '60-79 %' : mark_index == 4 ? '80-99 %' : ''}`);
      $('.division-boost .desired-selected-info').html(`${desired_rank_name} ${desired_division_name}`)

      $('.current').removeClass().addClass(`current ${current_rank_name}`)
      $('.desired').removeClass().addClass(`desired ${desired_rank_name}`)

      $('.total-price #division-boost-price').text(`$${result_with_mark}`)
  
      // From Value
      if ($('.division-boost input[name="game_type"]').val() == 'D') {
        $('.division-boost input[name="current_rank"]').val(current_rank);
        $('.division-boost input[name="current_division"]').val(current_division);
        $('.division-boost input[name="marks"]').val(mark_index);
        $('.division-boost input[name="desired_rank"]').val(desired_rank);
        $('.division-boost input[name="desired_division"]').val(desired_division);
        $('.division-boost input[name="server"]').val(selectedDivsionServer);
        $('.division-boost input[name="price"]').val(result_with_mark);
      }
    }
  }


  // Current Rank Change
  radioButtonsCurrent.forEach(function (radio, index) {
    radio.addEventListener('change', function () {
      getDivisionPrice();
    });
  });

  // Desired Rank Change
  radioButtonsDesired.forEach(function (radio, index) {
    radio.addEventListener('change', function(){
      getDivisionPrice()
    });
  });

  // Current Division Change
  radioButtonsCurrentDivision.forEach(function (radio, index) {
    radio.addEventListener('change', ()=>{
      getDivisionPrice()
    });
  })

  // Desired Division Change
  radioButtonsDesiredDivision.forEach(function (radio, index) {
    radio.addEventListener('change', function(){
      getDivisionPrice()
    });
  });

  // Mark Changes
  makrs_on_current_rank_selected.addEventListener("change", function(){
    getDivisionPrice()
  });
  // Server Changes
  division_server_select_element.addEventListener("change", function(){
    getDivisionPrice()
  }); // we dont need this


  // Get Result 
  getDivisionPrice();


  
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
  let pervious_rank_name = divisionRanks[pervious_rank]
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
      pervious_rank_name = divisionRanks[pervious_rank]
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
    console.log($(this).val())
    selectedPlacementServer = $(this).val();
    getPlacementPrice();
  });

  // ----------------------------- Others ---------------------------------



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

  role_selected.addEventListener('change', function () {
    role_price = 0
    const role_imput = document.getElementById('role_input')
    switch (this.value) {
      case '1':
        role_price = 0
        role_imput.value = '1';
        getDivisionPrice()
        break;
      case '2':
        role_price = 0
        role_imput.value = '2';
        getDivisionPrice()
        break;
      case '3':
        role_price = .12;
        role_imput.value = '3';
        getDivisionPrice()
        break;
      default:
        console.log('Invalid option selected');
        break;
    }
  });
  
  promo_form.addEventListener('submit', async function(event) {
    event.preventDefault();
    discount_amount = await fetch_promo(); 
    getDivisionPrice(); 
    getPlacementPrice();
  });
});