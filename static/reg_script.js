document.getElementById("reg").disabled = true;
//document.getElementById("debugtext").innerHTML = document.form1.benefactor.checked
//if(document.form1.level.value != "family") {
try {
    document.form2.style.display = "none";
}
catch(err) {}


function checkValidation (reg_type) {
  document.getElementById('debugtext').innerHTML = reg_type
  let v = true
  let l = ['first_name', 'last_name', 'street', 'city', 'state']
  if (reg_type == 'joad') {
    l = ['first_name', 'last_name']
  }

  //    alert("DOB = " + document.form1.dob.value +"\n level " + document.form1.level.value)
  for (let i = 0; i < l.length; i++) {
    if (reg_check(l[i]) == false) {
      v = false
    }
  }

  if (ValidateEmail(document.form1.email) == false) {
    v = false
  }
  if (reg_type != 'joad') {
    //        if(allnumeric(document.form1.zip) == false) {
    //            v = false;
    //        }
    if (phone_check(document.form1.phone) == false) {
      v = false
    }
    if (zip_check(document.form1.zip) == false) {
      v = false
    }
    if (select_check(document.form1.level) == false) {
      v = false
    }
  }

  if (v) {
    document.getElementById('reg').disabled = false
  } else {
    document.form1.terms.checked = false
  }
  return v
}

function reg_check (input) {
  const i = document.getElementById(input)
  if (i.value == '') {
    i.style = 'border: 3px solid Tomato;'
  } else {
    i.style = 'border: 3px solid Green;'
  }
}

function phone_check (inputText) {
//    var phoneno = /^\d{10}$/;
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

function select_check (in_select) {
  if (in_select.value === 'level') {
    in_select.style = 'border: 3px solid Tomato;'
    return false
  } else if (in_select.value === 'joad'{
    var d = new Date(document.getElementById('dob'))
    var td = new Date()
    td.setFullYear(td.getFullYear()-21)
    if (d > td) {
        in_select.style = 'border: 3px solid Tomato;'
        return false
    }
  } else {
    // TODO add joad reg checkbox to register for a joad session and show or enable here.
    in_select.style = 'border: 3px solid Green;'
    return true
  }
}

function ValidateEmail (inputText) {
  var mailformat = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/
  if (inputText.value.match(mailformat)) {
    inputText.style = 'border: 3px solid Green;'
    return true
  } else {
    //        alert("You have entered an invalid email address!");
    inputText.style = 'border: 3px solid Tomato;'
    document.form1.email.focus()
    return false
  }
}
function zip_check (in_zip) {
  if (/^\d{5}(-\d{4})?$/.test(in_zip.value)) {
    in_zip.style = 'border: 3px solid Green;'
  } else {
    in_zip.style = 'border: 3px solid Tomato;'
  }
}

$.get('/reg_values', function (data) {
  if (data != null) {
    const dob = new Date(data.dob)
    let i = 0
    console.log(typeof 'dob')
    //            document.getElementById("debugtext").innerHTML = dob.toISOString().substring(0,10);
    const l = ['first_name', 'last_name', 'street', 'city', 'state', 'zip', 'email', 'phone', 'dob', 'level', 'benefactor']
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
