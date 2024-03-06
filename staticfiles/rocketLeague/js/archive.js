function getDivisionPrice() {
  const startRank = ((valuesToSet[3] - 1) * 3) + valuesToSet[4];
  const endRank = ((desired_rank_ - 1) * 3) + desired_division_-1;
  const slicedArray = sliceArray(divisionPrices, startRank, endRank);
  let sum = slicedArray.reduce((accumulator, currentValue) => accumulator + currentValue, 0);
  console.log(slicedArray)

  // Apply extra charges to the result
  sum += sum * total_Percentage;
  sum = parseFloat(sum.toFixed(2)); 

  const pricee = document.querySelector('.price-data.ranked-boost');
  pricee.innerHTML = `
  <p class='fs-5 text-uppercase my-4 text-secondary'>Boosting <span class='fw-bold text-white'>From ${current_rank_name_} ${current_division_name_} to ${ranksNames[valuesToSet[3]]} ${divisionNames[valuesToSet[4]] } </span></p>
  <p class='fs-5 text-uppercase my-4 text-secondary'>Extend <span class='fw-bold text-white'>From ${ranksNames[valuesToSet[3]]} ${divisionNames[valuesToSet[4]]} to ${desired_rank_name_} ${desired_division_name_} </span></p>
  <span class='fs-5 text-uppercase fw-bold'>Extra Cost: $${sum}</span>
`;

  // From Value
  if ($('.ranked-boost input[name="ranked_type"]').val() == 3) {
    $('.ranked-boost input[name="current_rank"]').val(current_rank_);
    $('.ranked-boost input[name="current_division"]').val(current_division_);
    $('.ranked-boost input[name="desired_rank"]').val(desired_rank_);
    $('.ranked-boost input[name="desired_division"]').val(desired_division_);
    $('.ranked-boost input[name="price"]').val(sum);
  }
}


