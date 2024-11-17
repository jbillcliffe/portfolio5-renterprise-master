function submitItemTypeForm(event){
    // let amount_paid = document.getElementById("invoice-modal-create-amount-paid").value;
    // let note = document.getElementById("invoice-modal-create-note").value;

    // //trigger the form validation on required fields before submitting
    // if(document.forms["invoice-create-form"].reportValidity() == false) {
    //     //do no further functions as it is not valid
    // } else {
    //     //set href of hidden confirm button, after grabbing values to post
    //     let paidURL = `${orderId}/invoice_create/${amount_paid}/${note}/`;
    //     let submitButton = document.getElementById("hidden-invoice-create-confirm");
    //     submitButton.href = paidURL;
    //     submitButton.click(); 
    // }

    // Prevent default form submission (navigate to the URL)
    event.preventDefault();
    //Want to disable further submissions while waiting for response.
    $('#edit-type-submit-button').attr('disabled', true)
    $('#edit-type-cancel-button').attr('disabled', true)
}

function setTypeCategory(categoryString){
    console.log(categoryString);
    $('#edit-type-image').attr('src','/static/images/default.webp');
    $('#id_edit-type-category').val(categoryString);
    $('#id_edit-type-name').val('');



    

}

function resetEditTypeForm(){
    //Name / Sku / Category / Initial / Weekly

    // Reset text in modal to be the same as the text in the item view
    // Name
    $('#id_edit-type-name').val($('#id_edit-item-item_type option:selected').text());
    // SKU
    $('#id_edit-type-sku').val($('#id_item_type_sku').val());
    //Category
    //Cost Initial
    $('#id_edit-type-cost_initial').val($('#id_type-cost_initial').val());
    //Cost Week
    $('#id_edit-type-cost_week').val($('#id_type-cost_week').val());
}