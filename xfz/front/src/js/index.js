
//面向对象方式
// 1.添加属性
// 通过this关键字，绑定属性，并指定他的值

// 原型链
// 2.添加方法
// Banner.prototype.greet = function (word){
//     console.log("hello", word)
// }



// function Banner() {
//     // 这里面写的代码相当于python中的__init__方法的代码
//     console.log('构造函数')
//     this.person = "zhiliao"
//
// }
//
// Banner.prototype.greet = function (word){
//     console.log("hello", word)
// }
//
// var banner = new Banner()
// console.log(banner.person)
// banner.greet("zhiliao")


// 控制轮播图
function Banner(){
    // 监听轮播图
    this.bannerGroup = $("#banner-group")
    //每次改变的时候就会保存，如果只是在下面的方法定义不在此定义的话，每次都会从第一个图开始循环
    this.index = 0
    // 一但对象被初始化之后就监听banner

    //直接定义left-arrow
    this.leftArrow = $('.left-arrow')
    this.rightArrow = $('.right-arrow')
    this.listenBannerHover()

}

// 控制左右箭头是否需要隐藏，鼠标移动到图片区域就显示，否则隐藏
Banner.prototype.toggleArrow = function (isShow) {
    var self = this
    if (isShow){
        // 直接调用show方法
        // $('.left-arrow').show()
        // $('.right-arrow').show()

        //优化方法
        // 但是这样做的话每次移动进出都要寻找left-arrow right-arrow，消耗时间
        // 可以直接在类中定义，方法中直接调用就好
        self.leftArrow.show()
        self.rightArrow.show()
    }else{
        // $('.left-arrow').hide()
        // $('.right-arrow').hide()

        //优化之后
        self.leftArrow.hide()
        self.rightArrow.hide()
    }
}

// 监听鼠标移动事件
Banner.prototype.listenBannerHover = function () {
    // this表示Banner类,
    var self = this
    // 鼠标移动事件
    this.bannerGroup.hover(function () {
        //第一个函数是， 把鼠标移动到banner上会执行的函数
        // 停止轮播图，停止执行 timer
        clearInterval(self.timer)
        //显示左右箭头
        self.toggleArrow(true)

    }, function (){
        //第二个函数是， 把鼠标从banner上移走会执行的函数
        self.loop()
        // 隐藏左右箭头
        self.toggleArrow(false)
    })
}

Banner.prototype.loop = function(){
    // 在此定义的this表示Banner类,在改类的方法中调用类属性
    var self = this

    // 获取所有id=banner-ul的元素
    var bannerUl = $("#banner-ul")
    // 修改left值，一步到位，再次打开网页的时候还是该图片而不是原本的第一张
    // 不适合
    // bannerUl.css({"left": -798})

    // 产生动画效果, 还可以指定过度时间，500毫秒
    // bannerUl.animate({"left": -798}, 500)

    // 根据下标轮播
    // var index = 0
    // 计时器，把需要执行的函数放进去即可
    this.timer = setInterval(function () {
        if (self.index >= 3){
            self.index = 0
        }else{
            self.index += 1
        }
        bannerUl.animate({"left": -798 * self.index}, 500)
    }, 2000) //2秒轮播一次

}


Banner.prototype.run = function () {
    console.log("running")
    this.loop()

}

// 全部文本执行之后再执行此代码
$ (function(){
    var banner = new Banner()
    banner.run()
})