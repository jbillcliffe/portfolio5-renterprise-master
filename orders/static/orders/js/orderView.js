// Needs double parse. After one it is a string. But converts to accessible objects after two
const fullItemList = JSON.parse(JSON.parse(document.getElementById('json-item-list').textContent));
const fullItemTypesList = JSON.parse(JSON.parse(document.getElementById('json-item-type-list').textContent));
const fullOrderList = JSON.parse(JSON.parse(document.getElementById('json-order-list').textContent));
const dateErrors = document.getElementById('id-order-date-messages');
let currentItemType = document.getElementById('id_item_type').value;

// This will stop any submissions without validation from the time the script is triggered
document.getElementById("id-date-change-submit").addEventListener(
    "click", function(event){
    event.preventDefault()
});

// Define the category and type selectors.

function validateDates(){

    let startDate = new Date(document.getElementById("id_start_date").value);
    let endDate = new Date(document.getElementById("id_end_date").value);
    let today = new Date();
    startDate.setHours(0);
    endDate.setHours(0);
    today.setHours(0);
    
    //id_item_type.value

    if (startDate == "Invalid Date" || endDate == "Invalid Date") {
        console.log("only one date set")
        
        if (startDate < today) {
            console.log("Less than today");
        } else if (endDate < today) {
            console.log("Less than today");
        }
    } else if (startDate && endDate) {
        if (startDate < today || endDate < today) {
            errorSet('danger', `Changed dates cannot be before today.`);
            // if (dateErrors.classList.contains('text-danger')){
            // } else {
            //     //stockCollapseInner.classList.add("card-warning")
            //     if (dateErrors.classList.contains('text-success')){

            //     dateErrors.classList.remove('text-success').add("text-danger");
            // }
            
            // dateErrors.innerHTML = `Changed dates cannot be before today.`;

        } else if (endDate < startDate) {
            // if (dateErrors.classList.contains('text-danger')){
            // } else {
            //     dateErrors.classList.remove('text-success').add("text-danger");
            // }
            // dateErrors.innerHTML = `Order end must be after start`;
            errorSet('danger', `Order end must be after start`);

        } else if (startDate == endDate){
            // if (dateErrors.classList.contains('text-danger')){
            // } else {
            //     dateErrors.classList.remove('text-success').add("text-danger");
            // }
            // dateErrors.innerHTML = `Cannot start and end the order on the same day`;
            errorSet('danger', `Cannot start and end the order on the same day`);
        } else {

            let assetsOwned = [];
            for (let x = 0; x < fullItemList.length; x++) {
                if (fullItemList[x].fields.item_type == currentItemType) {
                    assetsOwned.push(fullItemList[x]);
                }
            } 

            if (assetsOwned.length == 0) {
                // if (dateErrors.classList.contains('text-danger')) {
                // } else {
                //     dateErrors.classList.remove('text-success').add("text-danger");
                // }
                // dateErrors.innerHTML = `None of these are owned.`;
                errorSet('danger', `None of these are owned.`);
            } else {

                getAvailableStockAfterOrders(JSON.stringify(assetsOwned), startDate, endDate);
            }
        }
    } else {
        // should not be an error. Either there are two dates, or not
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
    
    //start by loading each item.
    for (let x = 0; x < assetList.length; x++) {
        let newItemObject = assetList[x];
        let newItem = newItemObject.pk;

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
                            // If this is the final order to check in the order list.

                            availableChoices.push(newItemObject)
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
                        availableChoices.push(newItemObject)
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

    if (availableChoices.length > 0) {

        //Good, remove warning if there.
        //if (dateErrors.classList.contains('text-danger')){
        //    dateErrors.classList.remove('text-danger').add('text-success');
        errorSet('', ``);
        for (let z = 0; z < availableChoices.length; z++)
        {
            if (availableChoices[z].pk == currentItemId) {
                //make this the only choice for "autoSelectStock"
                autoSelectStock(JSON.stringify(availableChoices[z]));
                //dateErrors.innerHTML = `Assigning the original item to it's new dates.`;
                break;
            } else {
                if (z == availableChoices.length - 1) {
                    //last item in the list to check for and it still has not
                    //found the current item available. So a selection needs to be
                    //made from the full array.
                    autoSelectStock(JSON.stringify(availableChoices));
                }
            }
        }
        //} 
    } else {
        errorSet('danger', `There are none in stock for these dates. Another Item would be required.`);
        // if (dateErrors.classList.contains("text-danger")){
        // } else {
        //     dateErrors.classList.remove('text-success').add("text-danger");
        // }
        // dateErrors.innerHTML = `There are none in stock for these dates. Another Item would be required.`;
    }
}


function autoSelectStock(availableItems) {
    //console.log("AVAILABLE : "+availableItems);
    //availableItems = JSON.parse(`${availableItems}`);
    
    availableItems = "["+availableItems+"]";
    console.log("AVAILABLE : "+availableItems);
    availableItems = JSON.parse(availableItems);
    console.log(availableItems);
    console.log(availableItems[0].fields);
    let itemSelect;
    for (let x = 0; x < availableItems.length; x++) {
        let newItemObject = availableItems[x];
        console.log("OBJECT "+x+": "+newItemObject)
        // Iterate through the available items and see which has made the least money.
        // Automatically assign that one to the order.
        if (x ==  0)  {
            itemSelect = JSON.stringify(availableItems[x]);
        } else {
            // if they match (most likely at 0.00) then don't change.
            if (newItemObject.fields.income < itemSelect.fields.income) {
                itemSelect = JSON.stringify(newItemObect);
            } else {
            }
        }
    }
    console.log("ITEM SELECT : "+itemSelect)
    let submitButton = document.getElementById('id-date-change-submit');
    submitButton.hidden = false;
    submitButton.disabled = false

    let orderItem = document.getElementById('order-view-tab-content').dataset.itemId;
    let orderProfile = document.getElementById('order-view-tab-content').dataset.profileId;
    let orderId = document.getElementById('order-view-tab-content').dataset.orderId;
    let originalStart = document.getElementById('order-view-tab-content').dataset.originalStartDate;
    let originalEnd = document.getElementById('order-view-tab-content').dataset.originalStartEnd;
    let orderNote;
    // itemSelect = JSON.parse(itemSelect);
    console.log("final select : "+itemSelect.pk)
    if (itemSelect.pk == orderItem) {
        orderNote = `Item ${itemSelect.fields.item_serial} rebooked. Previous Start Date : ${originalStart}, Previous End Date : ${originalEnd}`
    }
    let orderItemEditURL = `/profiles/customers/${orderProfile}/order/${orderId}/edit/${orderNote}/?tab=despatches`
    document.getElementById("date-change-form").action = `${orderItemEditURL}`;
    //document.getElementById("date-change-form").submit();
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
    if (textClass == '') {
        
    } else {
        if (dateErrors.classList.contains('text-danger')) {
            dateErrors.classList.remove('text-danger');
        }
        if (dateErrors.classList.contains('text-success')) {
            dateErrors.classList.remove('text-success');
        }
        dateErrors.classList.add(textClass);
    }
    dateErrors.innerHTML = textMessage;
}