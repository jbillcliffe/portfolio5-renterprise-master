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

function setTypeCategory(categoryString){
    console.log(categoryString);
    let categoryListElements = document.getElementsByClassName('type-category-list-item');
    
    for ( let x = 0; x < categoryListElements.length; x++ ) {

        //set to none on click to start.
        //categoryListElements[x].onclick = "";
        //if the selection made matches the currently iterated list item. 
        if (categoryListElements[x].innerText == categoryString) {
            categoryListElements[x].className = "dropdown-item type-category-list-item list-active";
            
        } else {
            
            categoryListElements[x].onclick = function(){setTypeCategory(categoryListElements[x].innerText)};
            categoryListElements[x].className = "dropdown-item type-category-list-item";
        }
    }
    //for each of the elements, if the selected category matches the element category the 
    //class needs to be list-active and to not have an onclick function (this disables this function
    //for the item)
    //If the 
    //set each to "dropdown-item type-category-list-item"

    //if matching category set to "dropdown-item type-category-list-item list-active"

    //

    originalType = $('#id_edit-type-category').val();
    $('#edit-type-image').attr('src','/static/images/default.webp');
    $('#id_edit-type-category').val(categoryString);
    $('#id_edit-type-name').val('');

    

}

function resetFormImage(){
    /* Set the image to be the same as the one from the item view */
    $('#edit-type-image').attr('src', $('#item-image-id').attr('src'));
    $('#edit-type-image').attr('alt', $('#item-image-id').attr('alt'));
}