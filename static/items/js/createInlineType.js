function getAvailableTypes(){

    let categorySelectElement = document.getElementById("id-category-select");
    let typeSelectElement = document.getElementById('id_item_type');
    let imageDisplayElement = document.getElementById('id-image-display');

    // Reset the type select each time
    typeSelectElement.selectedIndex = 0;
    typeSelectElement.disabled = false;
    // Reset the image display each time
    imageDisplayElement.src = "/static/images/default.webp";
    imageDisplayElement.alt = "default no image";

    
    // Get all the types in the type dropdown
    let typeOptionElements = document.getElementsByClassName('type-option-item');
    // Get the selected category
    let categoryString = categorySelectElement.value;

    // Iterate through all the types
    for (let x = 0; x < typeOptionElements.length; x++) {

        // Get the category of the current type iteration
        let thisCategory = typeOptionElements[x].dataset.category;

        // If the category on this element matches the category selection,
        // remove any d-none class applied.
        if (thisCategory == categoryString) {
            if (typeOptionElements[x].classList.contains("d-none")) {
                typeOptionElements[x].classList.remove("d-none");
            } else {
                // Class not present, no need to remove
            }
        } else {
            // If the category on the element does not match the selection
            if (typeOptionElements[x].classList.contains("d-none")) {
                // Does not need to be added more than once
            } else {
                // Remove any d-none class present
                typeOptionElements[x].classList.add("d-none");
            }
        }
    }
}

function displayTypeImage() {
    let typeSelectElement = document.getElementById('id_item_type');
    let imageDisplayElement = document.getElementById('id-image-display');

    //Get parts of the <option> of a <select>
    //https://stackoverflow.com/questions/14976495/get-selected-option-text-with-javascript

    imageDisplayElement.src = typeSelectElement.options[typeSelectElement.selectedIndex].dataset.image;
    imageDisplayElement.alt = typeSelectElement.options[typeSelectElement.selectedIndex].text;
}