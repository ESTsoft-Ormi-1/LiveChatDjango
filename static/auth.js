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
                // 로그인 후 프로필 설정 페이지로 이동
                var profileSettingsURL = "http://127.0.0.1:8000/mysite/user/v1/profile/"; // 프로필 설정 화면 URL로 변경
                var token = response.access;
                
                // 토큰을 LocalStorage에 저장 (이후에 사용자의 세션이 끝날 때까지 유지)
                localStorage.setItem('token', token);
    
                // 프로필 설정 페이지로 이동하며 토큰을 인증 헤더에 포함하여 전송
                window.location.href = profileSettingsURL;
            },
            error: function(error) {
                $("#result").text("로그인 실패");
            }
        });
    });   
});
