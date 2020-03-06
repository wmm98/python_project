
function PubCourse() {

}

PubCourse.prototype.initUEditor = function () {
    window.ue = UE.getEditor("editor",{
        'initialFrameHeight': 400,
        'serverUrl': '/ueditor/upload/'
    });
};

PubCourse.prototype.listenSubmitEvent = function () {
    var submitBtn = $("#submit-btn");


    submitBtn.click(function () {

        // event.preventDefault();
        var btn = $(this);
        var pk = btn.attr('data-course-id');

        var title = $("#title-input").val();
        var category_id = $("#category-input").val();
        var teacher_id = $("#teacher-input").val();
        // var teacher_id = $("select[name='teacher']").val();
        var video_url = $("#video-input").val();
        var cover_url = $("#cover-input").val();
        var price = $("#price-input").val();
        var duration = $("#duration-input").val();
        var profile = window.ue.getContent();



        var url = '';
        if(pk){
            url = '/cms/edit_course/';
        }else{
            url = '/cms/pub_course/';
        }

        xfzajax.post({
            'url': url,
            'data': {
                'title': title,
                'video_url': video_url,
                'cover_url': cover_url,
                'price': price,
                'duration': duration,
                'profile': profile,
                'category_id': category_id,
                'teacher_id': teacher_id,
                'pk': pk
            },
            'success': function (result) {
                if(result['code'] === 200){
                    // window.location = window.location.href;
                    if(url == '/cms/edit_course/'){
                        xfzalert.alertSuccess('课程编辑成功！',function () {
                            window.location.reload();
                        });
                    }else{
                        xfzalert.alertSuccess('恭喜！课程发表成功！',function () {
                            window.location.reload();
                        });
                    }

                }
            }
        });
    });
};

PubCourse.prototype.run = function () {
    this.initUEditor();
    this.listenSubmitEvent();
};


$(function () {
    var course = new PubCourse();
    course.run();
});