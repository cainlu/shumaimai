//下订单
function order(maxscore){
	if (orderjudge(maxscore)){
		$("#order-info").submit();
		var phone = $('#tmpphone').val();
		var address = $('#tmpaddress').val();
		$.cookie('phone', phone, {expires:7, path:'/' });
		$.cookie('address', address, {expires:7, path:'/' });
		$.cookie('buystate', '1', {expires:7, path:'/' });
	}
}

//下订单判断
function orderjudge(maxscore){
	var phone = $('#tmpphone').val();
	var address = $('#tmpaddress').val();
	var remark = $('#tmpremark').val();
	var score = $('#tmpscore').val();
	var price = $('#totalPrice').text();
	if (maxscore == -1){
		maxscore = 0;
	}
	if(address == ''){
        shuAlert('收货地址不能为空', 2);
        return false;
    }
	else if(isNaN(phone)){
		shuAlert('联系电话必须为数字', 2);
		return false;
	}
	else if(phone.length != 8 && phone.length != 11){
        shuAlert('联系电话必须为8位或11位', 2);
        return false;
    }
	else if(isNaN(score)){
        shuAlert('使用积分必须为数字', 2);
        return false;
    }
    else if(score * 1 > maxscore){
        shuAlert('积分不足', 2);
        return false;
    }
    else if(price * 1 < 0){
    	shuAlert('使用积分过多', 2);
        return false;
    }
    else{
        return true;
    }
}

//清除cookie
function cookieclear(){
	var typenum = $.cookie('typenum') * 1;
	var urlbehalftotalnum = $.cookie('urlbehalftotalnum') * 1;
	var bookbehalfnum = $.cookie('bookbehalftotalnum') * 1;
	for(var i = 0; i < typenum; i++) {
		$.cookie('bookid' + i, null, {path:'/' });
		$.cookie('bookname' + i, null, {path:'/' });
		$.cookie('bookauthor' + i, null, {path:'/' });
		$.cookie('bookprice' + i, null, {path:'/' });
		$.cookie('booknum' + i, null, {path:'/' });
	}
	$.cookie('typenum', null, {path:'/' });
	for(var i = 0; i < urlbehalftotalnum; i++) {
		$.cookie('url' + i, null, {path:'/' });
		$.cookie('urlbehalfnum' + i, null, {path:'/' });
	}
	$.cookie('urlbehalftotalnum', null, {path:'/' });
	for(var i = 0; i < bookbehalfnum; i++) {
		$.cookie('bookbehalfname' + i, null, {path:'/' });
		$.cookie('bookbehalfauthor' + i, null, {path:'/' });
		$.cookie('bookbehalfpublisher' + i, null, {path:'/' });
		$.cookie('bookbehalfisbn' + i, null, {path:'/' });
		$.cookie('bookbehalfnum' + i, null, {path:'/' });
	}
	$.cookie('bookbehalftotalnum', null, {path:'/' });
	$.cookie('buystate', null, {path:'/' });
	shoppingCarShow('/static/');
}

//取消订单
function cancelorder(dealid, event){
	$.get('/shopping/cancelorder/?dealid=' + dealid, function(result){
		jsonResult = eval('(' + result + ')');
		if (jsonResult.state == '1'){
			$('#statustd' + dealid).html('取消');
			shuAlert('订单取消成功', 1);
		}
	});
}