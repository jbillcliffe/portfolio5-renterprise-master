function getCreateOrderItemTypes(){

    let categorySelectElement = document.getElementById("id_category");
    let typeSelectElement = document.getElementById('id_item_type');
    let categoryOptions = categorySelectElement.options;
    let typeOptions = typeSelectElement.options;
    console.log(categorySelectElement);
    console.log(categoryOptions);
    console.log(typeOptions);
    // Reset the type select each time
    typeSelectElement.selectedIndex = 0;
    typeSelectElement.disabled = false;
    // Get the selected category
    let categoryString;


    //let categoryString2 = categorySelectElement.option.innerHTML;
    for (let x = 0; x < categoryOptions.length; x++) {

        let option = categoryOptions[x];
        if (option.selected == true) {
            if (option.value == "")
            {
                typeSelectElement.selectedIndex = 0;
                typeSelectElement.disabled = true;
            } else {
                categoryString = option.innerText;
            }
            break;
        } else {
            // do nothing.
        }
    }

    console.log(categoryString);

    // Iterate through all the types
    for (let x = 0; x < typeOptions.length; x++) {

        // Get the category of the current type iteration
        let thisOption = typeOptions[x];
        let optionValue = thisOption.value;

        // If the category on this element matches the category selection,
        // remove any d-none class applied.
        if (optionValue == "") {
            //do nothing, the unselected value should always be visible
        
        } else if (optionValue.includes(categoryString)) {
            if (thisOption.classList.contains("d-none")) {
                thisOption.classList.remove("d-none");
            } else {
                // Class not present, no need to remove
            }
        } else {
            // If the category on the element does not match the selection
            if (thisOption.classList.contains("d-none")) {
                // Does not need to be added more than once
            } else {
                // Remove any d-none class present
                thisOption.classList.add("d-none");
            }
        }
    }
}