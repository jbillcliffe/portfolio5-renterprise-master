function setTwoDecimalPlaces(elementId, initialNumber) {
    let number;
    
    if (!initialNumber) {
        number = "0.00"
    } else {
        number = parseFloat(initialNumber).toFixed(2);
    }

    document.getElementById(elementId).value = number;

    
}