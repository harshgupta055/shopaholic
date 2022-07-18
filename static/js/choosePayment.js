$("#choosePaymentForm").submit(function (evt) {
    evt.preventDefault();
    var d = $(this).serialize();
    console.log(d)
    var a = d.split("=")[1];
    console.log(a)
    if (a === "Wallet") {
        $.ajax({
            type: "GET",
            url: "http://127.0.0.1:8000/check-balance/", // be mindful of url names
            data: {
                'total': $("#total").text()
            },
            success: function (response) {

                var status = response.msg;
                console.log(status)
                if (status === "ok") {
                    $("#mode").val(a);
                    $("#paymentForm").submit();
                    console.log("done")
                }
                else {
                    $("#error").text(status).fadeIn(500).fadeOut(5000);
                }

            }
        })
    }
    else{
        $("#mode").val(a);
        $("#paymentForm").submit();
    }
})