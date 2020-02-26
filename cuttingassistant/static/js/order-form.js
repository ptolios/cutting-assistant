document.addEventListener('DOMContentLoaded', (event) => {
  // setup datepicker inputs
  let datepickers = document.querySelectorAll('.datepicker');
  let options = {
    'format': ' dd/mm/yyyy',
    'autoClose': 'true',
    'i18n': {
      'cancel': 'Ακυρο',
      'monthsShort': [
          'Ιαν',
          'Φεβ',
          'Μαρ',
          'Απρ',
          'Μαϊ',
          'Ιουν',
          'Ιουλ',
          'Αυγ',
          'Σεπ',
          'Οκτ',
          'Νοε',
          'Δεκ'
      ]
    }
  }
  let instances = M.Datepicker.init(datepickers, options);
  
  // The first item-row of the page is used as a template div
  // to copy from
  let firstItemRow = document.querySelector('.item-row:first-child');
  templateItemRow = firstItemRow.cloneNode(true);
  // templateItemRow = document.querySelector('.item-row:first-child');
  let firstMaterialForm = document.querySelector('.material-form:first-child');
  templateMaterialForm = firstMaterialForm.cloneNode(true);
  materialWrapper = document.querySelector('.material-form-wrapper');
  // Make sure the item-rows buttons are shown/hidden appropriately
  itemRows = document.getElementsByClassName('item-row');
  for (let itemRow of itemRows) {
    manageButtonOf(itemRow);
  }
});


function manageButtonOf (itemRow) {
  // Shows button if all inputs are filled
  // and hides it if they aren't.


  let quantity = itemRow.querySelector('input[id$="quantity"]');
  let x_dimension = itemRow.querySelector('input[id$="x_dimension"]');
  let y_dimension = itemRow.querySelector('input[id$="y_dimension"]');

  let button = itemRow.querySelector('.var-btn');
  if ([quantity, x_dimension, y_dimension].every(elem => elem.value)) {
    button.classList.remove('hide');
  } else {
    button.classList.add('hide');
  }
}


function addRemoveItemRow () {
  // Depending on the class of the calling button
  // executes either 
  // the add or remove function
  let button = event.target;
  if (button.classList.contains('add')) {
    addItemRow(button);
  } else if (button.classList.contains('remove')) {
    removeItemRow(button);
  }
}

function addItemRow (button) {
  let newRow = templateItemRow.cloneNode(true);
  
  // Update css classes
  button.classList.remove('add', 'teal');
  button.classList.add('remove', 'red')
  // Change icon
  icon = button.querySelector('.material-icons')
  icon.innerHTML = 'delete'

  let totalFormsInput = document.querySelector('#id_' + orderitemFormsetPrefix + '-TOTAL_FORMS');
  let totalForms = totalFormsInput.value;
  let newRowIndex = parseInt(totalForms);
  
  // Fill in the hidden material input
  // according to the material-form material
  let thisItemRow = button.closest('.item-row');
  let thisMaterial = thisItemRow.querySelector('input[id$="material"]');
  let materialInput = button.closest('.material-form').querySelector('[name="material"]');
  let material = materialInput.value;
  thisMaterial.value = material;
  
  // append the newly created .item-row to the end of the .items div
  let itemsDiv = button.closest('.items');
  setupNewItemRow(newRow, material, newRowIndex);
  itemsDiv.appendChild(newRow);
  newRow.querySelector('input[id$="quantity"]').focus();
  totalFormsInput.value = newRowIndex + 1;
}

function setupNewItemRow (itemRow, material, rowIndex) {
  itemRowButton = itemRow.querySelector('.var-btn');
  itemRowButton.classList.remove('remove', 'red');
  itemRowButton.classList.add('add', 'teal');
  itemRowButton.classList.add('hide');
  icon = itemRowButton.querySelector('.material-icons');
  icon.innerHTML = 'add';

  updateItemRowIndex (itemRow, material, rowIndex);
}

function updateItemRowIndex (itemRow, material, rowIndex) {
  // If 'material' is null or undefined ( not string, in any case), only update the index
  regex = new RegExp(orderitemFormsetPrefix + '-\\d+-', 'g')
  
  let inputElements = itemRow.querySelectorAll('[id^="id_' + orderitemFormsetPrefix + '-"]');
  inputElements.forEach((inputElement) => {
    // And update the id and name attributes of the inputs
    inputElement.id = inputElement.id.replace(regex, orderitemFormsetPrefix + '-' + rowIndex  + '-');
    inputElement.name = inputElement.name.replace(regex, orderitemFormsetPrefix + '-' + rowIndex  + '-');
    
    let labelElements = itemRow.querySelectorAll('[for^="id_' + orderitemFormsetPrefix + '-"]');
    //Update the for attribute of the labels
    labelElements.forEach((labelElement) => {
      let labelFor = labelElement.getAttribute('for');
      labelFor = labelFor.replace(regex, orderitemFormsetPrefix + '-' + rowIndex  + '-');
      labelElement.setAttribute('for', labelFor);
    });
    
    // If the material arg is provided, clear the value of the inputs 
    // and fill in the material value of the 'material' input 
    // Otherwise, do nothing (just update the index of each input and label)

    isMaterialProvided = (typeof(material)==='string') ? true : false;
    if (isMaterialProvided) {
      if (inputElement.id.endsWith('material')) {
        inputElement.value = material
      } else {
        inputElement.value = ''
      }
    }
  });
}

function removeItemRow (itemRowButton) {
  let itemsDiv = itemRowButton.closest('.items')
  let itemRow = itemRowButton.closest('.item-row');
  itemsDiv.removeChild(itemRow);
  reIndexElements();
}

function reIndexElements () {
  // Renumber all inputs' and labels' ids and names
  let itemRows = document.querySelectorAll('.item-row');
  let totalFormsInput = document.querySelector('#id_' + orderitemFormsetPrefix + '-TOTAL_FORMS');
  totalFormsInput.value = itemRows.length;
  for (let [index, itemRow] of itemRows.entries()) {
    updateItemRowIndex(itemRow, null, index);
  }
}


function fillHiddenInput () {
  // Whenever the material field is given 
  // fill in all the hidden 'material' inputs
  // of the calling material form
  let material = event.target.value;
  let materialForm = event.target.closest('.material-form');
  let itemrowMaterialInputs = materialForm.querySelectorAll('input[id$="material"]');
  for (let materialInput of itemrowMaterialInputs) {
    materialInput.value = material
  }
}


function addMaterialForm () {
  let newMaterialForm = templateMaterialForm.cloneNode(true);
  materialWrapper.appendChild(newMaterialForm);
}


function cleanUp () {
  deleteEmptyItemRows();
  return true;
}

function deleteEmptyItemRows () {
  console.log('Checking for empty inputs...')
  let itemRows = document.querySelectorAll('.item-row');
  for (let itemRow of itemRows) {
    let quantity = itemRow.querySelector('input[id$="quantity"]');
    let x_dimension = itemRow.querySelector('input[id$="x_dimension"]');
    let y_dimension = itemRow.querySelector('input[id$="y_dimension"]');

    if ([quantity, x_dimension, y_dimension].every((elem)=> elem.value===(undefined || ''))) {
      itemRow.remove();
    }
    reIndexElements();
  }
}
