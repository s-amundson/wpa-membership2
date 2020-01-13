function allnumeric(inputtxt) {
    var numbers = /^[0-9]+$/;
    if(inputtxt.value.match(numbers)) {
//        document.form1.text1.focus();
        return true;
    }
    else {
        alert('Please input numeric characters only');
//        document.form1.text1.focus();
        return false;
    }
}

function checkValidation() {
    let v = true;
    let l = ["first_name", "last_name", "street", "city", "state"]
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
    if(phoneNumber(document.form1.phone) == false){
        v = false;
    }
    return v

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
function phoneNumber(inputText)
{
    var phoneno = /^\d{10}$/;
    if((inputText.value.match(phoneno)) {
        return true;
    }
    else {
        alert("Please enter a valid phone number");
        return false;
    }
}
