
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

}

Banner.prototype.run = function(){
    // 获取所有id=banner-ul的元素
    var bannerUl = $("#banner-ul")
    // 修改left值，一步到位，再次打开网页的时候还是该图片而不是原本的第一张
    // 不适合
    // bannerUl.css({"left": -798})

    // 产生动画效果, 还可以指定过度时间，500毫秒
    bannerUl.animate({"left": -798}, 500)
}

// 全部文本执行之后再执行此代码
$ (function(){
    var banner = new Banner()
    banner.run()
})