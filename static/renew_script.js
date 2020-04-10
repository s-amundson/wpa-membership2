
function checkValidation(form) {
    // TODO get form elemets and check
}
function renew_reg_check(input) {
    let i = document.getElementById(input);
    if(i.value == "") {
        i.style = "border: 3px solid Tomato;";
    }
    else {
        i.style = "border: 3px solid Green;";
        if(ValidateEmail(document.form1.email)) {
            document.getElementById("renew").disabled = false;
            document.getElementById("renew").focus();
        }
    }
}

function renew_ValidateEmail(inputText) {
    var mailformat = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
    if(inputText.value.match(mailformat)) {
        inputText.style = "border: 3px solid Green;";
        if(inputText.name == "email2") {
            document.getElementById("renew2").disabled = false;
            document.getElementById("renew2").focus();
        }
        if(inputText.name == "email") {
            if(document.getElementById("vcode").value != ""){
                document.getElementById("renew").disabled = false;
                document.getElementById("renew").focus();
            }
        }

        return true;
    }
    else {
//        alert("You have entered an invalid email address!");
        inputText.style = "border: 3px solid Tomato;";
        if(inputText.name == "email2") {
            document.getElementById("renew2").disabled = true;
            document.form2.email2.focus();
        }
        if(inputText.name == "email") {
            document.getElementById("renew").disabled = true;
            document.form1.email.focus();
        }

        return false;
    }
}

