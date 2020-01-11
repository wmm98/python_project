// // 点击登录按钮， 弹出模态对话框
// $(function(){
//     // 弹出的对话框
//     $('#btn').click(function(){
//         $(".mask-wrapper").show()
//     })
//     $('.close-btn').click(function(){
//         $('.mask-wrapper').hide()
//     })
// })
//
// 登录注册页面切换
// $(function(){
//     $(".switch").click(function(){
//         //获取盒子的大小
//         var scrollWrapper = $(".scroll-wrapper")
//         //获取当前位置
//         var currentLeft = scrollWrapper.css("left")
//         // 转换为整数
//         currentLeft = parseInt(currentLeft)
//         if(currentLeft < 0){
//             scrollWrapper.animate({"left": "0"})
//         }else{
//             scrollWrapper.animate({"left": "-400px"})
//         }
//     })
// })
//
function Auth(){
    var self = this
    self.maskWrapper = $(".mask-wrapper")
    self.scrollWrapper = $(".scroll-wrapper")

}

Auth.prototype.run = function(){
    var self = this
    self.listenShowHideEvent()
    self.listenSwitchEvent()
    self.listenSigninEvent()
}

// 显示
Auth.prototype.showEvent = function(){
    var self = this
    self.maskWrapper.show()

}

// 隐藏
Auth.prototype.hideEvent = function(){
    var self = this
    self.maskWrapper.hide()
}

//监听点击事件
Auth.prototype.listenShowHideEvent = function(){
    var self = this;
    var signinBtn = $('.signin-btn');
    var signupBtn = $('.signup-btn');
    var closeBtn = $('.close-btn');
    //登录注册对话框
    signinBtn.click(function(){
        self.showEvent()
        //修改css样式显示为登录对话框
        self.scrollWrapper.css({"left": 0})
    })

    signupBtn.click(function(){
        self.showEvent()
        self.scrollWrapper.css({"left": -400})
    })

    // 点击关闭按钮隐藏
    closeBtn.click(function(){
        self.hideEvent()
    })
}

// 监听switch事件登录注册页面切换
Auth.prototype.listenSwitchEvent = function(){
    var self = this
    var switcher = $(".switch")
    switcher.click(function(){
        //获取当前位置
        var currentLeft = self.scrollWrapper.css("left")
        // 转换为整数
        currentLeft = parseInt(currentLeft)
        if(currentLeft < 0){
            self.scrollWrapper.animate({"left": "0"})
        }else{
            self.scrollWrapper.animate({"left": "-400px"})
        }
    })

}

// 监听登录按钮事件
Auth.prototype.listenSigninEvent = function(){
    var self = this
    // 获取登录盒子下的标签
    var signinGroup = $(".signin-group")
    var telephoneInput = signinGroup.find("input[name='telephone']")
    var passwordInput = signinGroup.find("input[name='password']")
    var rememberInput = signinGroup.find("input[name='remember']")

    // 点击登录事件，提取数据
    var submitBtn = signinGroup.find(".submit-btn")
    submitBtn.click(function(){
        var telephone = telephoneInput.val()
        var password = passwordInput.val()
        var remember = rememberInput.prop("checked");

        xfzajax.post({
            'url': '/account/login/',
            'data': {
                'telephone': telephone,
                'password': password,
                'remember': remember?1:0
            },
            'success': function(result){
                if(result['code'] == 200){
                    self.hideEvent()
                    window.location.reload()
                }else{
                    var messageObject = result['message']
                    if(typeof messageObject == 'string' || messageObject.constructor == String){
                        // console.log(messageObject)
                        window.messageBox.show(messageObject)
                    }else{
                        //{"meaasage":["密码长度不能超过20", "xxxx"]}
                        for(var key in messageObject){
                            var messages = messageObject[key]
                            var message = messages[0]
                            // console.log(message)
                            window.messageBox.show(message)

                        }
                    }
                }

            },
            'fail': function(error){
                console.log(error)
            }
        })
    })
}

//页面加载完毕之后进行事件
$(function(){
    var auth = new Auth()
    auth.run()
})

