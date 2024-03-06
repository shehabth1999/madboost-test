document.addEventListener("DOMContentLoaded", function () {
  const divisionBoostRadio = document.getElementById('rank-boost');
  const placementsBoostRadio = document.getElementById('placements-boost');
  const arenaBoostRadio = document.getElementById('arena-boost');

  const divisionBoostDiv = document.querySelectorAll('.rank-boost');
  const placementsBoostDiv = document.querySelectorAll('.placements-boost');
  const arenaBoostDiv = document.querySelectorAll('.arena-boost');

  // Initial setup
  if (divisionBoostRadio.checked) {
    divisionBoostDiv.forEach(div => div.classList.remove('d-none'));
    placementsBoostDiv.forEach(div => div.classList.add('d-none'));
    arenaBoostDiv.forEach(div => div.classList.add('d-none'));
  } else if (placementsBoostRadio.checked) {
    divisionBoostDiv.forEach(div => div.classList.add('d-none'));
    arenaBoostDiv.forEach(div => div.classList.add('d-none'));
    placementsBoostDiv.forEach(div => div.classList.remove('d-none'));
  } else {
    arenaBoostDiv.forEach(div => div.classList.remove('d-none'));
    divisionBoostDiv.forEach(div => div.classList.add('d-none'));
    placementsBoostDiv.forEach(div => div.classList.add('d-none'));
  }

  // Event listener for division-boost radio button
  divisionBoostRadio.addEventListener('change', function () {
    if (divisionBoostRadio.checked) {
      divisionBoostDiv.forEach(div => div.classList.remove('d-none'));
      arenaBoostDiv.forEach(div => div.classList.add('d-none'));
      placementsBoostDiv.forEach(div => div.classList.add('d-none'));
    } else {
      divisionBoostDiv.forEach(div => div.classList.add('d-none'));
    }
  });

  // Event listener for placements-boost radio button
  placementsBoostRadio.addEventListener('change', function () {
    if (placementsBoostRadio.checked) {
      divisionBoostDiv.forEach(div => div.classList.add('d-none'));
      arenaBoostDiv.forEach(div => div.classList.add('d-none'));
      placementsBoostDiv.forEach(div => div.classList.remove('d-none'));
    } else {
      placementsBoostDiv.forEach(div => div.classList.add('d-none'));
    }
  });

  // Event listener for arena-boost radio button
  arenaBoostRadio.addEventListener('change', function () {
    if (arenaBoostRadio.checked) {
      divisionBoostDiv.forEach(div => div.classList.add('d-none'));
      placementsBoostDiv.forEach(div => div.classList.add('d-none'));
      arenaBoostDiv.forEach(div => div.classList.remove('d-none'));
    } else {
      arenaBoostDiv.forEach(div => div.classList.add('d-none'));
    }
  });
});