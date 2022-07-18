$("#confirmPwdForm").submit(function (evt) {
    evt.preventDefault();
    $.ajax({
        type: "POST",
        url: "http://127.0.0.1:8000/confirm-password/",
        headers: {
            "X-CSRFToken": CSRF_TOKEN
        },
        data: {
            'password': $("#password3").val()
        },
        success: function (response) {

            status = response.msg;
            console.log(status);
            if (status === "authenticated") {
                $("#addBalanceBtn").click();
                $("#addBalanceFormBtn").click();
            }
            else {
                $("#error4").text(response.msg).fadeOut(5000);
            }

        }
    })
})


$("#addBalanceForm").submit(function (evt) {
    evt.preventDefault();
    $.ajax({
        type: "POST",
        url: "http://127.0.0.1:8000/add-balance/",
        headers: {
            "X-CSRFToken": CSRF_TOKEN
        },
        data: {
            'amount': $("#amount").val(),
        },
        success: function (response) {

            var status = response.msg;
            console.log(status);
            if (status === "added") {
                // location.reload();
                $("#amount").val("");
                $("#addBalanceFormBtn").click();
                if (window.history.replaceState) {
                    window.history.replaceState(null, null, window.location.href);
                }
                $("#wallet-box").load(location.href + " #wallet-box");

            }
            else {
                $("#error5").text(response.msg).fadeOut(5000);
            }

        }
    })
})








function w3_open() {
    document.getElementById("mySidebar").style.display = "block";
}

function w3_close() {
    document.getElementById("mySidebar").style.display = "none";
}

$("#search").click(function () {
    $("#search-box").css("display", "block")
    $.ajax({
        type: "GET",
        url: "http://127.0.0.1:8000/get-search-history/", // be mindful of url names
        data: {
            'data': null,
        },
        success: function (response) {

            var status = response.msg;
            if (status === "No") {
                console.log("No search History")
            }
            else {
                $("#search-box").html("<span id='searchSpan'></span>")
                $(status).each(function (i, obj) {
                    console.log(obj.title)
                    $("#searchSpan").after(`<a class='search-history-links' onclick="searchHist('` + (obj.title) + `')">` + (obj.title) + `</a>`)
                })
            }
        }
    })
})

function searchHist(t) {
    $("#search").val(t);
}

$("#body").mousedown(function () {
    $("#search-box").css("display", "none");
})

function clickLink(t) {
    console.log(t)
    $.ajax({
        type: "POST",
        url: "http://127.0.0.1:8000/search-history-save/", // be mindful of url names
        data: {
            'data': t,
        },
        success: function (response) {
            var status = response.msg;
        }
    })
}


$("#search").keyup(function () {
    $.ajax({
        type: "GET",
        url: "http://127.0.0.1:8000/search-show/", // be mindful of url names
        data: {
            'data': $(this).val(),
        },
        success: function (response) {

            var status = response.msg;
            $("#search-box").html("<span id='searchSpan'></span>")
            $(status).each(function (i, obj) {
                console.log(obj.name)
                $("#searchSpan").after(`<a href=/view-product/` + obj.slug + `/ onclick="clickLink('` + (obj.name).substring(0, 80) + `')" class='search-links'>` + (obj.name).substring(0, 80) + `</a>`)
            })
        }
    })
})
