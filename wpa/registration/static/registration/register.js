"use strict";

var app1
var costs
var form_index = 0
var max_forms
var member_forms = []
//var MemberFormComponentId = 0

function add_member(is_new) {
    console.log("add_member " + is_new)
    if(member_forms.length >= max_forms) {
        alert("Max forms reached")
    }
    member_forms.push(new MemberForm(form_index, is_new))
    disable_delete()

//    $("#id_delete_member_button-" + form_index).click(function (ev) {
//        ev.stopPropagation()
//        console.log(form_index)
//        delete_member($(this).attr("form_id"))
//    })

    form_index++
    $("#id_member_set-TOTAL_FORMS").val(form_index.toString())

    set_levels()
    $("#id_btn_add_row").prop('disabled', is_new)

    update_listener()

    calculate_costs()
}
function dob_check(obj) {
    console.log("main dob check" + obj)
    member_forms[obj.attr('form_id')].dob_check()

}
function calculate_costs() {
    if($("#id_level").val() == "") {
        $("#cost").html("Total Cost: Error")
    } else {
        if($("#id_benefactor").is(':checked')) {
            costs["family_total"] = costs['benefactor']
        } else {
            costs["family_total"] = costs[$("#id_level").val() + "_membership"]
        }

        for(var i = 0; i < member_forms.length; i++) {
            if(!(member_forms[i].joad_input.val() == "" || member_forms[i].joad_input.val() == null))  {
                costs["family_total"] = costs["family_total"] + costs["joad_session"]
            }
        }
        $("#cost").html("Total Cost: " + costs["family_total"])
    }

}

//function delete_member(this_form) {
//    console.log(this_form)
//    console.log(member_forms.length)
//    $("#form-div-" + this_form).remove()
//
//    member_forms.splice(this_form, 1)
//    console.log(member_forms.length)
//    for(var i = this_form; i < member_forms.length; i++) {
//        console.log(this_form)
//        console.log(i)
////        member_forms[i].decrement_form()
//    }
//    disable_delete()
//
//    if(is_members_valid()){
//        $("#id_btn_add_row").prop('disabled', false)
//    }
////    form_count--
//    set_levels()
//    $("#id_member_set-TOTAL_FORMS").val(member_forms.length.toString())
//
//}

function disable_delete() {
    $("#id_member_set-0-DELETE").prop('disabled', (member_forms.length == 1))
//    if(member_forms.length == 1){
//        $("#id_delete_member_button-0").prop('disabled', true)
//    } else {
//        $("#id_delete_member_button-0").prop('disabled', false)
//    }
}
function is_members_valid() {
    var valid = true
    for(var i = 0; i < member_forms.length; i++) {
        if (!member_forms[i].inputs_valid()){
            valid = false
        }
    }
    return valid
}
function set_levels() {
    console.log("set Level " + form_index)
    var mem_count = 0
    for(var i = 0; i < member_forms.length; i++) {
//        member_forms[i].dob_check()
        if(!$("#id_member_set-" + i + "-DELETE").is(':checked')) {
            mem_count++
        }
    }
    console.log(mem_count)
    if(mem_count == 1){
        if ($("#id_level").val() == "family") {
            $("#id_level").val("")
        }

        $("#id_level option[value='standard']").prop('disabled', false).siblings().prop('disabled', 'disabled')
        if(member_forms[0].dob_input.val != ""){
            if(member_forms[0].level_joad) {
                console.log(member_forms[0].level_joad)
                $("#id_level option[value='joad']").prop('disabled', false)
            }else if(member_forms[0].level_senior) {
                $("#id_level option[value='senior']").prop('disabled', false)
            }
        }
    } else {
        // set level to family
        $("#id_level option[value='family']").prop('disabled', false).siblings().prop('disabled', 'disabled')
        $("#id_level").val("family")
    }
}
function update_listener() {
    console.log('update_listner')
    $(".member-required").blur(function () {
        if($(this).hasClass('dob')) {
            console.log('member required dob')
            return
        }
        let this_form = $(this).attr("form_id")

        if(is_members_valid() && member_forms.length < max_forms) {
            $("#id_btn_add_row").prop('disabled', false)
        } else {
            $("#id_btn_add_row").prop('disabled', true)
        }
        return set_valid($(this), $(this).val() != '')
    })

    $(".delete_check").click(function () {
        console.log('delete check click')
        let this_form = $(this).attr("form_id")
        console.log(this_form)
        if($(this).is(':checked')) {
            $("#id_member_set-" + this_form + "-first_name").prop('disabled', true)
            $("#id_member_set-" + this_form + "-last_name").prop('disabled', true)
            $("#id_member_set-" + this_form + "-dob").prop('disabled', true)
            $("#id_member_set-" + this_form + "-joad").prop('disabled', true)
        } else {
            $("#id_member_set-" + this_form + "-first_name").prop('disabled', false)
            $("#id_member_set-" + this_form + "-last_name").prop('disabled', false)
            $("#id_member_set-" + this_form + "-dob").prop('disabled', false)
            $("#id_member_set-" + this_form + "-joad").prop('disabled', false)
        }
        set_levels()
    })
}

