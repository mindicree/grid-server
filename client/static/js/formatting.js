function formatDateString(dateString) {
    date = new Date(dateString);
    dateFormat = {
        weekday: 'short',
        day: 'numeric',
        month: 'short',
        year: 'numeric',
        hour: 'numeric',
        minute: 'numeric'
    }
    return date.toLocaleDateString('en-UK', dateFormat);
}

//from stackoverflow and edited for my purposes
//https://stackoverflow.com/questions/8358084/regular-expression-to-reformat-a-us-phone-number-in-javascript
function formatPhoneNumberToDigits(phoneNumberString) {
    var cleaned = phoneNumberString.replace(/\D/g, '');
    if (cleaned.length == 10) {
        return cleaned;
    }
    return null;
}
function formatPhoneNumberToView(phoneNumberString) {
    var cleaned = ('' + phoneNumberString).replace(/\D/g, '');
    var match = cleaned.match(/^(\d{3})(\d{3})(\d{4})$/);
    if (match) {
        return '(' + match[1] + ') ' + match[2] + '-' + match[3];
    }
    return null;
}
///////////////////////////////////////////////////////////////////////////////////////////////
function formatPriceToPlainNumber(num) {
    return new Number(num.replace(',', '').replace('$', ''))
}

function formatPriceToView(num) {
    return `$${num.toFixed(2)}`
}