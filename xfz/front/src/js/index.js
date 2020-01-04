
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
    this.bannerWidth = 798
    // 监听轮播图
    this.bannerGroup = $("#banner-group")
    //每次改变的时候就会保存，如果只是在下面的方法定义不在此定义的话，每次都会从第一个图开始循环
    this.index = 1

    //直接定义left-arrow
    this.leftArrow = $('.left-arrow')
    this.rightArrow = $('.right-arrow')

    //获取banner-ul下有多少个li标签，即多少个图片，不用写死
    this.bannerUl = $("#banner-ul")
    this.liList = this.bannerUl.children("li")
    this.bannerCount = this.liList.length
    this.pageControl = $(".page-control")



}

// js动态修改轮播图
Banner.prototype.initBanner = function(){
    var self = this
    var firstBanner = self.liList.eq(0).clone()
    var lastBanner = self.liList.eq(self.bannerCount-1).clone()
    self.bannerUl.append(firstBanner)
    self.bannerUl.prepend(lastBanner)
    // 修改css样式
    self.bannerUl.css({"width": self.bannerWidth*(self.bannerCount+2),
    'left': -self.bannerWidth})

}


// 根据轮播图的个数动态修改小圆点的结构和样式
Banner.prototype.initPageControl = function(){
    var self = this;

    for (var i = 0; i<self.bannerCount; i++ ){
        // 动态生成li标签，小点点
        var circle = $("<li></li>")
        self.pageControl.append(circle)
        if(i == 0){
            // 给css增加属性，第一个白色填充
            circle.addClass("active")
        }

    }
    // 动态修改小圆点样式
    self.pageControl.css({"width": self.bannerCount*12 + 8*2 + 16*(self.bannerCount - 1)})
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

// 重复利用轮播图
Banner.prototype.animate = function() {
    var self = this
    self.bannerUl.animate({"left": -798 * self.index}, 500)
    var index = self.index
    if (index == 0){
        index = self.bannerCount-1
    }else if(index == self.bannerCount+1){
        index = 0

    }else{
        index = self.index - 1
    }
    self.pageControl.children('li').eq(index).addClass("active").siblings().
    removeClass('active')

}

//计时器
Banner.prototype.loop = function(){
    // 在此定义的this表示Banner类,在改类的方法中调用类属性
    var self = this

    // 获取所有id=banner-ul的元素
    // var bannerUl = $("#banner-ul")
    // 修改left值，一步到位，再次打开网页的时候还是该图片而不是原本的第一张
    // 不适合
    // bannerUl.css({"left": -798})

    // 产生动画效果, 还可以指定过度时间，500毫秒
    // bannerUl.animate({"left": -798}, 500)

    // 根据下标轮播
    // var index = 0
    // 计时器，把需要执行的函数放进去即可
    this.timer = setInterval(function () {
        if (self.index >= self.bannerCount + 1){
            self.bannerUl.css({"left":-self.bannerWidth})
            self.index = 2
        }else{
            self.index ++
        }
        self.animate()
    }, 2000) //2秒轮播一次

}

// 点击箭头上下切换图片
Banner.prototype.listenArrowClick = function (){
    var self = this
    // 点击左箭头
    self.leftArrow.click(function (){
        if(self.index == 0){
            // ==：1==‘1’返回true
            //====: 1 != '1' false 1==1 true
            self.bannerUl.css({"left":-self.bannerCount*self.bannerWidth})
            self.index = self.bannerCount - 1
        }else{
            self.index--
        }
        // 条件满足就实现轮播
        self.animate()
    })

    // 右边
    self.rightArrow.click(function (){
        if(self.index == self.bannerCount + 1){
            self.bannerUl.css({"left":-self.bannerWidth})
            self.index = 2
        }else{
            self.index++
        }
        // 条件满足就实现轮播
        self.animate()
    })

}


//小圆点的轮播
Banner.prototype.listenPageControl = function(){
    var self = this
    self.pageControl.children("li").each(function(index, obj){
        $(obj).click(function(){
            self.index = index
            //移除没有选中的圆点状态
            $(obj).addClass("active").siblings().removeClass("active")
            self.animate()
        })
    })
}

Banner.prototype.run = function () {
    console.log("running")
    this.initPageControl()
    this.initBanner()
    this.loop()
    this.listenArrowClick()
    // 一但对象被初始化之后就监听banner
    this.listenBannerHover()
    this.listenPageControl()


}

// 全部文本执行之后再执行此代码
$ (function(){
    var banner = new Banner()
    banner.run()
})