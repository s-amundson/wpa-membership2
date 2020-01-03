function lookup_price(val) {
    if(val != "") {
        $.get('/price?symbol=' + val, function(data) {
            document.getElementById("price").innerHTML = "Price: " + data;
        });
    }
}

function username_function(val) {
    // alert("The input value has changed. The new value is: " + val);
    if(val == "") {
        alert("username cannot be blank.");
        document.getElementById("username").style = "border:2px solid Tomato;";
        document.getElementById("reg").disabled = true;
    }
    else {
        // document.getElementById("username").style = "border:2px solid Green;";
        $.get('/check?username=' + val, function(data) {
            if(data){
                document.getElementById("username").style = "border:2px solid Green;";
                document.getElementById("usernameDiv").style.visibility = "hidden";
            }
            else{
                document.getElementById("username").style = "border: 2px solid Tomato;";
                document.getElementById("usernameDiv").style.visibility = "visible";
                // alert("This username has been taken. Please select another.")
            }
        });
    }
}
function reg_check(input) {
    let i = document.getElementById(input);
    if(i.value == "") {
        i.style = "border: 2px solid Tomato;";
    }
    else {
        i.style = "border: 2px solid Green;";
    }
}
function reg_pass() {
    let p1 = document.getElementById("password");
    let p2 = document.getElementById("confirmation");

    if(p1.value != "" && p2.value != "") {
        if(p1.value != p2.value) {
            p1.style = "border: 2px solid Tomato;";
            p2.style = "border: 2px solid Tomato;";
            document.getElementById("passDiv").style.visibility = "visible";
            document.getElementById("reg").disabled = true;

        }
        else {
            p1.style = "border: 2px solid Green;";
            p2.style = "border: 2px solid Green;";
            document.getElementById("passDiv").style.visibility = "hidden";
            document.getElementById("reg").disabled = false;

        }
    }
}
