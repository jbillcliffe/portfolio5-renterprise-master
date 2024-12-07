// Needs double parse. After one it is a string. But converts to accessible objects after two
const fullItemList = JSON.parse(JSON.parse(document.getElementById('json-item-list').textContent));
const fullItemTypesList = JSON.parse(JSON.parse(document.getElementById('json-item-type-list').textContent));
const fullOrderList = JSON.parse(JSON.parse(document.getElementById('json-order-list').textContent));
console.log(fullOrderList);

// Define the category and type selectors.
let categorySelectElement = document.getElementById("id_category");
let typeSelectElement = document.getElementById('id_item_type');

let stockCollapseDiv = document.getElementById('stock-collapse');
let stockCollapseInner = document.getElementById('stock-collapse-inner');

let costInitialField = document.getElementById('id_cost_initial');
let costWeekField = document.getElementById('id_cost_week');

function validateDates(){

    let startDate = new Date(document.getElementById("id_start_date").value);
    let endDate = new Date(document.getElementById("id_end_date").value);
    let today = new Date();
    startDate.setHours(0);
    endDate.setHours(0);
    today.setHours(0);

    let preType = typeSelectElement.value.split("|");
    let typeId = preType[0];
    let typeCategory = preType[1];

    if(!typeSelectElement.value) {
    } else {
        // To have a type selected, a category must be selected too
        // Input the costs for the item.
        for (let x = 0; x < fullItemTypesList.length; x++)
        {
            if (fullItemTypesList[x].pk == typeId) {
                costInitialField.value = fullItemTypesList[x].fields.cost_initial;
                costWeekField.value = fullItemTypesList[x].fields.cost_week;
            }
        }
    }

    if (startDate == "Invalid Date" || endDate == "Invalid Date") {
        console.log("only one date set")
        
        if (startDate < today) {
            console.log("Less than today");
        } else if (endDate < today) {
            console.log("Less than today");
        }
    } else if (startDate && endDate) {
        if (startDate < today || endDate < today) {

            if (stockCollapseInner.classList.contains("card-warning")){
            } else {
                stockCollapseInner.classList.add("card-warning")
            }
            stockCollapseInner.innerHTML = `Dates cannot be before today.`;
            if (stockCollapseDiv.classList.contains("show")) {
            } else {
                $(stockCollapseDiv).collapse('show');
            }

        } else if (endDate < startDate) {
            if (stockCollapseInner.classList.contains("card-warning")){
            } else {
                stockCollapseInner.classList.add("card-warning")
            }
            stockCollapseInner.innerHTML = `Order end must be after start`;
            if (stockCollapseDiv.classList.contains("show")) {
            } else {
                $(stockCollapseDiv).collapse('show');
            }
            
        } else if (startDate == endDate){
            if (stockCollapseInner.classList.contains("card-warning")){
            } else {
                stockCollapseInner.classList.add("card-warning")
            }
            stockCollapseInner.innerHTML = `Cannot start and end the order on the same day`;
            if (stockCollapseDiv.classList.contains("show")) {
            } else {
                $(stockCollapseDiv).collapse('show');
            }
            
        } else {
            if (!typeSelectElement.value) {
                if (stockCollapseInner.classList.contains("card-warning")){
                } else {
                    stockCollapseInner.classList.add("card-warning")
                }
                stockCollapseInner.innerHTML = `Select a type to check stock.`;
                if (stockCollapseDiv.classList.contains("show")) {
                } else {
                    $(stockCollapseDiv).collapse('show');
                }
                
            } else {
                
                let assetsOwned = [];
                for (let x = 0; x < fullItemList.length; x++) {
                    if (fullItemList[x].fields.item_type == typeId) {
                        assetsOwned.push(fullItemList[x]);
                    }
                } 

                if (assetsOwned.length == 0) {
                    if (stockCollapseInner.classList.contains("card-warning")){
                    } else {
                        stockCollapseInner.classList.add("card-warning")
                    }
                    stockCollapseInner.innerHTML = `None of these are owned.`;
                    if (stockCollapseDiv.classList.contains("show")) {
                    } else {
                        $(stockCollapseDiv).collapse('show');
                    }
                } else {
                    for (let x = 0; x < fullItemTypesList.length; x++)
                    {
                        if (fullItemTypesList[x].pk == typeId) {
                            costInitialField.value = fullItemTypesList[x].fields.cost_initial;
                            costWeekField.value = fullItemTypesList[x].fields.cost_week;
                        }
                    }
                    
                    $(stockCollapseDiv).collapse('hide');
                    getAvailableStockAfterOrders(JSON.stringify(assetsOwned), startDate, endDate, typeCategory);
                }
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

function getAvailableStockAfterOrders(assetList, newStart, newEnd, selectedCategory) {
    
    //console.log("INIT: "+assetList)
    let availableChoices = [];
    assetList = JSON.parse(`${assetList}`);
    
    //start by loading each item.
    for (let x = 0; x < assetList.length; x++) {
        let newItemObject = assetList[x];
        let newItem = newItemObject.pk;
        //console.log(`Item : ${newItem}`)

        //first check it is available and double check against a repair date on the item
        if (assetList[x].fields.status == 0 && !assetList[x].fields.repair_date) {
            //if they both resolve correctly, it needs to be checked against the orders.    
            //begin searching the order history
            for (let y = 0; y < fullOrderList.length; y++) {
                //get the start date and end date of this order
                let oldStart = new Date(fullOrderList[y].fields.start_date);
                let oldEnd = new Date(fullOrderList[y].fields.end_date);
                let oldItem = fullOrderList[y].fields.item;

                
                //first is the item x, in the order of y.
                if (newItem == oldItem) {
                    //Although there is another booking, do the dates clash?
                    if (areDatesClear(newStart, newEnd, oldStart, oldEnd) == true) {
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
        if (stockCollapseInner.classList.contains("card-warning")){
            stockCollapseInner.classList.remove("card-warning")
        }
        stockCollapseInner.innerHTML = `${availableChoices.length} out of ${assetList.length} available`;

        autoSelectStock(JSON.stringify(availableChoices));
    } else {
        if (stockCollapseInner.classList.contains("card-warning")){
        } else {
            stockCollapseInner.classList.add("card-warning")
        }
        stockCollapseInner.innerHTML = `There are none in stock for these dates. Try something else.`;
    }
    $(stockCollapseDiv).collapse('show');
}


function autoSelectStock(availableItems) {
    availableItems = JSON.parse(`${availableItems}`);
    let itemSelect;
    for (let x = 0; x < availableItems.length; x++) {
        let newItemObject = availableItems[x];

        // Iterate through the available items and see which has made the least money.
        // Automatically assign that one to the order.
        if (x ==  0)  {
            itemSelect = availableItems[x];
        } else {
            // if they match (most likely at 0.00) then don't change.
            if (newItemObject.fields.income < itemSelect.fields.income) {
                itemSelect = newItemObect;
            } else {
            }
        }
    }
    console.log(itemSelect);
    document.getElementById('id_item').value = itemSelect.pk;   
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