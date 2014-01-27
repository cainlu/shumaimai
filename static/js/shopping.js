//减少购买数量
function buynummin(){
	var tmpnum = $('#booknum0').val() * 1;
	if(!(isNaN($('#booknum0').val())) && tmpnum > 1){
		$('#booknum0').val(tmpnum - 1);
	}
	else{
		shuAlert('请输入1-99之间的整数', 2);
	}
}

//增加购买数量
function buynumadd(){
	var tmpnum = $('#booknum0').val() * 1;
	if(!(isNaN($('#booknum0').val())) && (tmpnum < 99)){
		$('#booknum0').val(tmpnum + 1);
	}
	else{
		shuAlert('请输入1-99之间的整数', 2);
	}
}

//取消url代购
function urldel(i, url){
	$.cookie('urlbuynum' + i, 0, {path:'/' });
	shoppingCarShow(url);
}

//取消书名代购
function bookbehalfdel(i, url){
	$.cookie('bookbuynum' + i, 0, {path:'/' });
	shoppingCarShow(url);
}

//显示代购frame
function buybehalfframeshow(){
	$('#footer').css("opacity", ".30");
	$('#content').css("opacity", ".30");
	$('#header').css("opacity", ".30");
	$('#fixed-frame').css("opacity", "1");
	$('.sc_up_img').css("opacity", "1");
	$('#buybehalfframe').show();
	$('#sellframe').hide();
	$('#confirmframe').hide();
}

//关闭代购frame
function closebuybehalfframe(){
	$('#footer', window.parent.document).css("opacity", "1");
	$('#content', window.parent.document).css("opacity", "1");
	$('#header', window.parent.document).css("opacity", "1");
	$('#fixed-frame', window.parent.document).css("opacity", "1");
	$('body', window.parent.document).css("filter", "alpha(opacity=100)");
	$('#buybehalfframe', window.parent.document).hide();
}

//书名代购判断
function bookbehalfjudge(){
	var buystate = $.cookie('buystate');
	if (buystate == '1'){
		cookieclear();
	}
	var bookname = $('#bookname').val();
	var bookauthor = $('#bookauthor').val();
	var bookpublisher = $('#bookpublisher').val();
	var bookisbn = '';
	var bookurl = $('#bookurl').val();
	var booknum = $('#booknum').val() * 1;
	if (!isNaN($('#booknum').val()) && booknum > 0 && booknum <= 99){
		if ((bookname == '') || (bookauthor == '')){
			frameAlert('请填写完整信息');
			return;
		}
		else{
			if (bookbehalf(bookname, bookauthor, bookpublisher, bookisbn, bookurl, booknum)){
				$('#behalftable').append('<tr><td style="text-align:center;">\
				' + bookname + '</td><td style="text-align:center;">' + bookauthor + '\
				</td><td style="text-align:center;">' + booknum + '</td></tr>');
			}
		}
	}
	else{
		frameAlert('购买数量在0-99之间');
		$('#booknum').val('');
		return;
	}
}

//书名代购
function bookbehalf(bookname, bookauthor, bookpublisher, bookisbn, bookurl, booknum){
	var totalnum = $.cookie('bookbehalftotalnum') * 1;
	if (totalnum >= 0){
		for(var i = 0; i < totalnum; i++) {
			var tmpname = $.cookie('bookbehalfname' + i);
			var tmpauthor = $.cookie('bookbehalfauthor' + i);
			var tmppublisher = $.cookie('bookbehalfpublisher' + i);
			var tmpisbn = $.cookie('bookbehalfisbn' + i);
			var tmpurl = $.cookie('bookbehalfurl' + i);
			var tmpnum = $.cookie('bookbehalfnum' + i) * 1;
			if((tmpname == bookname) && (tmpauthor == bookauthor) && (tmppublisher == bookpublisher) && (tmpisbn == bookisbn) && (tmpurl == bookurl)) {
				if(tmpnum + booknum < 100){
					frameAlert2("放入购物车成功");
					$.cookie('bookbehalfnum' + i, tmpnum + booknum, {path:'/' });
					$('#bookname').val('');
					$('#bookauthor').val('');
					$('#bookpublisher').val('');
					$('#bookisbn').val('');
					$('#bookurl').val('');
					$('#booknum').val('');
					return true;
				}
				else{
					frameAlert('购买数量在0-99之间');
					return false;
				}
			}
		}
		frameAlert2("放入购物车成功");
		$.cookie('bookbehalfname' + totalnum, bookname, {path:'/' });
		$.cookie('bookbehalfauthor' + totalnum, bookauthor, {path:'/' });
		$.cookie('bookbehalfpublisher' + totalnum, bookpublisher, {path:'/' });
		$.cookie('bookbehalfisbn' + totalnum, bookisbn, {path:'/' });
		$.cookie('bookbehalfurl' + totalnum, bookurl, {path:'/' });
		$.cookie('bookbehalfnum' + totalnum, booknum, {path:'/' });
		$.cookie('bookbehalftotalnum', totalnum + 1, {path:'/' });
		$('#bookname').val('');
		$('#bookauthor').val('');
		$('#bookpublisher').val('');
		$('#bookisbn').val('');
		$('#bookurl').val('');
		$('#booknum').val('');
		return true;
	}
	else{
		frameAlert2("放入购物车成功");
		$.cookie('bookbehalfname0', bookname, {path:'/' });
		$.cookie('bookbehalfauthor0', bookauthor, {path:'/' });
		$.cookie('bookbehalfpublisher0', bookpublisher, {path:'/' });
		$.cookie('bookbehalfisbn0', bookisbn, {path:'/' });
		$.cookie('bookbehalfurl0', bookurl, {path:'/' });
		$.cookie('bookbehalfnum0', booknum, {path:'/' });
		$.cookie('bookbehalftotalnum', 1, {path:'/' });
		$('#bookname').val('');
		$('#bookauthor').val('');
		$('#bookpublisher').val('');
		$('#bookisbn').val('');
		$('#bookurl').val('');
		$('#booknum').val('');
		return true;
	}
}

