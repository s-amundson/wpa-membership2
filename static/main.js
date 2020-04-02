"use strict";
function reg_check (input) {
    var i = document.getElementById(input)
    if (i.value == '') {
        i.style = 'border: 3px solid Tomato;';
        return false;
    } else {
        i.style = 'border: 3px solid Green;';
        return true;
    }
}

function select_check (in_select) {
    console.log('select_check' + in_select.value)
    if (in_select.value === 'invalid') {
        in_select.style = 'border: 3px solid Tomato;'
        return false
    } else {
        in_select.style = 'border: 3px solid Green;'
        return true
    }
}

function ValidateEmail(inputText) {
    var mailformat = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
    if(inputText.value.match(mailformat)) {
        inputText.style = "border: 3px solid Green;";
        return true;
    }
    else {
        alert("You have entered an invalid email address!");
        inputText.style = "border: 3px solid Tomato;";
        document.form1.email.focus();
        return false;
    }
}