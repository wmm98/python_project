
function CMSNewsList() {

}

CMSNewsList.prototype.listenDeleteEvent = function () {
    var deleteBtns = $(".delete-btn");
    deleteBtns.click(function () {
        var btn = $(this);
        var staff_id = btn.attr('data-staff-id');
        xfzalert.alertConfirm({
            'text': '您是否要删除该员工？',
            'confirmCallback': function () {
                xfzajax.post({
                    'url': '/cms/delete_staff/',
                    'data': {
                        'staff_id': staff_id
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