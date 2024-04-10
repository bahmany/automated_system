jQuery(document).ready(function () {


    $(function () {



        // using jQuery
        function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie !== '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = jQuery.trim(cookies[i]);
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) === (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }

        var csrftoken = getCookie('rahsoon-CSRF-TOKEN');

        function csrfSafeMethod(method) {
            // these HTTP methods do not require CSRF protection
            return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
        }

        $.ajaxSetup({
            beforeSend: function (xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("rahsoon-csrftoken", csrftoken);
                }
            }
        });


        $.backstretch("/static/login/media/1.jpg");
        $('.login-form input[type="text"], .login-form input[type="password"], .login-form textarea').on('focus', function () {
            $(this).removeClass('input-error');
        });

        function refreshCaptcha() {
            $.getJSON('/captcha/refresh/', {}, function (json) {
                $("#id_captcha_0").attr("value", json.key);
                $(".captcha").attr("src", json.image_url);
            });
        }

        function refreshCaptchaReg() {
            $.getJSON('/reg/api/v1/login/registerRefCaptcha/', {}, function (json) {
                $("#id_captcha2_0").attr("value", json.key);
                $(".captch-reg .captcha").attr("src", json.image_url);
            });
        }

        $('.btn-ref-cap').on('click', function (e) {
            refreshCaptcha()
        });
        $('.btn-ref-cap-reg').on('click', function (e) {
            refreshCaptchaReg()
        });
        $('.login-form').on('submit', function (e) {
            e.preventDefault();

            $(this).find('input[type="text"], input[type="password"], textarea').each(function () {
                if ($(this).val() == "") {
                    e.preventDefault();
                    $(this).addClass('input-error');
                }
                else {
                    $(this).removeClass('input-error');
                }
            });

            $('.btn-login').text('کنترل صحت').attr('disabled', 'true');


            var isValid = $('.login-form').valid();


            if (isValid) {
                $('.error-login').fadeOut(function () {
                        $.ajax(
                            {
                                type: 'post',
                                url: "/api/v1/auth/login/",
                                data: $('.login-form').serialize(),
                                success: function (data) {
                                    if (data.u === 1) {
                                        window.location.reload();
                                        // return
                                    }
                                    if (data.u === 2) {
                                        // window.location = "/dashboards/";
                                        // return
                                        window.location.reload();

                                    }
                                    if (data.u === 3) {
                                        // window.location = "/dashboards/";
                                        // return
                                        window.location.reload();

                                    }
                                    if (data.u === 4) {
                                        // window.location = "/dashboards/";
                                        // return
                                        window.location.reload();

                                    }
                                    if (data.u === 5) {
                                        // window.location = "/dashboards/";
                                        // return
                                        window.location.reload();

                                    }
                                    if (data.u === 6) {
                                        // window.location = "/dashboards/";
                                        window.location.reload();
                                        // return/

                                    }
                                    if (data.u === 7) {
                                        // window.location = "/dashboards/";
                                        window.location.reload();
                                        // return

                                    }

                                },
                                error: function (data) {
                                    if (data["status"]) {


                                        $.getJSON('/captcha/refresh/', {}, function (json) {
                                            $("#id_captcha_0").attr("value", json.key);
                                            // debugger;
                                            $('.error-login').text(data.responseJSON.message);
                                            $(".captcha").attr("src", json.image_url);
                                            $('.error-login').fadeIn(function () {
                                                $('.captch-login').fadeIn(function () {
                                                    $('.btn-login').text('ورود').attr('disabled', null);

                                                });
                                            });


                                        })


                                    }
                                }
                            });
                    }
                );

            }


        });
        $('.registration-form input[type="text"], .registration-form textarea').on('focus', function () {
            $(this).removeClass('input-error');
            $('.reg-help').fadeIn()

        });


        $('.registration-form').on('submit', function (e) {

            e.preventDefault();

            $(this).find('input[type="text"],input[type="email"],input[type="password"], textarea').each(function () {
                if ($(this).val() == "") {
                    e.preventDefault();
                    $(this).addClass('input-error');
                }
                else {
                    $(this).removeClass('input-error');
                }
            });

            var isValid = $(".registration-form").valid();
            if (isValid) {

                $('.btn-ref-cap-reg').text('کنترل صحت').attr('disabled', 'true');

                $.ajax({
                    type: "POST",
                    url: "/reg/api/v1/login/register/",
                    data: $(".registration-form").serialize(),
                    success: function (data) {
                        window.location.href = "/";

                    },
                    error: function (data) {
                        $('.btn-ref-cap-reg').text('ثبت نام').attr('disabled', null);
                        var ht = "<h3 style='color: red;'>ثبت نام به دلایل زیر با موفقیت انجام نشد</h3>";
                        for (var i = 0; data.responseJSON.message.length > i; i++) {
                            ht += "<i class='fa fa-warning'></i><strong>" + data.responseJSON.message[i].fieldName + "</strong> : " + data.responseJSON.message[i].message + "<br>"
                        }
                        $('.error-after-post').html(ht);
                        refreshCaptchaReg();
                    }
                })
            }

        });
    });

});

// $.cookie("domainName",window.location.hostname);
// if (location.protocol !== 'https:') {
//     location.replace("https://app.******.com");
// }