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