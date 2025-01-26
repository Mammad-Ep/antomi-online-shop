
// ________________________________________________________________________

// Refresh image Recaptcha- رفرش کردن عکس ریکپچا
$(function () {
    // Add refresh button after field (this can be done in the template as well)

    $('#id_captcha_field_0').after(
        $('<a href="#void" class="captcha-refresh mx-2 text-black-50"><i class="fa fa-refresh" aria-hidden="true"></i></a>')
    );

    // Click-handler for the refresh-link
    $('.captcha-refresh').click(function () {
        var $form = $(this).parents('form');
        var url = location.protocol + "//" + window.location.hostname + ":"
            + location.port + "/captcha/refresh/";

        // Make the AJAX-call
        $.getJSON(url, {}, function (json) {
            $form.find('input[name="captcha_field_0"]').val(json.key);
            $form.find('img.captcha').attr('src', json.image_url);
        });

        return false;
    });
});

// ________________________________________________________________________

// نمایش پیغام برای مشتری
function show_message(message) {
    $('#message-box-script').show();
    $('#message-box-script p').text(message);
}
// ________________________________________________________________________

//    verify-phone-number------------------------
if ($("#countdown-verify-end").length) {
    var $countdownOptionEnd = $("#countdown-verify-end");

    $countdownOptionEnd.countdown({
        date: (new Date()).getTime() + 120 * 1000, // 1 minute later
        text: '<span class="day">%s</span><span class="hour">%s</span><span>: %s</span><span>%s</span>',

        end: function () {
            $('#submit-verify').attr('style', 'visibility:hidden;');
            $countdownOptionEnd.html("<a href='/send_sms_again/' class='link-border-verify form-account-link'>ارسال مجدد</a>");
        }
    });
}




$(document).ready(function () {
    // get start time and current time from local storage or set default values 
    let startTime = localStorage.getItem("startTime") || Date.now();
    let currentTime = Date.now();

    // calculate the remaining time 
    let remainingTime = startTime + 60 * 1000 - currentTime;

    // update the start time in local storage 
    localStorage.setItem("startTime", startTime);

    // update the countdown every second 
    let intervalId = setInterval(function () {
        currentTime = Date.now();
        remainingTime = startTime +  60 * 1000 - currentTime;

        // stop the interval when the countdown reaches 0 
        if (remainingTime <= 0) {
            clearInterval(intervalId);

        }

        // update the UI with the remaining time 
        let minutes = Math.floor(remainingTime / (1000 * 60));
        let seconds = Math.floor((remainingTime % (1000 * 60)) / 1000);
        let display = `${minutes}:${seconds}`;
        document.getElementById("countdown-timer").innerHTML = display;
    }, 1000);
})




// function send_sms_again() {

//     $.ajax({
//         type:'GET',
//         url:'/send_sms_again/',
//         data:{},

//         success:function(){
//             $('#submit-verify').attr('style','visibility:visible;');
//         }
//     })
// }
//    verify-phone-number-----------------------

// ________________________________________________________________________

function add_star(score, product_id) {

    $.ajax({
        type: 'GET',
        url: '/add_score/',
        data: {
            product_id: product_id,
            score: score
        },

        success: function (res) {
            $('#scorings_partal').html(res);
            show_message('امتیاز شما به محصول ثبت شد')

        }
    })
}
// ________________________________________________________________________

// اکتیو کردن هدر و تب مربوط به باکس محصولات index
function active_header_tab_products() {
    $('.product_area .container .product_header .nav li:first-child a').addClass('active');
    $('.product_area .tab-content div:first-child').addClass('active');
}
// ________________________________________________________________________

function create_comment_child(product_id, comment_id) {
    $('#btn-child' + comment_id).css('visibility', 'hidden');
    $.ajax({
        type: 'GET',
        url: '/create_comment_child/',
        data: {
            product_id: product_id,
            comment_id: comment_id,
        },

        success: function (res) {
            $('#comment-child-section' + comment_id).html(res)
        }
    })
}

// // like comment

