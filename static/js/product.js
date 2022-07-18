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

                var status = response.msg;
                console.log(status);
                $("#msg").text("Added to Wishlist").fadeIn(100).fadeOut(3000)

            }
        })
    }
    else {
        $(this).attr("src", "/static/images/heart.png")
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
                console.log(status);
                $("#msg").text("Removed from Wishlist").fadeIn(100).fadeOut(3000)
            }
        })
    }
})


$("#msg").hide();



$("#addReviewForm").submit(function (evt) {
    evt.preventDefault();
    var id = $("#product_id").val()
    var comment = $("#comment").val()
    console.log(id)
    console.log(comment)
    $.ajax({
        type: "POST",
        url: "http://127.0.0.1:8000/add-review/",
        headers: {
            "X-CSRFToken": CSRF_TOKEN
        },
        data: {
            'prod_id': $("#product_id").val(),
            'comment': $("#comment").val()
        },
        success: function (response) {
            var status = response.msg;
            if (status === "added") {
                $("#addReviewForm")[0].reset();
                $("#commentss").load(location.href + " #commentss");
            }
            else {
                $("#msg").text("Please login to add review for this product").fadeIn(500).fadeOut(3000)
            }
        }
    })
})





$("#addtocartbtn").click(function () {
    var id = $("#prod_id").val();
    $.ajax({
        type: "POST",
        url: "http://127.0.0.1:8000/add-to-cart/",
        headers: {
            "X-CSRFToken": CSRF_TOKEN
        },
        data: {
            'id': id
        },
        success: function (response) {

            status = response.msg;
            if (status === "added") {
                console.log(status)
                $("#cart-count").load(location.href + " #cart-count")
                $("#msg").text("Added to Cart").fadeIn(500).fadeOut(3000)
            }
            else {
                console.log(status)
            }

        }
    })
})


$(".rate-star").click(function () {
    var rating = $(this).attr("alt");
    console.log(rating);
    var id = $("#prod_id").val();
    $.ajax({
        type: "POST",
        url: "http://127.0.0.1:8000/add-rating/",
        headers: {
            "X-CSRFToken": CSRF_TOKEN
        },
        data: {
            'prod_id': id,
            'rating': rating
        },
        success: function (response) {

            var status = response.msg;
            if (status === "Rated") {
                $("#rating-box").load(location.href + " #rating-box")
            }
            else {
                $("#msg").text(status).fadeIn(500).fadeOut(3000)
            }

        }
    })

})