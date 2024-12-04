// Needs double parse. After one it is a string. But converts to accessible objects after two
const fullItemList = JSON.parse(JSON.parse(document.getElementById('json-item-list').textContent));
const fullItemTypesList = JSON.parse(JSON.parse(document.getElementById('json-item-type-list').textContent));
const fullOrderList = JSON.parse(JSON.parse(document.getElementById('json-order-list').textContent));
const dateErrors = document.getElementById('id-order-date-messages');
let currentItemType = document.getElementById('id_item_type').value;

let orderId = document.getElementById('despatches-tab-pane').dataset.originalStartDate;
let originalStartDate = document.getElementById('despatches-tab-pane').dataset.originalStartDate;
let originalEndDate = document.getElementById('despatches-tab-pane').dataset.originalEndDate;

let submitAllowed = false;

// This will stop any submissions without validation from the time the script is triggered
document.getElementById("id-date-change-submit").addEventListener(
    "click", function(event){
    event.preventDefault()
    
    if (submitAllowed == true) {
        document.getElementById("date-change-form").submit();
        //submitDateChanges()
    } else {
        // Do nothing.
    }
});

// Define the category and type selectors.

function validateDates(){

    let oldStartDate = new Date(Date.parse(originalStartDate));
    let oldEndDate = new Date(Date.parse(originalEndDate));
    let startDate = new Date(document.getElementById("id_start_date").value);
    let endDate = new Date(document.getElementById("id_end_date").value);
    let today = new Date();
    startDate.setHours(0);
    endDate.setHours(0);
    today.setHours(0);

    console.log("OLD START MS :"+oldStartDate.getTime());
    console.log("NEW START MS :"+startDate.getTime());
    console.log("OLD END MS :"+oldEndDate.getTime());
    console.log("NEW END MS :"+endDate.getTime());
    
    //id_item_type.value

    if (startDate == "Invalid Date" || endDate == "Invalid Date") {
        
        if (startDate < today) {
            errorSet('danger', `Start date cannot be before than today.`);
            
        } else if (endDate < today) {
            errorSet('danger', `End date cannot be before than today.`);
        }

        submitAllowed = false;
    
    } else if (startDate && endDate) {
        console.log("START - Old: "+oldStartDate+", New: "+startDate);
        console.log("END - Old: "+oldEndDate+", New: "+endDate);

        if (startDate < today && startDate.getTime() != oldStartDate.getTime()) {
            errorSet('danger', `Changed change start date to be before today. It can be left the same.`);
            submitAllowed = false;

        } else if (endDate < today && endDate.getTime() != oldEndDate.getTime()) {
            errorSet('danger', `Changed change end date to be before today. It can be left the same.`);
            submitAllowed = false;
        
        } else if (endDate < startDate) {
            errorSet('danger', `Order end must be after start`);
            submitAllowed = false;

        } else if (startDate == endDate){
            errorSet('danger', `Cannot start and end the order on the same day`);
            submitAllowed = false;

        } else {
            // Although this is a positive step through the functions.
            // It could still fail after this point, so submit is still not available.
            submitAllowed = false;
            let assetsOwned = [];
            for (let x = 0; x < fullItemList.length; x++) {
                if (fullItemList[x].fields.item_type == currentItemType) {
                    assetsOwned.push(fullItemList[x]);
                }
            } 
            console.log("OWNED: "+assetsOwned);
            if (assetsOwned.length == 0) {
                errorSet('danger', `None of these are owned.`);

            } else {
                getAvailableStockAfterOrders(JSON.stringify(assetsOwned), startDate, endDate);
            }
        }
    } else {
        // should not be an error. Either there are two dates, or not
        // Disable submit as there is an
        submitAllowed = false;
    }
}


/**
 * @param {JSON} assetList - list of items that match the type searched
 * @param {Date} startCheck - Date for order to start.
 * @param {Date} endCheck - Date for order to end.
 * @param {String} categoryOption - To offer others in the same category if none available.
 * 
 * 
 * A function to calculate if the date range on a new order is going to intercept
 * an old order. If it does, the function returns false to imply it is invalid.
 */

