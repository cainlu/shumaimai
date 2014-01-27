
//显示卖出frame
function sellframeshow(){
	$('#footer').css("opacity", ".30");
	$('#content').css("opacity", ".30");
	$('#header').css("opacity", ".30");
	$('#fixed-frame').css("opacity", "1");
	$('.sc_up_img').css("opacity", "1");
	$('#sellframe').show();
	$('#buybehalfframe').hide();
	$('#confirmframe').hide();
}

//关闭卖出frame
function closesellframe(){
	$('#footer', window.parent.document).css("opacity", "1");
	$('#content', window.parent.document).css("opacity", "1");
	$('#header', window.parent.document).css("opacity", "1");
	$('#fixed-frame', window.parent.document).css("opacity", "1");
	$('body', window.parent.document).css("filter", "alpha(opacity=100)");
	$('#sellframe', window.parent.document).hide();
}

//卖出判断
function selljudge(){
	if (($('#sellphone').val() != '') && ($('#selladdress').val() != '')){
		var sellphone = $("#sellphone").val();
		if (!isNaN(sellphone) && (sellphone.length == 8 || sellphone.length == 11)){
			$('#sell-info').submit();
			$.cookie('phone', $('#sellphone').val(), {expires:7, path:'/' });
			$.cookie('address', $('#selladdress').val(), {expires:7, path:'/' });
			return true;
		}
		else if(isNaN(sellphone)){
			frameAlert('联系电话必须为数字');
			return false;
		}
		else if(sellphone.length != 8 && sellphone.length != 11){
            frameAlert('联系电话必须为8位或11位');
            return false;
        }
	}
	else{
		frameAlert('请填写完整信息');
		return false;
	}
}