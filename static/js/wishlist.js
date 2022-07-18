$(".favourite").click(function () {
    var a = $(this).attr("src");
    if (a === '/static/images/heart.png') {
        $(this).attr("src", "/static/images/fillheart.png")
        $.ajax({
            type: "POST",
            url: "http://127.0.0.1:8000/add-to-favourite/",
            headers: {
                "X-CSRFToken": CSRF_TOKEN
            },
            data: {
                'prod_id': $(this).attr("alt")
            },
            success: function (response) {

                status = response.msg;
                console.log(status);

            }
        })
    }
    else {
        $(this).attr("src", "/static/images/heart.png")
        var prod_id = $(this).attr("alt");
        $.ajax({
            type: "POST",
            url: "http://127.0.0.1:8000/add-to-favourite/",
            headers: {
                "X-CSRFToken": CSRF_TOKEN
            },
            data: {
                'prod_id': $(this).attr("alt")
            },
            success: function (response) {

                var status = response.msg;
                $("#fav-item"+prod_id).fadeOut(800);
                $("#msg").text("Removed from Wishlist").fadeIn(500).fadeOut(2000)
                // $("#wishlist-box").load(location.href + " #wishlist-box");
            }
        })
    }
})



$("#msg").hide();