function getAvailableStockAfterOrders(assetList, newStart, newEnd) {
    
    let availableChoices = [];
    let currentItemId = document.getElementById('order-view-tab-content').dataset.itemId;
    let currentOrderId = document.getElementById('order-view-tab-content').dataset.orderId;
    
    assetList = JSON.parse(`${assetList}`);
    console.log("AL: "+assetList);

    //start by loading each item.
    for (let x = 0; x < assetList.length; x++) {
        let newItemObject = assetList[x];
        let newItem = newItemObject.pk;
        console.log("newIObject : "+newItemObject);
        console.log("newIPK : "+newItem);

        //first check it is available and double check against a repair date on the item
        if (assetList[x].fields.status == 0 && !assetList[x].fields.repair_date) {

            //if they both resolve correctly, it needs to be checked against the orders.    
            //begin searching the order history
            for (let y = 0; y < fullOrderList.length; y++) {

                //get the start date and end date of this order
                let oldStart = new Date(fullOrderList[y].fields.start_date);
                let oldEnd = new Date(fullOrderList[y].fields.end_date);
                let oldItem = fullOrderList[y].fields.item;
                
                //Is the item x, in the order of y.
                if (newItem == oldItem) {

                    //Although there is another booking, do the dates clash?
                    //Or, bypass this item if the order and item in question are this order and item.
                    //Therefore it is an amend process and a date change on itself is permitted.
                    if (areDatesClear(newStart, newEnd, oldStart, oldEnd) == true ||
                        ((fullOrderList[y].pk == currentOrderId) &&
                         (fullOrderList[y].fields.item == currentItemId))) {

                        //resolving as true, means the dates are clear.
                        if (y == fullOrderList.length - 1) {

                            // If this is the final order to check in the order list
                            availableChoices.push(JSON.stringify(newItemObject))
                            break;
                        } else {

                            // Still more orders to check. Cannot push yet
                            continue;
                        }

                    } else {

                        //this item has a reservation in those dates and therefore this item is unavailable.
                        break;
                    }

                } else {

                    // This item has not been booked in this order
                    if (y == fullOrderList.length - 1) {

                        // If this is the final order to check in the order list.
                        availableChoices.push(JSON.stringify(newItemObject))
                        break;

                    } else {

                        // Still more orders to check. Cannot push yet.
                        continue;
                    }
                }
            }
        } else {

            //it is not available, or it has a repair date on it.
            //Continue to the next item
            continue;
        }
    }
    // TEST ITEMS
    // let testChoices = [];
    // for (let z = 0; z < 2; z++)
    // {   
    //     testChoices.push(JSON.parse(`{"model":"items.item","pk":${z},"fields":{"item_type":5,"delivery_date":null,"collect_date":null,"repair_date":null,"income":"0.00","status":0}}`))
    // }
    // availableChoices = testChoices
    // console.log(testChoices)
    
    console.log("CHOICES : "+availableChoices);

    if (availableChoices.length > 0) {

        // All good, remove warning if there.
        errorSet('', '');

        // Check if the old item is in the available list
        for (let z = 0; z < availableChoices.length; z++)
        {   
            parsedChoiceObject = JSON.parse(availableChoices[z]);
            console.log("availableChoices Z PARSE: "+JSON.parse(availableChoices[z]).pk)

            if (parsedChoiceObject.pk == currentItemId) {

                // Force it to pick the item already ordered. Much simpler and if it is close
                // to despatch date, then the likelihood is that item will lose money.
                console.log("found current item @ ("+z+"): "+parsedChoiceObject.pk)
                console.log("found current item @ ("+z+"): "+parsedChoiceObject.fields)
                autoSelectStock(JSON.stringify(parsedChoiceObject));
                break;

            } else {
                if (z == availableChoices.length - 1) {

                    //last item in the list to check for and it still has not
                    //found the current item available. So a selection needs to be
                    //made from the full array.
                    console.log("LASTCHANCE: "+JSON.stringify(availableChoices));
                    autoSelectStock(JSON.stringify(availableChoices));
                    getAvailableStockAfterOrders(JSON.stringify(assetsOwned), startDate, endDate);
                }
            }
        }

    } else {
        submitAllowed = false;
        errorSet('danger', `There are none in stock for these dates. Another Item would be required.`);
    }
}

