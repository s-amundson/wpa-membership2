document.getElementById("reg").disabled = true;

function allnumeric(inputtxt) {
    var numbers = /^[0-9]+$/;
    if(inputtxt.value.match(numbers)) {
        return true;
    }
    else {
//                alert('Please input numeric characters only');
        return false;
    }
}

function checkValidation() {
    let v = true;
    let l = ["first_name", "last_name", "street", "city", "state"];
//    alert("DOB = " + document.form1.dob.value +"\n level " + document.form1.level.value)
    for (var i = 0; i < l.length; i++) {
        if(reg_check(l[i]) == false) {
            v = false;
        }
    }
    if(allnumeric(document.form1.zip) == false) {
        v = false;
    }
    if(ValidateEmail(document.form1.email) == false) {
        v = false;
    }
    if(phone_check(document.form1.phone) == false){
        v = false;
    }
    if(zip_check(document.form1.zip) == false) {
        v = false;
    }
    if(select_check(document.form1.level) == false){
        v = false;
    }
    if(v){
        document.getElementById("reg").disabled = false;
    }
    else{
        document.form1.terms.value = 0;
    }
    return v;
}

function reg_check(input) {
    let i = document.getElementById(input);
    if(i.value == "") {
        i.style = "border: 3px solid Tomato;";
    }
    else {
        i.style = "border: 3px solid Green;";
    }
}

function phone_check(inputText){
//    var phoneno = /^\d{10}$/;
    var phoneno = /^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$/im;
    if(inputText.value.match(phoneno)) {
        inputText.style = "border: 3px solid Green;";
        return true;
    }
    else {
//        alert("Please enter a valid phone number");
        inputText.style = "border: 3px solid Tomato;";
        return false;
    }
}

function select_check(in_select){
    if(in_select.value === "level") {
        in_select.style = "border: 3px solid Tomato;";
        return false;
    }
    else {
        in_select.style = "border: 3px solid Green;";
        return true;
    }
}

function ValidateEmail(inputText) {
    var mailformat = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
    if(inputText.value.match(mailformat)) {
        inputText.style = "border: 3px solid Green;";
        return true;
    }
    else {
//        alert("You have entered an invalid email address!");
        inputText.style = "border: 3px solid Tomato;";
        document.form1.email.focus();
        return false;
    }
}
function zip_check(in_zip) {
    if (/^\d{5}(-\d{4})?$/.test(in_zip.value)) {
        in_zip.style = "border: 3px solid Green;";
    }
    else {
        in_zip.style = "border: 3px solid Tomato;";
    }
}

$.get('/reg_values', function(data) {
            if(data != null){
                let l = ["first_name", "last_name", "street", "city", "state", "zip", "email", "phone", "dob", "level", "benefactor"];
                    for (var i = 0; i < l.length; i++) {
                        document.getElementById(l[i]).value = data[l[i]];
//                        if(l[i] == "level" && data[l[i]] == "family"){
//                            document.getElementById(l[i]).disabled = true;
//                        }
                    }
            }
        });