document.addEventListener("DOMContentLoaded", function () {
  const extend_order = urlParams.get('extend');

  // Access the data attribute and convert it to a JavaScript variable
  const orderValue = orderContainer.dataset.order;

  const valuesAsList = orderValue.split(',')
  
  const ranked3vs3BoostRadio = document.getElementById('ranked3vs3-boost');
  const ranked2vs2BoostRadio = document.getElementById('ranked2vs2-boost');
  const ranked1vs1BoostRadio = document.getElementById('ranked1vs1-boost');
  const placementBoostRadio = document.getElementById('placements-boost');
  const seasonalBoostRadio = document.getElementById('seasonal-reward');
  const tournamentBoostRadio = document.getElementById('tournament-boost');

  const ranked3vs3BoostDiv = document.querySelectorAll('.ranked3vs3-boost');
  const ranked2vs2BoostDiv = document.querySelectorAll('.ranked2vs2-boost');
  const ranked1vs1BoostDiv = document.querySelectorAll('.ranked1vs1-boost');
  const rankedBoostDiv = document.querySelectorAll('.ranked-boost');
  const placementBoostDiv = document.querySelectorAll('.placements-boost');
  const seasonalBoostDiv = document.querySelectorAll('.seasonal-reward');
  const tournamentBoostDiv = document.querySelectorAll('.tournament-boost');

  // Initial setup
  if (ranked3vs3BoostRadio.checked) {
    ranked3vs3BoostDiv.forEach(div => div.classList.remove('d-none'));
    ranked2vs2BoostDiv.forEach(div => div.classList.add('d-none'));
    ranked1vs1BoostDiv.forEach(div => div.classList.add('d-none'));
    placementBoostDiv.forEach(div => div.classList.add('d-none'));
    seasonalBoostDiv.forEach(div => div.classList.add('d-none'));
    tournamentBoostDiv.forEach(div => div.classList.add('d-none'));

    rankedBoostDiv.forEach(div => div.classList.remove('d-none'));
    $('input[name="ranked_type"]').val(3);
  } else if (ranked2vs2BoostRadio.checked) {
    ranked3vs3BoostDiv.forEach(div => div.classList.add('d-none'));
    ranked2vs2BoostDiv.forEach(div => div.classList.remove('d-none'));
    ranked1vs1BoostDiv.forEach(div => div.classList.add('d-none'));
    placementBoostDiv.forEach(div => div.classList.add('d-none'));
    seasonalBoostDiv.forEach(div => div.classList.add('d-none'));
    tournamentBoostDiv.forEach(div => div.classList.add('d-none'));

    rankedBoostDiv.forEach(div => div.classList.remove('d-none'));
    $('input[name="ranked_type"]').val(2);
  } else if (ranked1vs1BoostRadio.checked) {
    ranked3vs3BoostDiv.forEach(div => div.classList.add('d-none'));
    ranked2vs2BoostDiv.forEach(div => div.classList.add('d-none'));
    ranked1vs1BoostDiv.forEach(div => div.classList.remove('d-none'));
    placementBoostDiv.forEach(div => div.classList.add('d-none'));
    seasonalBoostDiv.forEach(div => div.classList.add('d-none'));
    tournamentBoostDiv.forEach(div => div.classList.add('d-none'));
    
    rankedBoostDiv.forEach(div => div.classList.remove('d-none'));
    $('input[name="ranked_type"]').val(1);
  } else if (placementBoostRadio.checked) {
    ranked3vs3BoostDiv.forEach(div => div.classList.add('d-none'));
    ranked2vs2BoostDiv.forEach(div => div.classList.add('d-none'));
    ranked1vs1BoostDiv.forEach(div => div.classList.add('d-none'));
    placementBoostDiv.forEach(div => div.classList.remove('d-none'));
    seasonalBoostDiv.forEach(div => div.classList.add('d-none'));
    tournamentBoostDiv.forEach(div => div.classList.add('d-none'));

    rankedBoostDiv.forEach(div => div.classList.add('d-none'));
  } else if (seasonalBoostRadio.checked) {
    ranked3vs3BoostDiv.forEach(div => div.classList.add('d-none'));
    ranked2vs2BoostDiv.forEach(div => div.classList.add('d-none'));
    ranked1vs1BoostDiv.forEach(div => div.classList.add('d-none'));
    placementBoostDiv.forEach(div => div.classList.add('d-none'));
    seasonalBoostDiv.forEach(div => div.classList.remove('d-none'));
    tournamentBoostDiv.forEach(div => div.classList.add('d-none'));

    rankedBoostDiv.forEach(div => div.classList.add('d-none'));
  } else if (tournamentBoostRadio.checked) {
    ranked3vs3BoostDiv.forEach(div => div.classList.add('d-none'));
    ranked2vs2BoostDiv.forEach(div => div.classList.add('d-none'));
    ranked1vs1BoostDiv.forEach(div => div.classList.add('d-none'));
    placementBoostDiv.forEach(div => div.classList.add('d-none'));
    seasonalBoostDiv.forEach(div => div.classList.add('d-none'));
    tournamentBoostDiv.forEach(div => div.classList.remove('d-none'));

    rankedBoostDiv.forEach(div => div.classList.add('d-none'));
  } 

  // Event listener for 3vs3 ranked-boost radio button
  ranked3vs3BoostRadio.addEventListener('change', function () {
    if (ranked3vs3BoostRadio.checked) {
      ranked3vs3BoostDiv.forEach(div => div.classList.remove('d-none'));
      ranked2vs2BoostDiv.forEach(div => div.classList.add('d-none'));
      ranked1vs1BoostDiv.forEach(div => div.classList.add('d-none'));
      placementBoostDiv.forEach(div => div.classList.add('d-none'));
      seasonalBoostDiv.forEach(div => div.classList.add('d-none'));
      tournamentBoostDiv.forEach(div => div.classList.add('d-none'));

      rankedBoostDiv.forEach(div => div.classList.remove('d-none'));
      $('input[name="ranked_type"]').val(3);
    } else {
      ranked3vs3BoostDiv.forEach(div => div.classList.add('d-none'));
      rankedBoostDiv.forEach(div => div.classList.add('d-none'));
    }
  });

  // Event listener for 2vs2 ranked-boost radio button
  ranked2vs2BoostRadio.addEventListener('change', function () {
    if (ranked2vs2BoostRadio.checked) {
      ranked3vs3BoostDiv.forEach(div => div.classList.add('d-none'));
      ranked2vs2BoostDiv.forEach(div => div.classList.remove('d-none'));
      ranked1vs1BoostDiv.forEach(div => div.classList.add('d-none'));
      placementBoostDiv.forEach(div => div.classList.add('d-none'));
      seasonalBoostDiv.forEach(div => div.classList.add('d-none'));
      tournamentBoostDiv.forEach(div => div.classList.add('d-none'));

      rankedBoostDiv.forEach(div => div.classList.remove('d-none'));
      $('input[name="ranked_type"]').val(2);
    } else {
      ranked2vs2BoostDiv.forEach(div => div.classList.add('d-none'));
      rankedBoostDiv.forEach(div => div.classList.add('d-none'));
    }
  });

  // Event listener for 1vs1 ranked-boost radio button
  ranked1vs1BoostRadio.addEventListener('change', function () {
    if (ranked1vs1BoostRadio.checked) {
      ranked3vs3BoostDiv.forEach(div => div.classList.add('d-none'));
      ranked2vs2BoostDiv.forEach(div => div.classList.add('d-none'));
      ranked1vs1BoostDiv.forEach(div => div.classList.remove('d-none'));
      placementBoostDiv.forEach(div => div.classList.add('d-none'));
      seasonalBoostDiv.forEach(div => div.classList.add('d-none'));
      tournamentBoostDiv.forEach(div => div.classList.add('d-none'));

      rankedBoostDiv.forEach(div => div.classList.remove('d-none'));
      $('input[name="ranked_type"]').val(1);
    } else {
      ranked1vs1BoostDiv.forEach(div => div.classList.add('d-none'));
      rankedBoostDiv.forEach(div => div.classList.add('d-none'));
    }
  });

  // Event listener for placements-boost radio button
  placementBoostRadio.addEventListener('change', function () {
    if (placementBoostRadio.checked) {
      ranked3vs3BoostDiv.forEach(div => div.classList.add('d-none'));
      ranked2vs2BoostDiv.forEach(div => div.classList.add('d-none'));
      ranked1vs1BoostDiv.forEach(div => div.classList.add('d-none'));
      placementBoostDiv.forEach(div => div.classList.remove('d-none'));
      seasonalBoostDiv.forEach(div => div.classList.add('d-none'));
      tournamentBoostDiv.forEach(div => div.classList.add('d-none'));

      rankedBoostDiv.forEach(div => div.classList.add('d-none'));
    } else {
      placementBoostDiv.forEach(div => div.classList.add('d-none'));
    }
  });

  // Event listener for seasonal-reward radio button
  seasonalBoostRadio.addEventListener('change', function () {
    if (seasonalBoostRadio.checked) {
      ranked3vs3BoostDiv.forEach(div => div.classList.add('d-none'));
      ranked2vs2BoostDiv.forEach(div => div.classList.add('d-none'));
      ranked1vs1BoostDiv.forEach(div => div.classList.add('d-none'));
      placementBoostDiv.forEach(div => div.classList.add('d-none'));
      seasonalBoostDiv.forEach(div => div.classList.remove('d-none'));
      tournamentBoostDiv.forEach(div => div.classList.add('d-none'));

      rankedBoostDiv.forEach(div => div.classList.add('d-none'));
    } else {
      seasonalBoostDiv.forEach(div => div.classList.add('d-none'));
    }
  });

  // Event listener for tournament-boost radio button
  tournamentBoostRadio.addEventListener('change', function () {
    if (tournamentBoostRadio.checked) {
      ranked3vs3BoostDiv.forEach(div => div.classList.add('d-none'));
      ranked2vs2BoostDiv.forEach(div => div.classList.add('d-none'));
      ranked1vs1BoostDiv.forEach(div => div.classList.add('d-none'));
      placementBoostDiv.forEach(div => div.classList.add('d-none'));
      seasonalBoostDiv.forEach(div => div.classList.add('d-none'));
      tournamentBoostDiv.forEach(div => div.classList.remove('d-none'));

      rankedBoostDiv.forEach(div => div.classList.add('d-none'));
    } else {
      tournamentBoostRadio.forEach(div => div.classList.add('d-none'));
    }
  });

  // Check Correct Option When Extend
  // if(extend_order) {
  //   if (valuesAsList[0] == 3) {
  //     console.log("Ranked Type: 3vs3")
  //     ranked3vs3BoostRadio.checked = true
  //   } else if (valuesAsList[0] == 2) {
  //     console.log("Ranked Type: 2vs2")
  //     ranked2vs2BoostRadio.checked = true
  //   } else if (valuesAsList[0] == 1) {
  //     console.log("Ranked Type: 1vs1")
  //     ranked1vs1BoostRadio.checked = true
  //   }
  // }
});