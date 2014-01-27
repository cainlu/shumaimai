//关闭确认frame
function closeconfirmframe(){
	$('#footer', window.parent.document).css("opacity", "1");
	$('#content', window.parent.document).css("opacity", "1");
	$('#header', window.parent.document).css("opacity", "1");
	$('#fixed-frame', window.parent.document).css("opacity", "1");
	$('body', window.parent.document).css("filter", "alpha(opacity=100)");
	$('#confirmframe', window.parent.document).hide();
}

//关闭alertframe
function closealertframe(){
	if (!$('#buybehalfframe', window.parent.document).is(':visible') && !$('#sellframe', window.parent.document).is(':visible')){
		$('#footer', window.parent.document).css("opacity", "1");
		$('#content', window.parent.document).css("opacity", "1");
		$('#header', window.parent.document).css("opacity", "1");
		$('#fixed-frame', window.parent.document).css("opacity", "1");
		$('body', window.parent.document).css("filter", "alpha(opacity=100)");
	}
	$('#alertframe', window.parent.document).hide();
}

//主页面跳到我的订单
function parentorder(){
	window.parent.location.href = '/shopping/ordershow/';
}