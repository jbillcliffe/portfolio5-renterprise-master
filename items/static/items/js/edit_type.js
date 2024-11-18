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

function submitItemTypeForm(event){
    // Prevent default form submission (navigate to the URL)
    event.preventDefault();
    //Want to disable further submissions while waiting for response.
    $('#edit-type-submit-button').attr('disabled', true)
    $('#edit-type-cancel-button').attr('disabled', true)
}

function typeCategoryChanged(categoryString){
    let categoryListElements = document.getElementsByClassName('type-category-list-item');
    
    for ( let x = 0; x < categoryListElements.length; x++ ) {

        // If the selection made matches the currently iterated list item.
        if (categoryListElements[x].innerText == categoryString) {
            // Set the style of the element to be "list-active"
            categoryListElements[x].className = "dropdown-item type-category-list-item list-active";
            
        } else {
            // Otherwise, set the element to the default css below
            categoryListElements[x].className = "dropdown-item type-category-list-item";
        }
    }

    //Get original category value
    originalCategory = $('#id_edit-type-category').val();

    //Compare against selection to determine if there has been a change.
    //If no change
    if (originalCategory == categoryString){
        // Do Nothing, there has been no change
    } else {
        $('#edit-type-image').attr('src','/static/images/default.webp');
        $('#edit-type-image').attr('alt','No Image');
        $('#id_edit-type-category').val(categoryString);
        $('#id_edit-type-name').val('');
        changeTypesAvailable(categoryString);
    }
}

function changeTypesAvailable(categoryString){
    //li-#, li-a-#
    //the <li> element which will need d-none or not, depending on if it's category is correct.
    let typeListElements = document.getElementsByClassName('edit-type-list-item ');
    //let typeATagElements = document.getElementsByClassName('dropdown-item type-name-list-item ');

    for ( let x = 0; x < typeListElements.length; x++){
        let getId = typeListElements[x].id;
        getId = getId.replace('li-', '');
        let relativeATag = document.getElementById('li-a-'+getId);

        if ($(relativeATag).attr('data-category') == categoryString){
            typeListElements[x].className = "edit-type-list-item";
        } else {
            typeListElements[x].className = "edit-type-list-item d-none";
        }
    }
}

function typeChanged(typeId){
    //Data Attrs : data-img, data-category, data-sku, data-initial, data-week
    //Field Ids : id_edit-type-name, id_edit-type-sku, id_edit-type-cost_initial, id_edit-type-cost_week
    let selectedTypeOption = document.getElementById("li-a-"+typeId);

    $('#edit-type-image').attr('src', '/media/'+$(selectedTypeOption).attr('data-img'));
    $('#edit-type-image').attr('alt', $(selectedTypeOption).val());
    console.log( $('#id_edit-type-name').val());
    console.log( selectedTypeOption.innerText);
    console.log($(selectedTypeOption).attr('data-sku'));
    $('#id_edit-type-name').val(selectedTypeOption.innerText);
    $('#id_edit-type-sku').val($(selectedTypeOption).attr('data-sku'));
    $('#id_edit-type-cost_initial').val($(selectedTypeOption).attr('data-initial'));
    $('#id_edit-type-cost_week').val($(selectedTypeOption).attr('data-week'));
}

//typeChanged( '5', 'Bathlift', 'Bathroom Accessories', 'orca-bathlift.webp' )

function resetFormImage(){
    /* Set the image to be the same as the one from the item view */
    $('#edit-type-image').attr('src', $('#item-image-id').attr('src'));
    $('#edit-type-image').attr('alt', $('#item-image-id').attr('alt'));
}