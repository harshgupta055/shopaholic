$('#profileUpdateForm').submit(function (evt) {
    evt.preventDefault();
    $.ajax({
        type: "POST",
        url: "http://127.0.0.1:8000/profile/",
        headers: {
            "X-CSRFToken": CSRF_TOKEN
        },
        data: {
            'first_name': $("#first_name").val(),
            'last_name': $("#last_name").val(),
            'phone': $("#phone").val()
        },
        success: function (response) {

            var status = response.msg;
            console.log(status);
            if (status === "Updated") {
                location.reload();
            }
            else {
                $("#error").text(response.msg).fadeOut(5000);
            }

        }
    })
})


$("#confirmPwdForm2").submit(function (evt) {
    evt.preventDefault();
    $.ajax({
        type: "POST",
        url: "http://127.0.0.1:8000/confirm-password/",
        headers: {
            "X-CSRFToken": CSRF_TOKEN
        },
        data: {
            'password': $("#password").val()
        },
        success: function (response) {

            var status = response.msg;
            console.log(status);
            if (status === "authenticated") {
                $("#changepwdbtn").click();
                $("#newPwdBtn").click();
            }
            else {
                $("#error2").text(response.msg).fadeOut(5000);
            }

        }
    })
})


$("#pwdUpdateForm").submit(function(evt){
    evt.preventDefault();
    $.ajax({
        type: "POST",
        url: "http://127.0.0.1:8000/password-update/",
        headers: {
            "X-CSRFToken": CSRF_TOKEN
        },
        data: {
            'password1': $("#password1").val(),
            'password2': $("#password2").val()
        },
        success: function (response) {

            var status = response.resp;
            console.log(status);
            if (status === "success") {
                $("#success").text("Your password has been changed").fadeIn(100).fadeOut(4000)
                $("#newPwdBtn").click();
                $("#pwdUpdateForm").trigger("reset");
                $("#confirmPwdForm").trigger("reset");
            }
            else {
                $("#error3").text(response.msg).fadeOut(5000);
            }

        }
    })
})