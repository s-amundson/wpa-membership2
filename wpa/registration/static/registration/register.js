"use strict";

var app1
var form_count = 0
var max_forms
var member_forms = []
//var MemberFormComponentId = 0

function add_member() {
    member_forms.push(new MemberForm(form_count))
    disable_delete()
    form_count++
    $("#id_btn_add_row").prop('disabled', true)
    update_listener()
    $("#id_member_set-TOTAL_FORMS").val(form_count.toString())
}

function disable_delete() {
    if(form_count == 0){
        $("#id_member_button-0").prop('disabled', true)
    } else {
        $("#id_member_button-0").prop('disabled', false)
    }
}

function update_listener() {
    $(".dob").blur(function() {
        member_forms[parseInt($(this).attr("form_id"))].dob_check()
    })

    $(".member_button").click(function () {
        console.log(form_count)
        let this_form = $(this).attr("form_id")
        console.log(this_form)
        console.log(member_forms.length)
        $("#form-div-" + this_form).remove()
//        member_forms[this_form].delete_div()
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
        $("#id_member_set-TOTAL_FORMS").val(form_count.toString())
    })

    $(".member-required").blur(function () {
        let this_form = $(this).attr("form_id")

        let valid = member_forms[parseInt($(this).attr("form_id"))].inputs_valid()
        if(valid) {
            $("#id_btn_add_row").prop('disabled', false)
        } else {
            $("#id_btn_add_row").prop('disabled', true)
        }
    })
}

$(document).ready(function() {
    add_member()

    $("#id_btn_add_row").prop('disabled', true)

    $("#id_btn_add_row").click(function () {
        add_member()
    })
})

class MemberForm {
    constructor(index){
        // adds a member to the form.
        $("#before_me").before($("#member-form-template").html().replace(/__prefix__/g, form_count))

        this.first_name_input = $("#id_member_set-" + index + "-first_name")
        this.last_name_input = $("#id_member_set-" + index + "-last_name")
        this.dob_input = $("#id_member_set-" + index + "-last_name")
        this.div = $("#form-div-" + form_count)
        this.div_joad = $("#form-div-" + form_count + "-joad")
        this.div_joad.hide()
        this.form_index = index
    }

    decrement_form() {
        this.form_index--
        console.log(this.form_index)
        this.div.attr("id", "form-div-" + this.form_index)
        this.div_joad.attr("id", "form-div-" + this.form_index + "-joad")
        this.first_name_input.attr("id", "id_member_set-" + this.form_index + "-first_name")
        this.last_name_input.attr("id", "id_member_set-" + this.form_index + "-last_name")
        this.dob_input.attr("id", "id_member_set-" + this.form_index + "-last_name")
    }

    dob_check() {
        console.log('dob blur')
        var bd = new Date(this.dob_input.val());
        var joad_date = new Date();
        joad_date.setFullYear(joad_date.getFullYear() - 21);
        if(bd > joad_date && bd < new Date()) {
            this.div_joad.show()
        } else {
            this.div_joad.hide()
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