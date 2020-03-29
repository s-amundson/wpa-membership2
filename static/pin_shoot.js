"use strict";
try {
    document.getElementById('submit').disabled = true;
} catch (err) {}

function all_numeric(input_txt) {
    var numbers = /^[0-9]+$/;
    if(input_txt.value.match(numbers)) {
        input_txt.style = 'border: 3px solid Green;';
        return true;
    }
    else {
        alert('Please input numeric characters only');
        input_txt.style = 'border: 3px solid Tomato;';
        return false;
    }
}

function checkValidation() {
    var v = true;
    var l = ['first_name', 'last_name', 'shoot_date'];

    for (var i = 0; i < l.length; i++) {
        if (reg_check(l[i]) == false) {
            v = false;
        }
    }

    l = ['category', 'bow', 'target', 'distance', 'prev_stars'];
    for (var i = 0; i < l.length; i++) {
        if (select_check(document.getElementById(l[i])) == false) {
            v = false;
        }
    }

    l = ['score'];
    for (var i = 0; i < l.length; i++) {
        if (all_numeric(document.getElementById(l[i])) == false) {
            v = false;
        }
    }

    if (v) {
        document.getElementById('submit').disabled = false;
    } else {
        document.getElementById('submit').disabled = true;
    }
    return v
}


function membership_number (input_txt) {
    if (input_txt.value == '') {
        input_txt.style = 'border: 1px solid Black;';
    } else {
        all_numeric(input_txt);
    }
}
function pin_select_check (in_select) {
    if (in_select.value === 'invalid') {
        in_select.style = 'border: 3px solid Tomato;'
        return false
    } else {
        in_select.style = 'border: 3px solid Green;'
        return true
    }
}

