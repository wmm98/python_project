function News() {
    this.progressGroup = $("#progress-group");
}


News.prototype.listenUploadFielEvent = function () {
    var uploadBtn = $('#thumbnail-btn');
    uploadBtn.change(function () {
        var file = uploadBtn[0].files[0]
        // console.log(file.name);
        var formData = new FormData();
        formData.append('file',file);
        xfzajax.post({
            'url': '/cms/upload_file/',
            'data': formData,
            'processData': false,
            'contentType': false,
            'success': function (result) {
                if(result['code'] === 200){
                    // var url = result['data']['url'];
                    var url = file.name
                    console.log(url)
                    var thumbnailInput = $("#thumbnail-form");
                    thumbnailInput.val(url);
                }
            }
        });
    });
};

News.prototype.listenQiniuUploadFileEvent = function () {
    var self = this;
    var uploadBtn = $('#thumbnail-btn');
    uploadBtn.change(function () {
        var file = this.files[0];
        xfzajax.get({
            'url': '/cms/qntoken/',
            'success': function (result) {
                if(result['code'] === 200){
                    var token = result['data']['token'];
                    // a.b.jpg = ['a','b','jpg']
                    // 198888888 + . + jpg = 1988888.jpg
                    var key = (new Date()).getTime() + '.' + file.name.split('.')[1];
                    var putExtra = {
                        fname: key,
                        params:{},
                        mimeType: ['application/pdf']
                    };
                    var config = {
                        useCdnDomain: true,
                        retryCount: 6,
                        region: qiniu.region.z2
                    };
                    var observable = qiniu.upload(file,key,token,putExtra,config);
                    observable.subscribe({
                        'next': self.handleFileUploadProgress,
                        'error': self.handleFileUploadError,
                        'complete': self.handleFileUploadComplete
                    });
                }
            }
        });
    });
};

News.prototype.handleFileUploadProgress = function (response) {
    var total = response.total;
    var percent = total.percent;
    var percentText = percent.toFixed(0)+'%';
    // 24.0909，89.000....
    var progressGroup = News.progressGroup;
    progressGroup.show();
    var progressBar = $(".progress-bar");
    progressBar.css({"width":percentText});
    progressBar.text(percentText);
};

News.prototype.handleFileUploadError = function (error) {
    window.messageBox.showError(error.message);
    var progressGroup = $("#progress-group");
    progressGroup.hide();
    console.log(error.message);
};

News.prototype.handleFileUploadComplete = function (response) {
    console.log(response);
    var progressGroup = $("#progress-group");
    progressGroup.hide();

    var domain = 'q5jl6xwjh.bkt.clouddn.com/';
    var filename = response.key;
    var url = domain + filename;
    var thumbnailInput = $("input[name='thumbnail']");
    thumbnailInput.val(url);
};

News.prototype.listenSubmitEvent = function () {
    var submitBtn = $("#submit-btn");
    submitBtn.click(function (event) {
        event.preventDefault();
        var btn = $(this);
        var pk = btn.attr('data-payinfo-id');

        var title = $("input[name='title']").val();
        var profile = $("input[name='desc']").val();
        var path = $("input[name='thumbnail']").val();
        var price = $("input[name='price']").val();

        var url = '';
        if(pk){
            url = '/cms/edit_payinfo/';
        }else{
            url = '/cms/pay_info/';
        }

        xfzajax.post({
            'url': url,
            'data': {
                'title': title,
                'price': price,
                'profile': profile,
                'path': path,
                'pk': pk
            },
            'success': function (result) {
                if(result['code'] === 200){
                    if(url == '/cms/pay_info/'){
                        xfzalert.alertSuccess('恭喜！资讯发表成功！',function () {
                            window.location.reload();
                        });
                    }else{
                        xfzalert.alertSuccess('恭喜！资讯编辑成功！',function () {
                            window.location.reload();
                        });
                    }

                }
            }
        });
    });
};

News.prototype.run = function () {
    var self = this;
    // self.listenQiniuUploadFileEvent();
    self.listenSubmitEvent();
    self.listenUploadFielEvent();
};


$(function () {
    var news = new News();
    news.run();

    News.progressGroup = $('#progress-group');
});