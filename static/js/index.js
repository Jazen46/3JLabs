var login = ["<form action=login method=POST>",
            "<input type=text placeholder=Username name=username>",
            "<input type=password placeholder=Password name=password>",
            "<input type=submit value=LOGIN name=login>"].join("\n");
var signup = ["<form action=signup method=POST>",
            "<input type=text placeholder=Username name=username>",
            "<input type=password placeholder=Password name=password>","<input type=password placeholder='Repeat Password' name=password2>",
            "<input type=submit value='SIGN UP' name=signup>"].join("\n");

$(document).ready(function(){
    $("#login-tab").click(function(){
        $("#login-tab").addClass("active");
        $("#signup-tab").removeClass("active");
        refresh($("#login-box"),login);
    });
    $("#signup-tab").click(function(){
        $("#login-tab").removeClass("active");
        $("#signup-tab").addClass("active");
        refresh($("#login-box"),signup);
    });
});
var refresh=function(target,newCode){
    target.empty();
    target.append(newCode);
}
