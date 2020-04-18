"use strict";

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
    if (shoot_date_check == false) {
        v = false;
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
    if (ValidateEmail(document.form1.email) == false) {
        v = false;
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

function shoot_date_check (input) {
    var i = document.getElementById(input)
    if (i.value == '') {
        i.style = 'border: 3px solid Tomato;';
        return false
    } else {
        var sd = new Date(i.value);
        if (sd > new Date()){
            i.style = 'border: 3px solid Tomato;';
            alert('Shoot Date cannot be in future');
            return false
        } else {
            i.style = 'border: 3px solid Green;'
            return true
        }
    }
}