function add_like_comment(comment_id, like_type) {

    $.ajax({
        type: 'GET',
        url: '/add_like_comment/',

        data: {
            comment_id: comment_id,
            like_type: like_type
        },

        success: function (res) {
            alert('امتیاز شما به این دیدگاه ثبت شد');
            $('#like-box' + comment_id).html(res);
        }
    })
}
// ________________________________________________________________________

function cancel_commnet(comment_id) {

    $('#btn-child' + comment_id).css('visibility', 'visible');

}

// ________________________________________________________________________

// تابع حذف پارامتر از خط آدرس
function removeURLParameter(url, parameter) {
    var urlparts = url.split('?');
    if (urlparts.length >= 2) {
        var prefix = encodeURIComponent(parameter) + '=';
        var pars = urlparts[1].split(/[&;]/g);
        for (var i = pars.length; i-- > 0;) {
            if (pars[i].lastIndexOf(prefix, 0) !== -1) {
                pars.splice(i, 1)
            }

        }
        return urlparts[0] + (pars.length > 0 ? '?' + pars.join('&') : '');

    }
    return url;
}

// __________________________________________________________________________________

// تابع انتخاب مرتب سازی محصولات 
function select_sort() {
    var select_sort_value = $("#select_sort").val();
    var data = "?"
    var url = removeURLParameter(window.location.href, "sort_type");

    if (url.includes(data)) {
        window.location = url + "&sort_type=" + select_sort_value;
    } else {
        window.location = url + "?sort_type=" + select_sort_value;
    }

}

// __________________________________________________________________________________

// // Compare Products

status_compare_product();

function status_compare_product() {
    $.ajax({
        type: 'GET',
        url: '/status_compare_product/',

        success: function (res) {
            $('#compare-count').text(res)
        }
    })
}

// ----------------------------------------------------

function add_compare_product(product_id, group_id) {

    $.ajax({
        type: 'GET',
        url: '/add_compare_product/',
        data: {
            product_id: product_id,
            group_id: group_id
        },

        success: function (res) {
            // alert(res);
            $('#message-box-script p').text(res);
            $('#message-box-script').show();

            status_compare_product();
        }
    })
}

// ----------------------------------------------------

function remove_compare_product(product_id, group_id) {

    $.ajax({
        type: 'GET',
        url: '/remove_compare_product/',
        data: {
            product_id: product_id,
            group_id: group_id
        },

        success: function (res) {
            $('#compare-products-box').html(res)
            status_compare_product();
        }
    })
}
// __________________________________________________________________________________

// // Shop Cart


function plus_number_product(product_id, max) {
    var number = document.getElementById("qty_" + product_id).value;
    if (number < max) {
        number++;
        document.getElementById("qty_" + product_id).value = number
    };

    return true
};


function minus_number_product(product_id) {
    var number = document.getElementById("qty_" + product_id).value;
    if (number > 1) {
        number--;
        document.getElementById("qty_" + product_id).value = number
    };

};
// ----------------------------------------------------

function plus_product_cart(product_id, max) {
    var number = document.getElementById("qty_cart" + product_id).value;
    if (number < max) {
        number++;
        document.getElementById("qty_cart" + product_id).value = number
    };

    var qty = number;

    $.ajax({
        type: 'GET',
        url: '/update_shop_cart/',
        data: {
            product_id: product_id,
            qty: qty
        },

        success: function (res) {
            $('#shop_cart_list').html(res);
            status_shop_cart();
        }
    })
};


function minus_product_cart(product_id) {
    var number = document.getElementById("qty_cart" + product_id).value;
    if (number > 1) {
        number--;
        document.getElementById("qty_cart" + product_id).value = number
    };

    var qty = number;

    $.ajax({
        type: 'GET',
        url: '/update_shop_cart/',
        data: {
            product_id: product_id,
            qty: qty
        },

        success: function (res) {
            $('#shop_cart_list').html(res);
            status_shop_cart();
        }
    })

};

status_shop_cart();

function status_shop_cart() {

    $.ajax({
        type: 'GET',
        url: '/status_shop_cart/',

        success: function (res) {
            $('#cart_count').text(res)
        }
    })
}
// ----------------------------------------------------


