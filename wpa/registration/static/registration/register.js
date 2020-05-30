"use strict";

var app1
var costs
var form_count = 0
var max_forms
var member_forms = []
//var MemberFormComponentId = 0

function add_member() {
    member_forms.push(new MemberForm(form_count))
    disable_delete()

    $("#id_delete_member_button-" + form_count).click(function (ev) {
    ev.stopPropagation()
    console.log(form_count)
    delete_member($(this).attr("form_id"))
    })
    form_count++
    set_levels()
    $("#id_btn_add_row").prop('disabled', true)

    update_listener()
    $("#id_member_set-TOTAL_FORMS").val(form_count.toString())
    calculate_costs()
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
            if(member_forms[i].joad_input.val() != "") {
                costs["family_total"] = costs["family_total"] + costs["joad_session"]
            }
        }
        $("#cost").html("Total Cost: " + costs["family_total"])
    }

}

function delete_member(this_form) {
    console.log(this_form)
    console.log(member_forms.length)
    $("#form-div-" + this_form).remove()

    member_forms.splice(this_form, 1)
    console.log(member_forms.length)
    for(var i = this_form; i < member_forms.length; i++) {
        console.log(this_form)
        console.log(i)
        member_forms[i].decrement_form()
    }
    disable_delete()
    var valid = true
    for(i = 0; i < member_forms.length; i++) {
        if (!member_forms[i].inputs_valid()){
            valid = false
        }
    }
    if(valid){
        $("#id_btn_add_row").prop('disabled', false)
    }
    form_count--
    set_levels()
    $("#id_member_set-TOTAL_FORMS").val(form_count.toString())

}

function disable_delete() {
    if(form_count == 0){
        $("#id_delete_member_button-0").prop('disabled', true)
    } else {
        $("#id_delete_member_button-0").prop('disabled', false)
    }
}

function set_levels() {
    console.log("set Level " + form_count)
    if(form_count == 1){
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

    $(".member-required").blur(function () {
        let this_form = $(this).attr("form_id")

        let valid = member_forms[parseInt($(this).attr("form_id"))].inputs_valid()
        if(valid) {
            $("#id_btn_add_row").prop('disabled', false)
        } else {
            $("#id_btn_add_row").prop('disabled', true)
        }
        return set_valid($(this), $(this).val() != '')

    })
}

$(document).ready(function() {
    console.log("document ready")
    if ($("#message").attr('message_text') != "") {
        alert($("#message").attr('message_text'))
    }
    costs = JSON.parse($("#costs").attr("cost-values"))
    max_forms = $("#id_member_set-MAX_NUM_FORMS").val()
    form_count = $("#id_member_set-INITIAL_FORMS").val()


    if(form_count == 0) {
        add_member()
    }

    $("#id_btn_add_row").prop('disabled', true)

    $("#id_btn_add_row").click(function () {
        add_member()
    })

    $("#id_level").change(function () {
        calculate_costs()
    })

    $("#id_benefactor").click(function () {
        calculate_costs()
    })

})

class MemberForm {
    constructor(index){
        // adds a member to the form.
        $("#before_me").before($("#member-form-template").html().replace(/__prefix__/g, form_count))

        this.first_name_input = $("#id_member_set-" + index + "-first_name")
        this.last_name_input = $("#id_member_set-" + index + "-last_name")
        this.dob_input = $("#id_member_set-" + index + "-dob")
        this.joad_input = $("#id_member_set-" + index + "-joad")

        this.div = $("#form-div-" + form_count)
        this.div_joad = $("#form-div-" + form_count + "-joad")
        this.div_joad.hide()
        this.form_index = index
        this.level_joad = false
        this.level_senior = false
        $("#id_invalid_dob-" + index).hide()

        this.first_name_input.attr('required', '');
        this.last_name_input.attr('required', '');
        this.dob_input.attr('required', '');

        $(function () {
            $("#id_member_set-" + index + "-dob").datepicker(
            {
              format:'yyyy-mm-dd',
            })
        })
        this.dob_input.blur(function() {
            member_forms[index].dob_check()
            set_levels()
        })
        this.joad_input.blur(function() {
            calculate_costs()
        })

    }

    decrement_form() {
        this.form_index--
        console.log(this.form_index)
        this.div.attr("id", "form-div-" + this.form_index)
        this.div_joad.attr("id", "form-div-" + this.form_index + "-joad")
        this.first_name_input.attr("id", "id_member_set-" + this.form_index + "-first_name")
        this.last_name_input.attr("id", "id_member_set-" + this.form_index + "-last_name")
        this.dob_input.attr("id", "id_member_set-" + this.form_index + "-dob")
    }

    dob_check() {
        console.log('dob blur')
        var bd = Date.parse(this.dob_input.val())

        if(isNaN(bd)) {
            $("#id_invalid_dob-" + this.form_index).show()
        } else {

            var joad_date = new Date();
            var senior_date = new Date().setFullYear(joad_date.getFullYear() - 55)
            joad_date.setFullYear(joad_date.getFullYear() - 21);

            if(bd > joad_date && bd < new Date()) {
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