$("#signupform").submit(function (evt) {
    evt.preventDefault();
    $.ajax({
        type: "POST",
        url: "http://127.0.0.1:8000/validation-signup/",
        headers: {
            "X-CSRFToken": CSRF_TOKEN
        },
        data: {
            'first_name': $("#id_first_name").val(),
            'last_name': $("#id_last_name").val(),
            'email': $("#id_email").val(),
            'phone': $("#id_phone").val(),
            'password1': $("#id_password1").val(),
            'password2': $("#id_password2").val()
        },
        success: function (response) {
            var field = response.field;
            var msg = response.msg;
            if (field === "ok") {
                $('#signupform').unbind('submit').submit();
            }
            else {
                $("#id_email").removeClass("is-invalid")
                $("#id_phone").removeClass("is-invalid")
                $("#id_password1").removeClass("is-invalid")
                $("#id_password2").removeClass("is-invalid")
                $("#msg-" + field).text(msg);
                $("#id_" + field).addClass("is-invalid");
            }

        }
    })
})



$("#id_email").attr("aria-describedby", "msg-email")
$("#id_phone").attr("aria-describedby", "msg-phone")
$("#id_password1").attr("aria-describedby", "msg-password1")
$("#id_password2").attr("aria-describedby", "msg-password2")
$("#id_password1").addClass("form-control mx-1")
$("#id_password2").addClass("form-control mx-1")
$("#id_password2").attr("placeholder", "Re-enter password")
$("#id_password1").attr("placeholder", "Enter password")