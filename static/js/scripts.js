/*!
* Start Bootstrap - Coming Soon v6.0.5 (https://startbootstrap.com/theme/coming-soon)
* Copyright 2013-2021 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-coming-soon/blob/master/LICENSE)
*/
// This file is intentionally blank
// Use this file to add JavaScript to your project
$("#submitBut").click(function () {
    var a = $("#emails").val().toString()
    console.log(a)
    $.ajax({
        type: 'POST',
        url: '/',
        data: { 'data': a },
        success: function (data) {
            if (data['type'] == 1) {
                location.href = a;
            }
            else if (data['type'] == 2) {
                location.href = a;
            }
            else if(a==""){
                location.href = data['type'];
            }
            else {
                $('#errormsg').text("不好意思，这个id还没有收录，已经紧急加到队列里啦，五分钟之后再来看看吧🎆~")
            }
        },
        error: function (event) {
            console.log(event.responseText);
        },
        dataType: 'json'
    });
})