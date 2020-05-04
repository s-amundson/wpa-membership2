"use strict";


var costs = {}

function dob_check (input) {
    var i = document.getElementById(input)
    if (i.value == '') {
        i.style = 'border: 3px solid Tomato;';
    } else {
        if (input == 'dob'){
            var bd = new Date(i.value);
            var joad_date = new Date();
            var senior_date = new Date();

            joad_date.setFullYear(joad_date.getFullYear() - 21);
            senior_date.setFullYear(senior_date.getFullYear() - 55)
            console.log(senior_date);
            if (bd > joad_date && bd < new Date()) {
                console.log("Eligable for JOAD");
                joad_enable(true);
                level_enable(false, "senior");

            } else if (bd <= senior_date) {
                console.log("Senior");
                joad_enable(false);
                level_enable(true, "senior");
            } else {
                console.log("Standard and family only");
                joad_enable(false);
                level_enable(false, "senior");
            }
        }
        i.style = 'border: 3px solid Green;'
    }
}



function calculate_cost() {
    var price = 0;
    console.log(costs.family_total)
    if (costs.family_total != null){
        price = parseInt(costs.family_total);
    } else if(document.getElementById("benefactor").checked) {
        price = parseInt(costs.benefactor);
    } else {
        if(document.getElementById("level").value == "invalid") {
            price = "Invalid Membership Level";
        } else {
            price = parseInt(costs[document.getElementById("level").value + "_membership"]);
        }
    }
    console.log("joad select = " + document.getElementById("joad").value);
    if(document.getElementById("joad").value != "None") {
        price += parseInt(costs["joad_session"]);
    }
    document.getElementById("cost").innerHTML = "Total Cost: " + price;
}

function checkValidation(reg_type) {
    var v = true;
    var l = ['first_name', 'last_name', 'street', 'city', 'state'];
    if (reg_type == 'joad') {
        l = ['first_name', 'last_name'];
    }

    //    alert("DOB = " + document.form1.dob.value +"\n level " + document.form1.level.value)
    for (var i = 0; i < l.length; i++) {
        if (reg_check(l[i]) == false) {
            v = false;
        }
    }

    if (ValidateEmail(document.form1.email) == false) {
        v = false;
    }

    if (phone_check(document.form1.phone) == false) {
        v = false;
    }
    if (zip_check(document.form1.post_code) == false) {
        v = false;
    }
    if (select_check(document.form1.level) == false) {
        v = false;
    }

    if (v) {
        document.getElementById('reg').disabled = false
    } else {
        document.form1.terms.checked = false
    }
    return v
}

function joad_enable(enable_value){
    // Get all options within <select id='foo'>...</select>
    level_enable(enable_value, "joad");
    var vis = "hidden";
    if(enable_value) {
//        document.getElementById("joad_div").style.display = 'block';
        document.getElementById("joad").disabled = false
        vis = 'visible';
    } else {
//        document.getElementById("joad_div").style.display = 'none';
        document.getElementById("joad").disabled = true
    }
}

function level_enable (enable_value, level){
    if(document.getElementById("level").value == level) {
        document.getElementById("level").value = "invalid";
        calculate_cost();
    }
    var op = document.getElementById("level").getElementsByTagName("option");


    for (var i = 0; i < op.length; i++) {
        var op_level =  op[i].value.toLowerCase()
        // lowercase comparison for case-insensitivity
        if ( op_level == level) {
            op[i].disabled = !enable_value;
        }
    }
}

function phone_check (inputText) {
    var phoneno = /^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$/im
    if (inputText.value.match(phoneno)) {
        inputText.style = 'border: 3px solid Green;'
        return true
    } else {
        //        alert("Please enter a valid phone number");
        inputText.style = 'border: 3px solid Tomato;'
        return false
    }
}

function reg_level_check (in_select) {
    calculate_cost();
    if (in_select.value === 'level') {
        in_select.style = 'border: 3px solid Tomato;'
        return false
    } else if (in_select.value === 'joad'){
        var d = new Date(document.getElementById('dob'))
        var td = new Date()
        td.setFullYear(td.getFullYear()-21)
        if (d > td) {
            in_select.style = 'border: 3px solid Tomato;'
            return false
        }
    } else {

        in_select.style = 'border: 3px solid Green;'
        return true
    }
}

function zip_check (in_zip) {
  if (/^\d{5}(-\d{4})?$/.test(in_zip.value)) {
    in_zip.style = 'border: 3px solid Green;'
  } else {
    in_zip.style = 'border: 3px solid Tomato;'
  }
}

window.onload = function () {

    $.get(document.getElementById("cost").getAttribute("cost_link"), function (data) {
        costs = data;
        });
    joad_enable(false);
    level_enable(false, "senior");
    try {
        document.getElementById("reg").disabled = true;
    } catch (err) {}

    try {
        document.form2.style.display = "none";
    } catch (err) {}

    try {
        document.getElementById("joad_div").style.display = 'block';
    } catch (err) {}


    $.get('/reg_values', function (data) {
      if (data != null) {
        var dob = new Date(data.dob)
        var i = 0
        var l = ['first_name', 'last_name', 'street', 'city', 'state', 'zip', 'email', 'phone', 'dob', 'level', 'benefactor']
        for (i = 0; i < l.length; i += 1) {
          if (l[i] == 'dob') {
            console.log("in dob");
            if (data.renewal == true) {
                document.getElementById("dob_div").style.display = 'none';
            }
          }
          if (l[i] == 'level') {
            if (data[l[i]] == 'family') {

              $("select[name='level']").find('option').remove().end().append(
                "<option value='family'>Family</option>")

              document.form2.style.display = 'initial'
            } else {
              document.form2.style.display = 'none'
            }
          }

          // TODO add for DOB
          document.getElementById(l[i]).value = data[l[i]]
        }
        calculate_cost();
      }
    })
}
