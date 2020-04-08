"use strict";
try {
    document.getElementById("reg").disabled = true;
} catch (err) {}


function checkValidation(reg_type) {
    var v = true;
    var l = ['first_name', 'last_name'];

    //    alert("DOB = " + document.form1.dob.value +"\n level " + document.form1.level.value)
    for (var i = 0; i < l.length; i++) {
        if (reg_check(l[i]) == false) {
            v = false;
        }
    }

    if (ValidateEmail(document.form1.email) == false) {
        v = false;
    }

//    if (phone_check(document.form1.phone) == false) {
//        v = false;
//    }
//    if (zip_check(document.form1.zip) == false) {
//        v = false;
//    }
//    if (select_check(document.form1.level) == false) {
//        v = false;
//    }

    if (v) {
        document.getElementById('reg').disabled = false
    } else {
        document.form1.terms.checked = false
    }
    return v
}

