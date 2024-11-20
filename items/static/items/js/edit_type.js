// 
// setCategoryFunctions();

// function setCategoryFunctions(){
//     for ( let x = 0; x < categoryListElements.length; x++ ) {
//         if (categoryListElements[x].innerText == categoryString) {
//             categoryListElements[x].className = "dropdown-item type-category-list-item list-active";
//             categoryListElements[x].onclick = function(){};
//         } else {
            
//             categoryListElements[x].onclick = function(){setTypeCategory(categoryString)};
//             categoryListElements[x].className = "dropdown-item type-category-list-item";
//         }
//     }
// }

// function submitItemTypeForm(event){
//     // Prevent default form submission (navigate to the URL)
//     event.preventDefault();
//     //Want to disable further submissions while waiting for response.
//     $('#edit-type-submit-button').attr('disabled', true)
//     $('#edit-type-cancel-button').attr('disabled', true)
// }

function typeCategoryChanged(categoryString, from_where){
    console.log("category value : " +categoryString);
    console.log("1."+from_where);

    let categoryListElements = document.getElementsByClassName('type-category-list-item');
    let categoriesAvailable = [];

    let dropdownButton = document.getElementById('id-types-dropdown-btn');

    let imageElement = document.getElementById('edit-type-image');
    let imageTextElement = document.getElementById('image-input-id');

    let categoryElement = document.getElementById('id_edit-type-category');
    let typeNameElement = document.getElementById('id_edit-type-name');
    let skuElement = document.getElementById('id_edit-type-sku');
    let initialCostElement = document.getElementById('id_edit-type-cost_initial');
    let weekCostElement = document.getElementById('id_edit-type-cost_week');

    for ( let x = 0; x < categoryListElements.length; x++ ) {
        
        categoriesAvailable.push(categoryListElements[x].innerHTML.trim());

        // If the selection made matches the currently iterated list item.
        if (categoryListElements[x].innerText.trim() == categoryString) {
            if ( from_where == "rerun" ) {
                console.log("found at : "+categoryListElements[x].innerText);
            }
            // Set the style of the element to be "list-active"
            categoryListElements[x].className = "dropdown-item type-category-list-item list-active";
        } else {
            // Otherwise, set the element to the default css below
            categoryListElements[x].className = "dropdown-item type-category-list-item";
        }
    }

    console.log(categoriesAvailable);
    //Get original category value
    let originalCategory = categoryElement.value;
    
    //Compare against selection to determine if there has been a change.
    console.log("2."+from_where);
    //If no change
    if ( from_where == "drop" || from_where == "rerun" ) {
        dropdownButton.disabled = false;
        if (originalCategory == categoryString && from_where == "drop"){
            // Do Nothing, there has been no change
            console.log("Same category as before");
        } else {

            imageElement.src = '/static/images/default.webp';
            imageElement.alt = 'No Image';
            imageTextElement.value = 'No Image';

            categoryElement.value = categoryString;
            typeNameElement.value = '';
            skuElement.value = '';
            initialCostElement.value = '';
            weekCostElement.value = '';

            changeTypesAvailable(categoryString);

        }
    } else {
        console.log("Input string : "+categoryString);

        if (categoriesAvailable.includes(categoryString) == true) {
            //found in original categories.
            //Rerun the function as if from the drop to reset the types
            typeCategoryChanged(categoryString, "rerun");
        } else {
            
            dropdownButton.disabled = true;
            imageElement.src = '/static/images/default.webp';
            imageElement.alt = 'No Image';
            imageTextElement.value = 'No Image';

            categoryElement.value = categoryString;
            typeNameElement.value = '';
            skuElement.value = '';
            initialCostElement.value = '';
            weekCostElement.value = '';

        }
    }
}

function changeTypesAvailable(categoryString){
    //li-#, li-a-#
    // The <li> element which will need d-none or not, depending on if it's category is correct.
    let typeListElements = document.getElementsByClassName('edit-type-list-item');
    // The button which is the dropdown of types available by category
    console.log(typeListElements);
    // Go through each list item and set it to not be visible if it does not match the category.
    for ( let x = 0; x < typeListElements.length; x++){
        let getId = typeListElements[x].id;

        //remove the li- to get the id of the li element.
        getId = getId.replace('li-', '');

        //To get the relative a tag element which holds the extra data
        let relativeATag = document.getElementById('li-a-'+getId);

        // Set the display to none if it is not the right category.
        if (relativeATag.dataset.category == categoryString){
            typeListElements[x].className = "edit-type-list-item";
        } else {
            typeListElements[x].className = "edit-type-list-item d-none";
        }
    }
}

function typeChanged(typeId = null){
    
    // The typeChanged gives the typeId from a dropdown li choice.
    // If it remains null it is because the type name input field is being
    // modified.
    // If it comes from the dropdown, it has values to work with. If this function
    // comes from the input then there is the possibility of creating a new type.
    // OR, even entering manually a type that already exists in the category.
    // The same item name in a different category is a different type and would have
    // to be created.
   
    let imageElement = document.getElementById('edit-type-image');
    let imageTextElement = document.getElementById('image-input-id');
    let typeNameElement = document.getElementById('id_edit-type-name');
    let skuElement = document.getElementById('id_edit-type-sku');
    let initialCostElement = document.getElementById('id_edit-type-cost_initial');
    let weekCostElement = document.getElementById('id_edit-type-cost_week');

    if (typeId == null) {
        //edit-type-list-item

    } else {

        let selectedTypeOption = document.getElementById("li-a-"+typeId);

        imageElement.src = '/media/'+selectedTypeOption.dataset.img;
        imageElement.alt = selectedTypeOption.value;
        imageTextElement.value = selectedTypeOption.dataset.img;

        typeNameElement.value = selectedTypeOption.innerText;
        skuElement.value = selectedTypeOption.dataset.sku;
        initialCostElement.value = selectedTypeOption.dataset.initial;
        weekCostElement.value = selectedTypeOption.dataset.week;
    }
    


    //$('#edit-type-image').attr('src', '/media/'+$(selectedTypeOption).attr('data-img'));
    //$('#edit-type-image').attr('alt', $(selectedTypeOption).val());

    //$('#id_edit-type-name').val(selectedTypeOption.innerText);
    //$('#id_edit-type-sku').val($(selectedTypeOption).attr('data-sku'));
    //$('#id_edit-type-cost_initial').val($(selectedTypeOption).attr('data-initial'));
    //$('#id_edit-type-cost_week').val($(selectedTypeOption).attr('data-week'));
}

//typeChanged( '5', 'Bathlift', 'Bathroom Accessories', 'orca-bathlift.webp' )



function resetFormImage(){
    /* Set the image to be the same as the one from the item view */
    $('#edit-type-image').attr('src', $('#item-image-id').attr('src'));
    $('#edit-type-image').attr('alt', $('#item-image-id').attr('alt'));
}

