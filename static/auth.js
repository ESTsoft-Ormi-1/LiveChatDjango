$(document).ready(function() {
    $("#signup").click(function() {
        var email = $("#email").val();
        var password = $("#password").val();
        var data = {
            email: email,
            password1: password,
            password2: password
        };

        $.ajax({
            url: "http://127.0.0.1:8000/mysite/user/v1/registration/",
            type: "POST",
            data: data,
            success: function(response) {
                $("#result").text("회원가입 성공");
            },
            error: function(error) {
                $("#result").text("회원가입 실패");
            }
        });
    });

    $("#login").click(function() {
        var email = $("#email").val();
        var password = $("#password").val();
        var data = {
            email: email,
            password: password
        };

        $.ajax({
            url: "http://127.0.0.1:8000/mysite/user/v1/login/",
            type: "POST",
            data: data,
            success: function(response) {
                $("#result").text("로그인 성공 - 토큰: " + response.access);
            },
            error: function(error) {
                $("#result").text("로그인 실패");
            }
        });
    });
});
