document.addEventListener("DOMContentLoaded", function() {
  const form = document.querySelector('form#complete-image-upload');
  const fileInput = document.querySelector('input[type="file"][name="finish_image"]');
  const errorElement = document.querySelector('#image-over-size-error');
  
  fileInput.addEventListener('change', function() {
    const file = this.files[0];
    if (file && file.size > 10 * 1024 * 1024) { // Check if file size is greater than 10 MB
      errorElement.textContent = "This file is too large. Please select a file smaller than 10 MB.";
      console.log("This file is too large. Please select a file smaller than 10 MB.")
      this.value = ''; // Clear the file input
      event.preventDefault(); // Prevent form submission
    } else {
      errorElement.textContent = ''; // Clear any previous error message
    }
  });
  
  form.addEventListener('submit', function(event) {
    const file = fileInput.files[0];
    if (file && file.size > 10 * 1024 * 1024) { // Check if file size is greater than 10 MB
      errorElement.textContent = "This file is too large. Please select a file smaller than 10 MB.";
      console.log("This file is too large. Please select a file smaller than 10 MB.")
      event.preventDefault(); // Prevent form submission
    } else {
      errorElement.textContent = ''; // Clear any previous error message
    }
  });
});