function autoSelectStock(availableItems) {
    
    availableItems = JSON.parse(`[${availableItems}]`)
    console.log("START AVAILABLE : "+availableItems);
    console.log([availableItems[0]])
    console.log("AVAILABLE LEN : "+availableItems.length);
    console.log("TYPE: "+(typeof availableItems))
    console.log("AVAILABLE : "+availableItems);

    let itemSelect;
    for (let x = 0; x < availableItems.length; x++) {

        newItemObject = availableItems[x];
        console.log(newItemObject);

        if (x ==  0)  {
            itemSelect = availableItems[x];
        } else {
            // if they match (most likely at 0.00) then don't change.
            console.log("NIO Income : "+newItemObject.fields.income);
            console.log("IS Income : "+itemSelect.fields.income);
            if (newItemObject.fields.income < itemSelect.fields.income) {
                itemSelect = newItemObject;
            } else {
            }
        }
    }

    if (!itemSelect) {
        submitAllowed = false;
        errorSet('danger', 'No Item Selected');
    } else {

        let submitButton = document.getElementById('id-date-change-submit');
        let orderProfile = document.getElementById('order-view-tab-content').dataset.profileId;
        let orderId = document.getElementById('order-view-tab-content').dataset.orderId;
        let orderNote = buildOrderNote();
        console.log(orderNote);
        
        if (orderNote == "empty"){
            submitAllowed = false;
            submitButton.hidden = true;
            submitButton.disabled = true;
            errorSet('danger', 'No change required, dates are the same as before.');
            
        } else {
            submitAllowed = true;
            submitButton.hidden = false;
            submitButton.disabled = false;
            let orderItemEditURL = `/profiles/customers/${orderProfile}/order/${orderId}/edit/${orderNote}/?tab=despatches`
            document.getElementById("date-change-form").action = `${orderItemEditURL}`;
        }
    }
}
function areDatesClear(newStartDate, newEndDate, previousStartDate, previousEndDate) {
    /*  Situations -     
                        |---------OLDORDER---------|
    1.        |----NEWORDER----|                      
    2.                                |----NEWORDER----|
    3.                    |----NEWORDER----|
    4. |--NEWORDER--|             
    5.                                               |--NEWORDER--|
    6.   |--NEWORDER--|
    7.                |--NEWORDER--|
    8.                                           |--NEWORDER--|
    9.                              |--NEWORDER--|

        4 & 5 are the only "true" values as the new order dates do not intercept the old order dates.
    
        Would ideally look to have ongoing rentals (no collection), but not initially
        Comment directly taken from Portfolio 4 as it explains it well
        Check each item available for date clashes with historical orders
    */
    if ((newStartDate < previousStartDate) && (newEndDate < previousStartDate)) {
        // Both the new start date and new end date are before the
        // start date of the historical order (4)
        return true;
    } else if ((newStartDate > previousEndDate) && (previousEndDate != null)) {
        // Both new start date and new end date are after the
        // collection of the historical order (5). Also allowing for
        // it to not have an unknown collection date.
        return true;
    } else if ((newStartDate > previousEndDate) && (previousEndDate == null)) {
        // even though the start date is after the end date. If the historical order
        // still has no collection value, it could still be on hire at this time and 
        // is not available for the new order
        return false;
    } else {
        // Anything else is a clash
        return false;
    }
}

function errorSet(textClass, textMessage) {

    let errorClasses = dateErrors.classList;
    
    errorClasses.forEach(
        function(className, x) {
            errorClasses.remove(className);
        }
    )
    dateErrors.classList.add(`text-${textClass}`);
    dateErrors.textContent = textMessage;
    // for (let x = 0; x < classNumber;)
    // dateErrors.classList.remove();
    // dateErrors.classList.add(`text-${textClass}`);
}

function buildOrderNote() {
    
    // Get dates from form, set them to midnight to stop same days having different times.
    let newStartDate = new Date(document.getElementById("id_start_date").value);
    let newEndDate = new Date(document.getElementById("id_end_date").value);
    newStartDate.setHours(0);
    newEndDate.setHours(0);

    // Change the format of the Date from the dataset providing the values
    // and declare Booleans to detect if there is changes in the start and end dates.
    let oldStartDate = new Date(Date.parse(originalStartDate));
    let oldEndDate = new Date(Date.parse(originalEndDate));
    let startChange = false;
    let endChange = false;

    // Convert the dates into milliseconds relative to midnight of 01/01/1970.
    if (newStartDate.getTime() != oldStartDate.getTime())
    {
        startChange = true;
    }
    if (newEndDate.getTime() != oldEndDate.getTime())
    {
        endChange = true;
    }

    //Build the string for an OrderNote.
    let noteText = "";
    
    if (startChange == true && endChange == true)
    {
        noteText += "The start and end dates have been changed. ";
        noteText += `The previous start date was ${originalStartDate}`;
        noteText += `The previous end date was ${originalEndDate}`;

    } else if (startChange == false && endChange == true) {
        noteText += "The end date has been changed. ";
        noteText += `The previous end date was ${originalEndDate}`;
    } else if (startChange == true && endChange == false) {
        noteText += "The start date has been changed. ";
        noteText += `The previous start date was ${originalStartDate}`;
    } else {
        noteText = "empty"
    }
    
    // Return the result (built string or empty). If empty, then there will be
    // no opportunity to make a POST from the form.
    return noteText;

}