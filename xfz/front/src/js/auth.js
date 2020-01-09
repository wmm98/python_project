// 点击登录按钮， 弹出模态对话框
$(function(){
    // 弹出的对话框
    $('#btn').click(function(){
        $(".mask-wrapper").show()
    })
    $('.close-btn').click(function(){
        $('.mask-wrapper').hide()
    })
})

// 登录注册页面切换
$(function(){
    $(".switch").click(function(){
        //获取盒子的大小
        var scrollWrapper = $(".scroll-wrapper")
        //获取当前位置
        var currentLeft = scrollWrapper.css("left")
        // 转换为整数
        currentLeft = parseInt(currentLeft)
        if(currentLeft < 0){
            scrollWrapper.animate({"left": "0"})
        }else{
            scrollWrapper.animate({"left": "-400px"})
        }
    })
})