//购买
function cookiebuy(counter){
	var buystate = $.cookie('buystate');
	if (buystate == '1'){
		cookieclear();
	}
	var counternum = '#booknum' + counter;
	var counterid = '#bookid' + counter;
	var countername = '#bookname' + counter;
	var counterauthor = '#bookauthor' + counter;
	var counterprice = '#bookprice' + counter;
	var counterpublisher = '#bookpublisher' + counter;
	var counterisbn = '#bookisbn' + counter;
	var num = $(counternum).val();
	if (!isNaN(num) && num > 0 && num < 100) {
		var bookid = $(counterid).val() * 1;
		var bookname = $(countername).val();
		var bookauthor = $(counterauthor).val();
		var bookprice = $(counterprice).val();
		var bookpublisher = $(counterpublisher).val();
		var bookisbn = $(counterisbn).val();
		var booknum = num * 1;
		var typenum = $.cookie('typenum') * 1;
		if (typenum >= 0){
			for(var i = 0; i < typenum; i++) {
				var tmpid = $.cookie('bookid' + i) * 1;
				var tmpname = $.cookie('bookname' + i);
				var tmpauthor = $.cookie('bookauthor' + i);
				var tmpprice = $.cookie('bookprice' + i);
				var tmppublisher = $.cookie('bookpublisher' + i);
				var tmpisbn = $.cookie('bookisbn' + i);
				var tmpnum = $.cookie('booknum' + i) * 1;
				if(tmpid == bookid) {
					if(tmpnum + booknum < 100){
						scAni2();
						$.cookie('booknum' + i, tmpnum + booknum, {path:'/' });
						return true;
					}
					else{
						shuAlert('购买总量不得超过99', 2);
						return false;
					}
				}
			}
			scAni2();
			$.cookie('bookid' +typenum , bookid, {path:'/' });
			$.cookie('bookname' +typenum , bookname, {path:'/' });
			$.cookie('bookauthor' +typenum , bookauthor, {path:'/' });
			$.cookie('bookprice' +typenum , bookprice, {path:'/' });
			$.cookie('bookpublisher' +typenum , bookpublisher, {path:'/' });
			$.cookie('bookisbn' +typenum , bookisbn, {path:'/' });
			$.cookie('booknum' +typenum , booknum, {path:'/' });
			$.cookie('typenum', typenum + 1, {path:'/' });
			return true;
		}
		else{
			scAni2();
			$.cookie('bookid0', bookid, {path:'/' });
			$.cookie('bookname0', bookname, {path:'/' });
			$.cookie('bookauthor0', bookauthor, {path:'/' });
			$.cookie('bookprice0', bookprice, {path:'/' });
			$.cookie('bookpublisher0', bookpublisher, {path:'/' });
			$.cookie('bookisbn0', bookisbn, {path:'/' });
			$.cookie('booknum0', booknum, {path:'/' });
			$.cookie('typenum', 1, {path:'/' });
			return true;
		}
	}
	else{
		shuAlert('请输入1-99之间的整数', 2);
		return false;
	}
}

function scAni2() {
	shuAlert("放入购物车成功", 1);
	//scLight();
	if ($('#fixed-frame-second').is(':visible')){
		$('#fixed-frame-second').slideToggle('fast');
	}
	return;
}
