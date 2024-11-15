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
}
