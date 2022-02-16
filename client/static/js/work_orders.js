function validateNewWorkOrder(wo) {
    let val = {};
    //phone number 1
    if(wo.phone1 == null || wo.phone1.length < 10) {
        val.err = true;
        val.msg = 'Invalid Phone #';
    }
    return val;
}

function renderSubmission() {
    let isPFU;
    document.getElementsByName('isPurchasedFromUs').forEach((item) => {
        if (item.checked) {
            isPFU = getBooleanValue(item.value);
        }
    });
    let isUW;
    document.getElementsByName('isUnderWarranty').forEach((item) => {
        if (item.checked) {
            isUW = getBooleanValue(item.value);
        }
    });
    let isWPS;
    document.getElementsByName('isWithPowerSupply').forEach((item) => {
        if (item.checked) {
            isWPS = getBooleanValue(item.value);
        }
    });
    let workOrder = {
        'fname': document.getElementsByName('fname')[0].value,
        'lname': document.getElementsByName('lname')[0].value,
        'phone1': formatPhoneNumberToDigits(document.getElementsByName('phone1')[0].value),
        'phone2': formatPhoneNumberToDigits(document.getElementsByName('phone2')[0].value),
        'computer_type': document.getElementsByName('computer-type')[0].value,
        'model': document.getElementsByName('model')[0].value,
        'password': document.getElementsByName('password')[0].value,
        'isPurchasedFromUs': isPFU,
        'isUnderWarranty': isUW,
        'isWithPowerSupply': isWPS,
        'isWithOtherItems': (document.getElementsByName('other_items')[0].value.replace(/\s/g, '').length > 0 ? true : false),
        'other_items': document.getElementsByName('other_items')[0].value,
        'issue_category': document.getElementsByName('issue-type')[0].value,
        'issue_description': document.getElementsByName('issue-description')[0].value,
        'cashier': document.getElementsByName('cashier')[0].value
    }
    return workOrder;
}

function generateTableRow (woData) {
    let rowString = '';
    switch (woData.status) {
        case 'Completed':
        rowString = 
            '<tr id="tr_'+woData._id+'" class="align-middle" onclick="displayWorkOrder(this)">' + 
                '<td><div style="display: grid; grid-template-columns: 80% auto;">' + formatDateString(woData.dt_recieved) + generateDateBox(woData) + '</div></td>' +
                '<td>' + woData.fname + ' ' + woData.lname + '</td>' + 
                '<td>' + woData.model + ' (' + woData.computer_type + ') </td>' +
                '<td>' + (woData.price == null || woData.price <= 0 ? '$0.00': Intl.NumberFormat('en-US', {style: 'currency', currency: 'USD'}).format(woData.price)) + '</td>' +
                '<td><div style="display: grid; margin: auto;"><button id="btn_pickup_'+woData._id+'" onclick="pickupWorkOrder(this)" class="btn" style="margin: auto;">Pickup</button></div></td>' +
            '</tr>' + 
            '';
            break;
        case 'In Progress':
        case 'Awaiting Part':
        rowString =
            '<tr id="tr_'+woData._id+'" class="align-middle" onclick="displayWorkOrder(this)">' + 
                '<td><div style="display: grid; grid-template-columns: 80% auto;">' + formatDateString(woData.dt_recieved) + generateDateBox(woData) + '</div></td>' +
                '<td>' + woData.fname + ' ' + woData.lname + '</td>' + 
                '<td>' + woData.model + ' (' + woData.computer_type + ') </td>' +
                '<td>' + (woData.starting_tech.length <= 0 ? 'N/A' : woData.starting_tech) + '</td>' +
                '<td><div style="display: grid; margin: auto;"><button id="btn_edit_'+woData._id+'" onclick="editWorkOrder(this)" class="btn" style="margin: auto;">Edit</button><button id="btn_complete_'+woData._id+'" onclick="completeWorkOrder(this)" class="btn" style="margin: auto;">Complete</button></div></td>' +
            '</tr>' + 
            '';
            break;
        case 'Dropped Off': 
            rowString =
            '<tr id="tr_'+woData._id+'" class="align-middle" onclick="displayWorkOrder(this)">' + 
                '<td><div style="display: grid; grid-template-columns: 80% auto;">' + formatDateString(woData.dt_recieved) + generateDateBox(woData) + '</div></td>' +
                '<td>' + woData.fname + ' ' + woData.lname + '</td>' + 
                '<td>' + woData.model + ' (' + woData.computer_type + ') </td>' +
                '<td><div style="display: grid; margin: auto;"><button id="btn_claim_'+woData._id+'" onclick="claimWorkOrder(this)" class="btn" style="margin: auto;">Claim</button></div></td>' +
            '</tr>' + 
            '';
            break;
    }
    return rowString
}

function editWorkOrder(btn) {
    let id = btn.id.replace('btn_edit_', '');
    //alert('Edit ID found: ' + id);

    window.location.replace('work-orders-edit?id=' + id);

    //stops row click from happening
    event.stopPropagation();
}

