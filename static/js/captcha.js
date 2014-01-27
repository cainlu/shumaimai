$(document).ready(function(){
	$('.captcha').css({'cursor':'pointer'});
    $('.captcha').click(function(){
        $.get('/account/captcha_refresh/', function(result){
            json_result = eval('(' + result + ')');
            if (json_result.state == '1'){
                $('.captcha').attr('src', json_result.new_captcha_image);
                $('#id_captcha_0').val(json_result.new_captcha_hashkey);
            }
        });
    });
});

