var gulp = require("gulp")
var cssnano = require("gulp-cssnano")
var rename = require("gulp-rename")
var uglify = require("gulp-uglify")
var concat = require("gulp-concat")
var imagemin = require('gulp-imagemin')
// //将压缩的图片放进缓存里，就不用每次都压缩
var cache = require('gulp-cache')
//创建服务器
var bs = require("browser-sync").create()
var sass = require("gulp-sass")
// 引用的是压缩的文件js, 出错不好指明是哪行， 用它可以明确知道出错是哪行
var sourcemaps = require("gulp-sourcemaps")
// gulp-util：这个插件中有一个方法log, 可以打印出当前js错误信息
// 不会在运行的时候直接停止过执行
var util = require("gulp-util")


//存放所有的路径,以后修改路径的时候只需要修改一个地方
var path = {
    // **表示中间有任意多个目录
    'html': './templates/**/',
    'css': './src/css/**/',
    'js': './src/js/',
    'images': './src/images/',
    'css_dist': './dist/css/',
    'js_dist': './dist/js/',
    'images_dist': './dist/images/'

}

//处理html文件
gulp.task("html", function(){
    gulp.src(path.html + "*.html")
        .pipe(bs.stream())
})

// 定义一个css任务
gulp.task("css", function(){
    // gulp.src(path.css + '*.css')
    // 读取sass
    gulp.src(path.css + '*.scss')
        .pipe(sass().on("error", sass.logError))
        .pipe(cssnano())
        .pipe(rename({"suffix": ".min"}))
        .pipe(gulp.dest(path.css_dist))
        .pipe(bs.stream())
})


//定义处理js文件的任务
gulp.task("js", function(){
    gulp.src(path.js + "*.js")
        .pipe(sourcemaps.init())
        .pipe(uglify().on("error", util.log))
        .pipe(rename({"suffix": ".min"}))
        .pipe(sourcemaps.write())
        .pipe(gulp.dest(path.js_dist))
        .pipe(bs.stream())
})


//定义处理图片文件的任务
gulp.task('images', function(){
    gulp.src(path.images + "*.*")
        .pipe(cache(imagemin()))
        .pipe(gulp.dest(path.images_dist))
        .pipe(bs.stream())
})

//定义监听文件修改的任务
gulp.task("watch", function(){
    gulp.watch(path.html + "*.html", ['html'])
    gulp.watch(path.css + "*.scss", ['css'])
    gulp.watch(path.js + "*.js", ['js'])
    gulp.watch(path.images + "*.*", ['images'])
})

//初始化browser-sync的任务
gulp.task("bs", function(){
    bs.init({
        'server': {
            "baseDir": './'
        }
    })
})

//创建一个默认任务
// gulp.task("default", ["bs", "watch"])

//只进行监听任务，并不会打开浏览器刷新
gulp.task("default", ["watch"])