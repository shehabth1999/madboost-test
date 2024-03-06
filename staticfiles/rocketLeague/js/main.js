document.addEventListener("DOMContentLoaded", function () {
  
  const divisionBoostRadio = document.getElementById('division-boost');
  const placementBoostRadio = document.getElementById('placements-boost');
  const seasonalBoostRadio = document.getElementById('seasonal-reward');
  const tournamentBoostRadio = document.getElementById('tournament-boost');

  const divisionBoostDiv = document.querySelectorAll('.division-boost');
  const placementBoostDiv = document.querySelectorAll('.placements-boost');
  const seasonalBoostDiv = document.querySelectorAll('.seasonal-reward');
  const tournamentBoostDiv = document.querySelectorAll('.tournament-boost');

  // Initial setup
  if (divisionBoostRadio.checked) {
    divisionBoostDiv.forEach(div => div.classList.remove('d-none'));
    placementBoostDiv.forEach(div => div.classList.add('d-none'));
    seasonalBoostDiv.forEach(div => div.classList.add('d-none'));
    tournamentBoostDiv.forEach(div => div.classList.add('d-none'));

  } else if (placementBoostRadio.checked) {
    divisionBoostDiv.forEach(div => div.classList.add('d-none'));
    placementBoostDiv.forEach(div => div.classList.remove('d-none'));
    seasonalBoostDiv.forEach(div => div.classList.add('d-none'));
    tournamentBoostDiv.forEach(div => div.classList.add('d-none'));

  } else if (seasonalBoostRadio.checked) {
    divisionBoostDiv.forEach(div => div.classList.add('d-none'));
    placementBoostDiv.forEach(div => div.classList.add('d-none'));
    seasonalBoostDiv.forEach(div => div.classList.remove('d-none'));
    tournamentBoostDiv.forEach(div => div.classList.add('d-none'));

  } else if (tournamentBoostRadio.checked) {
    divisionBoostDiv.forEach(div => div.classList.add('d-none'));
    placementBoostDiv.forEach(div => div.classList.add('d-none'));
    seasonalBoostDiv.forEach(div => div.classList.add('d-none'));
    tournamentBoostDiv.forEach(div => div.classList.remove('d-none'));

  } 

  // Event listener for division-boost radio button
  divisionBoostRadio.addEventListener('change', function () {
    if (divisionBoostRadio.checked) {
      divisionBoostDiv.forEach(div => div.classList.remove('d-none'));
      placementBoostDiv.forEach(div => div.classList.add('d-none'));
      seasonalBoostDiv.forEach(div => div.classList.add('d-none'));
      tournamentBoostDiv.forEach(div => div.classList.add('d-none'));

    } else {
      divisionBoostDiv.forEach(div => div.classList.add('d-none'));
    }
  });


  // Event listener for placements-boost radio button
  placementBoostRadio.addEventListener('change', function () {
    if (placementBoostRadio.checked) {
      divisionBoostDiv.forEach(div => div.classList.add('d-none'));
      placementBoostDiv.forEach(div => div.classList.remove('d-none'));
      seasonalBoostDiv.forEach(div => div.classList.add('d-none'));
      tournamentBoostDiv.forEach(div => div.classList.add('d-none'));

    } else {
      placementBoostDiv.forEach(div => div.classList.add('d-none'));
    }
  });

  // Event listener for seasonal-reward radio button
  seasonalBoostRadio.addEventListener('change', function () {
    if (seasonalBoostRadio.checked) {
      divisionBoostDiv.forEach(div => div.classList.add('d-none'));
      placementBoostDiv.forEach(div => div.classList.add('d-none'));
      seasonalBoostDiv.forEach(div => div.classList.remove('d-none'));
      tournamentBoostDiv.forEach(div => div.classList.add('d-none'));

    } else {
      seasonalBoostDiv.forEach(div => div.classList.add('d-none'));
    }
  });

  // Event listener for tournament-boost radio button
  tournamentBoostRadio.addEventListener('change', function () {
    if (tournamentBoostRadio.checked) {
      divisionBoostDiv.forEach(div => div.classList.add('d-none'));
      placementBoostDiv.forEach(div => div.classList.add('d-none'));
      seasonalBoostDiv.forEach(div => div.classList.add('d-none'));
      tournamentBoostDiv.forEach(div => div.classList.remove('d-none'));

    } else {
      tournamentBoostRadio.forEach(div => div.classList.add('d-none'));
    }
  });

});