$(document).ready(function() {
    console.log("document ready")
    if ($("#message").attr('message_text') != "") {
        alert($("#message").attr('message_text'))
    }
    costs = JSON.parse($("#costs").attr("cost-values"))
    max_forms = $("#id_member_set-MAX_NUM_FORMS").val()
    var forms = $("#id_member_set-INITIAL_FORMS").val()


    if(forms == 0) {
        add_member(true)
    } else {

        for(var i=0; i < forms; i++) {
            $("#id_member_set-" + i + "-first_name").attr('form_id', i)
            $("#id_member_set-" + i + "-last_name").attr('form_id', i)
            $("#id_member_set-" + i + "-dob").attr('form_id', i)
            $("#id_member_set-" + i + "-DELETE").attr('form_id', i)
            add_member(false)
        }
    }

//    $("#id_btn_add_row").prop('disabled', true)


    $("#id_btn_add_row").click(function () {
        add_member(true)
    })

    $("#id_level").change(function () {
        calculate_costs()
    })

    $("#id_benefactor").click(function () {
        calculate_costs()
    })

    $("#id_submit").click(function () {
        console.log('submit form')
        var form_count = 0
        var l = member_forms.length
        var n = 0
        for(var i=0; i < l; i++) {
            n = l - (i+1)
            var c = member_forms[n].delete_input.is(':checked')
            console.log("member " + n + "checked = " + c)
            console.log("member id" + member_forms[n].member_id.val())
            if(c && member_forms[n].member_id.val() == "") {
                member_forms[n].div.remove()
                member_forms.splice(n, 1)
            } else {
                form_count++
            }
        }
        $("#id_member_set-TOTAL_FORMS").val(form_count.toString())
    })

})

class MemberForm {
    constructor(index, existing_form){
        // adds a member to the form.
        if(existing_form) {
            $("#before_me").before($("#member-form-template").html().replace(/__prefix__/g, form_index))
        }
        this.member_id = $("#id_member_set-" + form_index + "-id")
        this.first_name_input = $("#id_member_set-" + form_index + "-first_name")
        this.last_name_input = $("#id_member_set-" + form_index + "-last_name")
        this.dob_input = $("#id_member_set-" + form_index + "-dob")
        this.joad_input = $("#id_member_set-" + form_index + "-joad")
        this.delete_input = $("#id_member_set-" + form_index + "-DELETE")
        this.delete_input.attr('class', "form-control m-2 custom-control-input delete_check")
        this.delete_input.attr("form_id", form_index)

        this.div = $("#form-div-" + form_index)
        this.div_joad = $("#form-div-" + form_index + "-joad")
        this.div_joad.hide()
        this.form_index = form_index
        this.level_joad = false
        this.level_senior = false
        $("#id_invalid_dob-" + form_index).hide()

        this.first_name_input.attr('required', '')
//        this.first_name_input.attr('form_id', index)
        this.last_name_input.attr('required', '')
//        this.last_name_input.attr('form_id', index)
        this.dob_input.attr('required', '')
//        this.dob_input.attr('form_id', index)

        $(function () {
            $("#id_member_set-" + index + "-dob").datepicker(
            {
              format:'yyyy-mm-dd',
              onSelect: function(dateText) { set_levels }
            })
        })
        this.dob_input.change(function() {
            dob_check($(this))
        })
    }

//    decrement_form() {
//        this.form_index--
//        console.log(this.form_index)
//        this.div.attr("id", "form-div-" + this.form_index)
//        this.div_joad.attr("id", "form-div-" + this.form_index + "-joad")
//        this.first_name_input.attr("id", "id_member_set-" + this.form_index + "-first_name")
//        this.last_name_input.attr("id", "id_member_set-" + this.form_index + "-last_name")
//        this.dob_input.attr("id", "id_member_set-" + this.form_index + "-dob")
//    }

    dob_check() {
        console.log('dob blur')
        console.log(this.dob_input.val())
//        if(this.dob_input.val() == ''){
//            return
//        }
        var bd = Date.parse(this.dob_input.val())
        let valid = false

        if(isNaN(bd)) {
            $("#id_invalid_dob-" + this.form_index).show()
        } else {

            var joad_date_old = new Date()
            var joad_date_young = new Date().setFullYear(joad_date_old.getFullYear() - 8)
            var senior_date = new Date().setFullYear(joad_date_old.getFullYear() - 55)
            joad_date_old.setFullYear(joad_date_old.getFullYear() - 21);

            if(bd > joad_date_young){
                this.level_joad = true
            } else if(bd > joad_date_old && bd <= joad_date_young) {
                this.div_joad.show()
                this.level_joad = true
            } else {
                this.div_joad.hide()
                this.level_joad = false
            }

            if (bd < senior_date) {
                this.level_senior  = true
            } else {
                this.level_senior  = false
            }
            $("#id_invalid_dob-" + this.form_index).hide()
            valid = true
        }
        console.log(valid)
        if (valid) {
            this.dob_input.attr("style", 'border: 3px solid Green;');
            return true;
        } else {
            this.dob_input.attr("style", 'border: 3px solid Tomato;');
            return false;
        }
    }

    inputs_valid() {
        let valid = true
        if(this.first_name_input.val() === "") {
            valid = false
        }
        if(this.last_name_input.val() === "") {
            valid = false
        }
        if(this.dob_input.val() === "") {
            valid = false
        }
        return valid
    }

}