

$(".addQbtn").click(function () {
    var id = $(this).attr("aria-details");
    var q = $("#quant" + id).attr("value");
    if (q < "5") {
        $.ajax({
            type: "POST",
            url: "http://127.0.0.1:8000/add-qantity/", // be mindful of url names
            data: {
                "id": id,
                "quantity": parseInt(q) + 1
            },
            success: function (response) {
                var status = response.msg;
                console.log(status);
                if (status == "added") {
                    // $("#pricesummary").load(location.href + " #pricesummary")
                    q = parseInt(q) + 1;
                    $("#quant" + id).attr("value", q);
                    $("#quanti" + id).text(q);
                    var cal = $("#price" + id).text();
                    var t = $("#total").text();
                    t = parseFloat(t) + parseFloat(cal);
                    $("#total").text(t + ".0");
                }
                else {
                    console.log("cannot add")
                }
            }
        })
    }
})


$(".subQbtn").click(function () {
    var id = $(this).attr("aria-details");
    var q = $("#quant" + id).attr("value");
    if (q > "1") {
        $.ajax({
            type: "POST",
            url: "http://127.0.0.1:8000/add-qantity/", // be mindful of url names
            data: {
                "id": id,
                "quantity": parseInt(q) - 1
            },
            success: function (response) {
                var status = response.msg;
                if (status == "added") {
                    // $("#pricesummary").load(location.href + " #pricesummary")
                    q = parseInt(q) - 1;
                    $("#quant" + id).attr("value", q);
                    $("#quanti" + id).text(q);
                    var cal = $("#price" + id).text();
                    var t = $("#total").text();
                    t = parseFloat(t) - parseFloat(cal);
                    $("#total").text(t + ".0");
                }
                else {
                    console.log("cannot remove")
                }
            }
        })
    }
})



$(".delete-item").click(function () {
    var id = $(this).attr("alt");
    console.log(id);
    $.ajax({
        type: "DELETE",
        url: "http://127.0.0.1:8000/remove-from-cart/", // be mindful of url names
        headers: {
            "X-CSRFToken": CSRF_TOKEN
        },
        data: {
            "id": id,
        },
        success: function (response) {
            var status = response.msg;
            console.log(status);
            location.reload()
            // $("#cart-count").load(location.href + " #cart-count")
            // $("#cart-box").load(location.href + " #cart-box")
        },
    })
})