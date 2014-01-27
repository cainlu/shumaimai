function ajaxAgree(id){
	var agree = $.cookie('ad' + id + '_agree');
	if (agree) {
		shuAlert('您已点击过该选项', 2);
	}
	else{
        $.get('/advertise/advertiseagree/?id=' + id, function(result){
            jsonResult = eval('(' + result + ')');
            if (jsonResult.state == '1'){
                $('.agree' + id).html(jsonResult.text);
            }
            else if (jsonResult.state == '2'){
                shuAlert('您已点击过该选项', 2);
            }
        });
        $.cookie('ad' + id + '_agree', '1', {expires:30, path:'/' });
	}
}

function ajaxDisagree(id){
	var disagree = $.cookie('ad' + id + '_disagree');
    if (disagree) {
        shuAlert('您已点击过该选项', 2);
    }
    else{
        $.get('/advertise/advertisedisagree/?id=' + id, function(result){
            jsonResult = eval('(' + result + ')');
            if (jsonResult.state == '1'){
                $('.disagree' + id).html(jsonResult.text);
            }
            else if (jsonResult.state == '2'){
                shuAlert('您已点击过该选项', 2);
            }
        });
        $.cookie('ad' + id + '_disagree', '1', {expires:30, path:'/' });
    }
}

function messagejudge(id){
	var activity = $('#activity' + id).val();
    var context = $('#context' + id).val();
    var objectid = $('#object' + id).val();
    var message = $.cookie('ad' + objectid + '_' + activity + '_message');
    if ((context) && !(message)){
        $.post('/advertise/messageboard/', {
            objectid:objectid,
            context:context,
            activity:activity
        },
        function(result){
            jsonResult = eval('(' + result + ')');
            if (jsonResult.state == '1'){
                shuAlert('留言成功', 1);
                $('#my_message').after(jsonResult.text);
                $('#context' + id).val('');
            }
        });
        var cookieTime = new Date();
        cookieTime.setTime(cookieTime.getTime() + (10 * 60 * 1000));
        $.cookie('ad' + objectid + '_' + activity + '_message', '1', {expires:cookieTime, path:'/' });
    }
    else if(message){
    	shuAlert('10分钟内无法再次留言', 2);
    }
    else{
        shuAlert('请填写内容', 2);
        return;
    }
    
}

function advertise_url(id){
    window.location.href = '/advertise/commentshow/?advertiseid=' + id;
}

function change_time(time){
	day = parseInt(time/(24*60*60*1000));
    hour = parseInt((time-day*24*60*60*1000)/(60*60*1000));
    minute = parseInt((time-day*24*60*60*1000-hour*60*60*1000)/(60*1000));
    second = parseInt((time-day*24*60*60*1000-hour*60*60*1000-minute*60*1000)/1000);
    return day + '天' + hour + '时' + minute + '分' + second + '秒';
}

function advertise_all(activity){
    window.location.href = '/advertise/advertiseshow/?all=1&activity=' + activity;
}

function ajaxMore(activity, page){
    $.get('/advertise/moreadvertise/?activity=' + activity + '&page=' + page, function(result){
        jsonResult = eval('(' + result + ')');
        if (jsonResult.state == '1'){
            $(jsonResult.text).appendTo('#ad_downtable');
            $('#more' + page).html('');
            $('#blank' + page).css('height', '0px');
        }
        else if (jsonResult.state == '2'){
            shuAlert('您已点击过该选项', 2);
        }
    });
}