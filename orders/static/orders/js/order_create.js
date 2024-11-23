// Needs double parse. After one it is a string. But converts to accessible objects after two
const fullItemList = JSON.parse(JSON.parse(document.getElementById('json-item-list').textContent));
const fullOrderList = JSON.parse(JSON.parse(document.getElementById('json-order-list').textContent));

// Define the category and type selectors.
let categorySelectElement = document.getElementById("id_category");
let typeSelectElement = document.getElementById('id_item_type');

function validateDates(){

    let deliveryDate = new Date(document.getElementById("id_delivery_date").value).setHours(0, 0, 0, 0);
    let collectDate = new Date(document.getElementById("id_collect_date").value).setHours(0, 0, 0, 0);
    let preType = typeSelectElement.value.split("|");
    let typeId = preType[0];
    let typeCategory = preType[1];
    //let typeName = typeElement.textContent;

    const today = new Date().setHours(0, 0, 0, 0);

    console.log(preType);

    if (deliveryDate == "Invalid Date" || collectDate == "Invalid Date") {
        //console.log("only one date set")
        
        if (deliveryDate < today) {
            //console.log("Less than today");
        } else if (collectDate < today) {
            //console.log("Less than today");
        }
    } else if (deliveryDate && collectDate) {
        if (deliveryDate < today || collectDate < today) {
            //console.log("either date selected is less than today");
        } else if (collectDate < deliveryDate) {
            //console.log("cannot have a delivery after collection");
        } else if (deliveryDate == collectDate){
            //console.log("same date");
        } else {
            //console.log("valid");
            if (!typeSelectElement.value) {
                //console.log("Type still needs selecting");
            } else {
                console.log("Stock availability")
                let assetsOwned = [];
                for (let x = 0; x < fullItemList.length; x++) {
                    if (fullItemList[x].fields.item_type == typeId) {
                        assetsOwned.push(fullItemList[x]);
                    }
                } 
                if (assetsOwned.length == 0) {
                    console.log("None of these are owned");
                } else {
                    getAvailableStockAfterOrders(assetsOwned, deliveryDate, collectDate);
                }
            }
        }
    } else {
        // should not be an error. Either there are two dates, or not
    }
}

function getAvailableStockAfterOrders(assetList, deliveryCheck, collectCheck) {
    
}


function getCreateOrderItemTypes(){

    let categoryOptions = categorySelectElement.options;
    let typeOptions = typeSelectElement.options;
    // Reset the type select each time
    typeSelectElement.selectedIndex = 0;
    typeSelectElement.disabled = false;
    // Get the selected category
    let categoryString;

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