function add_shop_cart(product_id, qty) {
    if (qty === 0) {
        qty = Number($('#qty_' + product_id).val())
    };

    $.ajax({
        type: 'GET',
        url: '/add_shop_cart/',
        data: {
            product_id: product_id,
            qty: qty
        },

        success: function (res) {
            alert('محصول به سبد خرید اضافه شد');
            status_shop_cart()
        }
    })
}


function update_shop_cart(product_id) {
    var qty = $('#qty' + product_id).val();
    // var qty = $('#qty-cart'+product_id).val();

    $.ajax({
        type: 'GET',
        url: '/update_shop_cart/',
        data: {
            product_id: product_id,
            qty: qty
        },

        success: function (res) {
            $('#shop_cart_list').html(res);
            status_shop_cart();
        }
    })
}

// ----------------------------------------------------

function remove_shop_cart(product_id) {

    $.ajax({
        type: 'GET',
        url: '/remove_shop_cart/',
        data: {
            product_id: product_id,
        },

        success: function (res) {
            $('#shop_cart_list').html(res);
            status_shop_cart()
        }
    })
}
// __________________________________________________________________________________

// // Favorites

status_favorite_product();

function status_favorite_product() {
    $.ajax({
        type: 'GET',
        url: '/status_favorite_product/',


        success: function (res) {
            $('#wishlist-count').text(res)

        }
    })
}
// ----------------------------------------------------

function add_favorite_product(product_id) {

    $.ajax({
        type: 'GET',
        url: '/add_favorite_product/',
        data: {
            product_id: product_id
        },

        success: function (res) {
            $(`.wishlist #favorite_${product_id}`).removeClass('fa-regular');
            $(`.wishlist #favorite_${product_id}`).addClass('fa-solid');
            show_message(res);
            status_favorite_product();
        }
    })
};

function alert_for_favorite() {
    alert('برای ثبت علاقه مندی ابتدا وارد شوید')
}

// ----------------------------------------------------

function remove_favorite_product(product_id) {
    $.ajax({
        type: 'GET',
        url: '/remove_favorite_product/',
        data: {
            product_id: product_id
        },

        success: function (res) {
            $('.wishlist_inner').html(res);
            status_favorite_product();

        }
    })
}


// __________________________________________________________________________________

$(document).ready(function () {

    // # two dropdown in adminpanel
    var listOfElements = $('select[id^="select2-id_product_features-"][id$="-feature-container"]')
    $(listOfElements).on('change', function () {
        f_id = $(this).val();
        dd1 = $(this).attr('id');
        dd2 = dd1.replace("-feature", "-filter_value")

        $.ajax({
            type: "GET",
            url: "/ajax_admin/?feature_id=" + f_id,
            success: function (res) {
                cols = document.getElementById(dd2),
                    cols.options.length = 0;
                for (var k in res) {
                    cols.options.add(new Option(k, res[k]));
                }
            }

        });
    });


    // payment-Tpye
    $('.payment_method div:first-child input').attr('checked', 'checked');

    // time close message-box
    $('.alert').fadeOut(15000).removeClass('fade');
    $('#message-box-script .alert').fadeOut(15000).removeClass('fade');
    active_header_tab_products();


    // اسکریپت برای ماندن مقادیر فیلتر بعداز اعمال کردن و زدن دکمه فیلتر
    var urlParams = new URLSearchParams(window.location.search);
    if (urlParams == "") {
        localStorage.clear()
        $("#filter-state").css("display", "none");

    } else {
        $("#filter-state").css("display", "inline-block");
    }
    $("input:checkbox").on("click", function () {
        var fav, favs = [];
        $("input:checkbox").each(function () {
            fav = { id: $(this).attr('id'), value: $(this).prop("checked") };
            favs.push(fav);
        })
        localStorage.setItem("favorites", JSON.stringify(favs));
    })

    var favorites = JSON.parse(localStorage.getItem('favorites'));
    for (let i = 0; i < favorites.length; i++) {
        $("#" + favorites[i].id).prop('checked', favorites[i].value);

    }

});
// __________________________________________________________________________________


