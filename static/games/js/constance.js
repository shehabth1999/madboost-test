// const  file for hold data only 

const urlParams = new URLSearchParams(window.location.search);
const extend_order = urlParams.get('extend');  // to get if extend_order choose 
const chooseBoosterValue = urlParams.get('choose_booster'); // to get if booster bootser choose after order


const orderContainer = document.getElementById('order-container'); // this an html part only to hold data from order extend if user need to exted order
const orderValue = orderContainer.dataset.order; // values of extended order as string 
const valuesAsList = orderValue.split(',') // values of extended order as list of strings
const list1 = valuesAsList.slice(0, 5); // values of extended order as {current_rank.id}, {current_division}, {current_marks}, {desired_rank.id}, {desired_division}
const list2 = valuesAsList.slice(5, 10);  // values of extended order as {duo_boosting}, {False}, {turbo_boost}, {streaming }, {choose_champions}


const valuesToSet = list1.map(function(item) {
    return parseInt(item, 10); // Use parseInt to convert list1 from srting to int as list
  });
const valuesToSetAdditional = list2.map(value => JSON.parse(value.toLowerCase())); // to convert code to true and false for list2 

let autoSelectBooster = $('input#select-booster'); // select an input for select-booster 
let chooseBoosterInt = 0 // inital value of choose booster
if (chooseBoosterValue != null) {
  chooseBoosterInt = parseInt(chooseBoosterValue, 10);
  autoSelectBooster.val(true) // make select booster = checked
}
document.getElementById('chooseBoosterInput').value = chooseBoosterInt; // remove this soon because i will use new value

let percentege = {    // Additional Initial Percent
  duoBoosting: 0.65,
  selectBooster: 0.10,
  turboBoost: 0.20,
  streaming: 0.15,
  boosterAgents: 0.0 
}

// buttons
const radioButtonsCurrent = document.querySelectorAll('input[name="radio-group-current"]');
const radioButtonsDesired = document.querySelectorAll('input[name="radio-group-desired"]');
const radioButtonsCurrentDivision = document.querySelectorAll('input[name="radio-group-current-division"]');
const radioButtonsDesiredDivision = document.querySelectorAll('input[name="radio-group-desired-division"]');
const makrs_on_current_rank_selected = document.querySelector('.current-marks-select');
const makrs_on_current_rank = document.querySelectorAll('.current-marks');
const division_server_select_element = document.querySelector('.division-servers-select');

const role_selected = document.querySelector('.role-select');

// All Checkbox
const extraOptions = document.querySelectorAll('input[name="extra-checkbox"]');
const duoBoosting = document.querySelector('input[name="switch-between-solo-duo"][value="duo"]')
const soloBoosting = document.querySelector('input[name="switch-between-solo-duo"][value="solo"]')

const promo_form = document.querySelector('.discount form');

// Checkbox
const soloOrDuoBoosting = document.querySelectorAll('input[name="switch-between-solo-duo"]');
let total_Percentage = 0; // inital value for Additional value 
let discount_amount = 0 // inital value of discount
console.log();