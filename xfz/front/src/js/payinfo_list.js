
function CMSNewsList() {

}

CMSNewsList.prototype.listenDeleteEvent = function () {
    var deleteBtns = $(".delete-btn");
    deleteBtns.click(function () {
        var btn = $(this);
        var payinfo_id = btn.attr('data-payinfo-id');
        xfzalert.alertConfirm({
            'text': '您是否要删除改资讯吗？',
            'confirmCallback': function () {
                xfzajax.post({
                    'url': '/cms/delete_payinfo/',
                    'data': {
                        'payinfo_id': payinfo_id
                    },
                    'success': function (result) {
                        if(result['code'] === 200){
                            window.location = window.location.href;
                            // window.location.reload()
                        }
                    }
                });
            }
        });
    });
};


CMSNewsList.prototype.run = function () {
    this.listenDeleteEvent();
};

$(function () {
    var newsList = new CMSNewsList();
    newsList.run();
});