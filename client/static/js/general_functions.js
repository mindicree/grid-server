function getBooleanValue(x) {
    switch(x.toLowerCase()) {
        case 'true':
        case 'TRUE':
        case 'True':
        case 1:
            return true;
            break;
        case 'false':
        case 'FALSE':
        case 'False':
        case 0:
            return false;
            break;
        default:
            return new Error('Something went wrong');
    }
}

// TODO refactor all instances to use Date rather than workOrderData
function generateDateBox (woData) {
    let now = new Date();
    let takeIn = new Date(woData.dt_recieved);
    let deltaTimeMilliseconds = now - takeIn; //date subtraction returns milliseconds
    let deltaTimeHours = deltaTimeMilliseconds / 1000 / 3600;
    //console.log('Name: ' + woData.fname + ' ' + woData.lname + '\nNow: ' + now + '\nDT_Recieved: ' + takeIn + '\ndeltaTimeMilliseconds: ' + deltaTimeMilliseconds + '\ndeltaTimeHours: ' + deltaTimeHours + '\n')
    let colorBoxString, colorRed, colorGreen;

    if (deltaTimeHours <= 36) {
        //7.0833333 RGB per hour up to 255 at 36 hours
        colorRed = (deltaTimeHours * 7.0833333);
        colorGreen = 255; 
        colorBoxString = 
        '<div class="date_color_box" style="background-color: rgb('+colorRed+', 255, 0);">' + 
        '</div>';
    } else if (deltaTimeHours <= 72) {
        //7.0833333per hour up to 255 at 36 hours
        colorRed = 255;
        colorGreen = 255 - ((deltaTimeHours - 36) * 7.0833333); 
        colorBoxString = 
        '<div class="date_color_box" style="background-color: rgb(255, '+colorGreen+', 0);">' + 
        '</div>';
    } else {
        colorBoxString = 
        '<div class="date_color_box" style="background-color: rgb(255, 0, 0);">' + 
        '</div>';
    }

    return colorBoxString;

}

// function to return the current set printing location
function getCurrentPrintLocation() {
    current_print_location = window.localStorage.getItem('print_location')
    if (current_print_location == null) {
        return "GOC"
    } else {
        return current_print_location
    }
}

// funtion to return number value based on provided HTML input id
function getNumberFromInput(input_id) {
    let amount_to_print = Number(document.querySelector(`#${input_id}`).value)
    if (amount_to_print == NaN || amount_to_print == 0) {
        amount_to_print = 1
    }
    return amount_to_print
}

// function to get the value of an input by id
function getValueOf(input_id) {
    return document.querySelector(`#${input_id}`).value
}

// function to check if variable is JSON object
// borrowed from https://www.cloudhadoop.com/javascript-check-json-found/
function isJSONObject(obj) {
    try {
        JSON.parse(obj)
        return true    
    } catch (e) {
        return false
    }
}

//function to format date for data
function formatDateString(dateString) {
    date = new Date(dateString);
    dateFormat = {
        weekday: 'short',
        day: 'numeric',
        month: 'short',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
    }
    return date.toLocaleDateString('en-UK', dateFormat);
}

//function to format date for data
function formatDate(dateString) {
    date = new Date(dateString);
    dateFormat = {
        weekday: 'short',
        day: 'numeric',
        month: 'short',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
    }
    return date.toLocaleDateString('en-UK', dateFormat);
}