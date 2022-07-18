$(".selectAddBtn").click(function () {
    var id = $(this).attr("id");
    console.log(id);
    $.ajax({
        type: "PUT",
        url: "http://127.0.0.1:8000/set-default-address/",
        headers: {
            "X-CSRFToken": CSRF_TOKEN
        },
        data: {
            'add_id': id
        },
        success: function (response) {

            var status = response.msg;
            console.log(status);
            $("#defaultAddress").load(location.href + " #defaultAddress");

        }
    })
})




$("#addAddressForm").submit(function (evt) {
    evt.preventDefault();
    var form = $(this);
    $.ajax({
        type: "POST",
        url: "http://127.0.0.1:8000/add-new-address/",
        headers: {
            "X-CSRFToken": CSRF_TOKEN
        },
        data: form.serialize(),
        success: function (response) {

            var status = response.msg;
            console.log(status);
            $("#addAddressForm").trigger("reset")
            $("#close-btn").click();
            $("#all-address-box").load(location.href + " #all-address-box")
        }
    })

})