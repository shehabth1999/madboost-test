$(document).ready(function() {
  $toggleMenu = $('.main-nav .toggle-menu');
  $links = $('.main-nav .links');
  $toggleMenu.click(function() {
    $links.toggleClass('shown')
  })
});