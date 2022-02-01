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