function displayWorkOrder(row_id) {
    let woId = row_id.id.replace('tr_', '');
    //alert('Row with ID ' + woId);
    let workOrderForDisplay;
    workOrders.forEach(item => {
        if (item._id == woId) {
            workOrderForDisplay = item;
        }
    })

    let modalString = getModalString(workOrderForDisplay);
    document.querySelector('#modal-wo-viewer').innerHTML = modalString;
    new bootstrap.Modal(document.querySelector('#modal-wo-viewer')).toggle();

}

function getModalString(wo) {
     return '' +
     '<div class="modal-dialog modal-dialog-centered modal-xl modal-dialog-scrollable">' +
        '<div class="modal-content">' +
            '<div class="modal-header">' + 
                '<h5 class="modal-title">Work Order</h5>' + 
                '<button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>' +                
            '</div>' + 
            '<div class="modal-body">' +
                getModalBodyString(wo) + 
            '</div>' + 
            '<div class="modal-footer">' + 
                getModalFooterString(wo) + 
            '</div>' + 
        '</div>' + 
    '</div>';
}

function getModalBodyString(wo) {
    let bodyString;
    switch(wo.status) {
        case 'Dropped Off':
            bodyString = 
            '<div>' +
                '<p><b>Name: </b>' + wo.fname + ' ' + wo.lname + '</p>' +
                '<p><b>Computer: </b>' + wo.model + ' (' + wo.computer_type + ')</p>' +
                '<p><b>Issue: </b>' + wo.issue_category + ' - ' + wo.issue_description + '</p>' +
                '<p><b>Cashier: </b>' + wo.cashier + '</p>' +
                '<hr>' + 
                '<p><b>Bought From Us: </b>' + (wo.isPurchasedFromUs ? 'Yes' : 'No') + '</p>' +
                '<p><b>Under Warranty: </b>' + (wo.isUnderWarranty ? 'Yes' : 'No') + '</p>' +
                '<p><b>Other Items: </b>' + (wo.isWithOtherItems ? 'Yes - ' + wo.other_items : 'No') + '</p>' +
            '</div>';
            break;
        case 'In Progress':
        case 'Awaiting Part':
            bodyString = 
            '<div>' +
                '<p><b>Name: </b>' + wo.fname + ' ' + wo.lname + '</p>' +
                '<p><b>Computer: </b>' + wo.model + ' (' + wo.computer_type + ')</p>' +
                '<p><b>Issue: </b>' + wo.issue_category + ' - ' + wo.issue_description + '</p>' +
                '<p><b>Bought From Us: </b>' + (wo.isPurchasedFromUs ? 'Yes' : 'No') + '</p>' +
                '<p><b>Under Warranty: </b>' + (wo.isUnderWarranty ? 'Yes' : 'No') + '</p>' +
                '<p><b>Other Items: </b>' + (wo.isWithOtherItems ? 'Yes - ' + wo.other_items : 'No') + '</p>' +
                '<p><b>Cashier: </b>' + wo.cashier + '</p>' +
                '<hr>' + 
                '<p><b>Tech: </b>' + wo.starting_tech + '</p>' +
                '<p><b>Last Update: </b>' + formatDateString(wo.dt_last_updated) + '</p>' +
                '<p><b>Needs Parts: </b>' + (wo.status == 'Awaiting Part' ? 'Yes' : 'No') + '</p>' +
                '<hr>' + 
                '<p><b>Notes: </b></p>' +
                '<p>'+wo.notes+'</p>' +
            '</div>';
            break;
        case 'Completed':
            bodyString = 
            '<div>' +
                '<p><b>Name: </b>' + wo.fname + ' ' + wo.lname + '</p>' +
                '<p><b>Computer: </b>' + wo.model + ' (' + wo.computer_type + ')</p>' +
                '<p><b>Issue: </b>' + wo.issue_category + ' - ' + wo.issue_description + '</p>' +
                '<p><b>Bought From Us: </b>' + (wo.isPurchasedFromUs ? 'Yes' : 'No') + '</p>' +
                '<p><b>Under Warranty: </b>' + (wo.isUnderWarranty ? 'Yes' : 'No') + '</p>' +
                '<p><b>Other Items: </b>' + (wo.isWithOtherItems ? 'Yes - ' + wo.other_items : 'No') + '</p>' +
                '<hr>' + 
                (wo.starting_tech == wo.finishing_tech ? '<p><b>Tech: </b>' + wo.starting_tech + '</p>' : '<p><b>Techs: </b>' + wo.starting_tech + ', ' + wo.finishing_tech + '</p>') + 
                '<p><b>Date of Completion: </b>' + formatDateString(wo.dt_completed) + '</p>' +
                '<p><b>Price: </b>' + (wo.price == null || wo.price <= 0 ? '$0.00': Intl.NumberFormat('en-US', {style: 'currency', currency: 'USD'}).format(wo.price)) + '</p>' +
                '<hr>' + 
                '<p><b>Notes: </b></p>' +
                '<p>'+wo.notes+'</p>' +
            '</div>';
            break;
    }
    return bodyString;
}

function getModalFooterString(wo) {

}