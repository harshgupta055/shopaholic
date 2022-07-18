$(".address").click(function () {
    $(".address").attr("src", "/static/images/not_default.png")
    $(this).attr("src", "/static/images/default.png")
    $.ajax({
        type: "PUT",
        url: "http://127.0.0.1:8000/set-default-address/",
        headers: {
            "X-CSRFToken": CSRF_TOKEN
        },
        data: {
            'add_id': $(this).attr("alt")
        },
        success: function (response) {

            var status = response.msg;
            console.log(status);

        }
    })
})


$("#addAddressForm").submit(function (evt) {
    evt.preventDefault();
    var form = $(this);
    $.ajax({
        type: "POST",
        url: "http://127.0.0.1:8000/add-new-address/", // be mindful of url names
        headers: {
            "X-CSRFToken": CSRF_TOKEN
        },
        data: form.serialize(),
        success: function (response) {

            var status = response.msg;
            console.log(status);
            location.reload();

        }
    })

})


$(".delete-address").click(function () {
    var c = confirm("Do you want to delete the address?")
    if (c === true) {
        $.ajax({
            type: "DELETE",
            url: "http://127.0.0.1:8000/delete-address/", // be mindful of url names
            headers: {
                "X-CSRFToken": CSRF_TOKEN
            },
            data: {
                "id": $(this).attr("alt")
            },
            success: function (response) {

                var status = response.msg;
                console.log(status);
                location.reload();

            }
        })
    }
})