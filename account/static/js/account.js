$(document).ready(function() {

    $.fn.changeBackgroundImage = function(imageURL) {
        $(this).css('background-image', 'url(' + imageURL + ')');
    }


    function login(){
        $('#login-dialog').dialog('open');
        $("#login-dialog").dialog({
            resizable: true,
            autoOpen:true,
            modal: true,
            title:"用户信息",
            buttons: {
                '提交': function() {
                    $(this).dialog('close');
                    $("#login").submit();
                },
                '取消': function() {
                    $(this).dialog('close');
                }
            }
        });
    }
});



