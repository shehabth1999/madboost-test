document.addEventListener('DOMContentLoaded', function() {
  const game_id = parseInt(document.querySelector('form.purchaseForm input[name="game_id"]').value);

  const urls = document.getElementById('urls');

  // --------------------- DIVISION ---------------------

  const divisionForm = document.getElementById('division-boost-form');
  const divisionPaypalBtn = document.getElementById('division-paypal-btn');
  const divisionCryptomusBtn = document.getElementById('division-cryptomus-btn');

  divisionPaypalBtn.addEventListener('click', function() {
    // Get the PayPal URL from data attribute
    const paypalUrl = urls.dataset.paypalUrl;
    // Set the form action
    divisionForm.action = paypalUrl;
    // Submit the form
    divisionForm.submit();
  });

  divisionCryptomusBtn.addEventListener('click', function() {
    // Get the Cryptomus URL from data attribute
    const cryptomusUrl = urls.dataset.cryptomusUrl;
    // Set the form action
    divisionForm.action = cryptomusUrl;
    // Submit the form
    divisionForm.submit();
  });

  // --------------------- PLACEMNET ---------------------

  if (game_id != 1) {
    const placementForm = document.getElementById('placements-boost-form');
    const placementPaypalBtn = document.getElementById('placement-paypal-btn');
    const placementCryptomusBtn = document.getElementById('placement-cryptomus-btn');

    placementPaypalBtn.addEventListener('click', function() {
      // Get the PayPal URL from data attribute
      const paypalUrl = urls.dataset.paypalUrl;
      // Set the form action
      placementForm.action = paypalUrl;
      // Submit the form
      placementForm.submit();
    });

    placementCryptomusBtn.addEventListener('click', function() {
      // Get the Cryptomus URL from data attribute
      const cryptomusUrl = urls.dataset.cryptomusUrl;
      // Set the form action
      placementForm.action = cryptomusUrl;
      // Submit the form
      placementForm.submit();
    });
  }

});
