document.addEventListener("DOMContentLoaded", function () {
  const divisionBoostRadio = document.getElementById('division-boost');
  const placementsBoostRadio = document.getElementById('placements-boost');
  
  const divisionBoostDiv = document.querySelectorAll('.division-boost');
  const placementsBoostDiv = document.querySelectorAll('.placements-boost');

  // const divisionForm = document.getElementById('division-boost');
  // const placementsForm = document.getElementById('placements-boost');

  // Initial setup
  if (divisionBoostRadio.checked) {
    divisionBoostDiv.forEach(div => div.classList.remove('d-none'));
    placementsBoostDiv.forEach(div => div.classList.add('d-none'));
    divisionBoostDiv.forEach(div => div.classList.add('active'));
    placementsBoostDiv.forEach(div => div.classList.remove('active'));
    // divisionForm.classList.add("active");
    // placementsForm.classList.remove("active");
  } else {
    divisionBoostDiv.forEach(div => div.classList.add('d-none'));
    placementsBoostDiv.forEach(div => div.classList.remove('d-none'));
    divisionBoostDiv.forEach(div => div.classList.remove('active'));
    placementsBoostDiv.forEach(div => div.classList.add('active'));
    // divisionForm.classList.remove("active");
    // placementsForm.classList.add("active");
  }

  // Event listener for division-boost radio button
  divisionBoostRadio.addEventListener('change', function () {
    if (divisionBoostRadio.checked) {
      divisionBoostDiv.forEach(div => div.classList.remove('d-none'));
      placementsBoostDiv.forEach(div => div.classList.add('d-none'));
      divisionBoostDiv.forEach(div => div.classList.add('active'));
      placementsBoostDiv.forEach(div => div.classList.remove('active'));
      // divisionForm.classList.add("active");
      // placementsForm.classList.remove("active");
    } else {
      divisionBoostDiv.forEach(div => div.classList.add('d-none'));
      divisionBoostDiv.forEach(div => div.classList.remove('active'));
      // divisionForm.classList.remove("active");
    }
  });

  // Event listener for placements-boost radio button
  placementsBoostRadio.addEventListener('change', function () {
    if (placementsBoostRadio.checked) {
      divisionBoostDiv.forEach(div => div.classList.add('d-none'));
      placementsBoostDiv.forEach(div => div.classList.remove('d-none'));
      divisionBoostDiv.forEach(div => div.classList.remove('active'));
      placementsBoostDiv.forEach(div => div.classList.add('active'));
      // divisionForm.classList.remove("active");
      // placementsForm.classList.add("active");
    } else {
      placementsBoostDiv.forEach(div => div.classList.add('d-none'));
      placementsBoostDiv.forEach(div => div.classList.remove('active'));
      // placementsForm.classList.remove("active");
    }
  });

});