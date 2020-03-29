"use strict";
try {
    document.getElementById("reg").disabled = true;
} catch (err) {}
//document.getElementById("debugtext").innerHTML = document.form1.benefactor.checked
//if(document.form1.level.value != "family") {
try {
    document.form2.style.display = "none";
} catch (err) {}

try {
    document.getElementById("joad_div").style.display = 'block';
} catch (err) {}

var costs = {}
$.get('/cost_values', function (data) {
    costs = data;
    });

function calculate_cost() {
    var price = 0;

    if(document.getElementById("benefactor").checked) {
        price = parseInt(costs.benefactor)
    } else {
        price = parseInt(costs[document.getElementById("level").value + "_membership"])
    }
    console.log("joad select = " + document.getElementById("joad").value)
    if(document.getElementById("joad").value != "None") {
        price += parseInt(costs["joad_session"])
    }
    document.getElementById("cost").innerHTML = "Total Cost: " + price
}
function checkValidation(reg_type) {
    document.getElementById('debugtext').innerHTML = reg_type;
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
    if (zip_check(document.form1.zip) == false) {
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
    console.log("enable value" + enable_value)
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
//    for (let el of document.querySelectorAll('.joad')) el.style.visibility = vis;
}
function level_enable (enable_value, level){
    var op = document.getElementById("level").getElementsByTagName("option");

    for (var i = 0; i < op.length; i++) {
        var op_level =  op[i].value.toLowerCase()
        // lowercase comparison for case-insensitivity
        if ( op_level == level) {
            op[i].disabled = !enable_value;
        }
    }
}
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
    console.log('select_check')
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

//function ValidateEmail (inputText) {
//  var mailformat = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/
//  if (inputText.value.match(mailformat)) {
//    inputText.style = 'border: 3px solid Green;'
//    return true
//  } else {
//    //        alert("You have entered an invalid email address!");
//    inputText.style = 'border: 3px solid Tomato;'
//    document.form1.email.focus();
//    return false
//  }
//}
function zip_check (in_zip) {
  if (/^\d{5}(-\d{4})?$/.test(in_zip.value)) {
    in_zip.style = 'border: 3px solid Green;'
  } else {
    in_zip.style = 'border: 3px solid Tomato;'
  }
}


joad_enable(false);
level_enable(false, "senior");

$.get('/reg_values', function (data) {
  if (data != null) {
    var dob = new Date(data.dob)
    var i = 0
    console.log(typeof 'dob')
    //            document.getElementById("debugtext").innerHTML = dob.toISOString().substring(0,10);
    var l = ['first_name', 'last_name', 'street', 'city', 'state', 'zip', 'email', 'phone', 'dob', 'level', 'benefactor']
    for (i = 0; i < l.length; i += 1) {
      console.log(l[i])
      console.log(typeof data[l[i]])
//      if (l[i] == 'benefactor') {
//        //                        document.getElementById("debugtext").innerHTML = document.form1.benefactor.value
//        document.getElementById('benefactor').checked = document.form1.benefactor.value
//      }
      if (l[i] == 'dob') {
        console.log("in dob");
        // document.getElementById('debugtext').innerHTML = dob.toISOString().substring(0, 10);
        // document.form1.dob.value = dob.toISOString().substring(0, 10)
        document.getElementById("dob_div").style.display = 'none';
//        document.getElementById("dob").style.display = 'none';
        document.getElementById("dob").value = dob.toISOString().substring(0,10);
        console.log(document.getElementById("dob").value);
      }
      if (l[i] == 'level') {
        if (data[l[i]] == 'family') {
          document.getElementById('terms').checked = true
          $("select[name='level']").find('option').remove().end().append(
            "<option value='family'>Family</option>")
          //                                document.getElementById("level").remove().append(
          //                                    "<option value='family'>Family</option>");
          document.form2.style.display = 'initial'
        } else {
          document.form2.style.display = 'none'
        }
      }

      // TODO add for DOB
      document.getElementById(l[i]).value = data[l[i]]
    }
  }
})
