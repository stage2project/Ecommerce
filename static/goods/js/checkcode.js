var emailPertten=/^\w+((.\w+)|(-\w+))@[A-Za-z0-9]+((.|-)[A-Za-z0-9]+).[A-Za-z0-9]+$/;

var phonePertten=/^1[3456789]\d{9}$/;

var code ; //在全局定义验证码   
//产生验证码  
function createCode(){
     code = "";   
     var codeLength = 4;//验证码的长度  
     var checkCode = document.getElementById("code");   
     var random = new Array(0,1,2,3,4,5,6,7,8,9,'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R',  
     'S','T','U','V','W','X','Y','Z');//随机数  
     for(var i = 0; i < codeLength; i++) {//循环操作  
        var index = Math.floor(Math.random()*36);//取得随机数的索引（0~35）  
        code += random[index];//根据索引取得随机数加到code上  
    }  
    checkCode.value = code;//把code值赋给验证码
}  
//校验验证码  
function validate(){
    var uname = document.getElementById("username").value;
    var pwd = document.getElementById("password").value;
    if(uname == null || pwd == null) return false;
    var send_flag =  -1; //0- 邮箱 1- 用户名， 2- 手机号

    if(phonePertten.test(uname)){
        send_flag = 2;
    }
    else if(emailPertten.test(uname)){
        send_flag=0;
    }
    else {
        send_flag =1;
    }
    var myform = document.getElementById("loginForm");

    var tmpInput=document.createElement("input");
    tmpInput.type="hidden";
    tmpInput.name="type";
    tmpInput.value=send_flag;
     myform.appendChild(tmpInput);
    // myform.submit();
    var inputCode = document.getElementById("authcode").value.toUpperCase(); //取得输入的验证码并转化为大写
    //
    if(inputCode.length <= 0) { //若输入的验证码长度为0
        alert("请输入验证码！"); //则弹出请输入验证码
    }
    else if(inputCode != code ) { //若输入的验证码与产生的验证码不一致时
        alert("验证码输入错误！@_@"); //则弹出验证码输入错误
        createCode();//刷新验证码
        document.getElementById("input").value = "";//清空文本框
    }
    else { //输入正确时
        // alert("登陆成功"); //弹出^-^
        myform.submit();
    }


}