

// Changed from getting known ids generated to this, it means that additional
// future statuses can be included with no extra coding here.
let switchElementArray = document.querySelectorAll('[id^="id-status-"]');

function statusSwitchChanger(sentStatus) {
    // When the modal is loaded, set the current status switch to be on.
    // This also works as a function for when one of the switches is toggled
    // manually.

    // Create a string that is the same as the id from the sending switch,
    // or the modal button which has the status also attached
    let switchIdSearchString = "id-status-"+sentStatus;

    for ( let x = 0; x < switchElementArray.length; x++) {
        // If the matching element in the array is found
        if (switchElementArray[x].id == switchIdSearchString) {
            // Set it to checked
            switchElementArray[x].checked = true;
            document.getElementById('id_status').value = switchElementArray[x].value;
        } else {
            // Otherwise, make sure it isn't checked
            switchElementArray[x].checked = false;
        }
    }
}

