"use strict";
$(document).ready(function(){
    $(".not_empty").blur(function() {
        return set_valid($(this), $(this).val() != '')
    });

});

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
function set_valid (input, valid) {
    if (valid) {
        $(input).attr("style", 'border: 3px solid Green;');
        return true;
    } else {
        $(input).attr("style", 'border: 3px solid Tomato;');
        return false;
    }
}

