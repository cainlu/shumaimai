//购物车显示
function shoppingCarShow(url){
	var buystate = $.cookie('buystate');
	var csrftoken = $.cookie('csrftoken');
	if (buystate == '1'){
		cookieclear();
	}
	var totalShow = '';
	totalShow += bookBuyShow(url);
	totalShow += bookBehalfShow(url);
	//totalShow += urlBehalfShow(url);
	if (totalShow == ''){
		totalShow = '<div class="ff-shopping-cart-detail">\
						<div id="sc-blank">\
							<label id="sc-blank1">还不赶快挑本自己需要的书？！~~~~@╮(╯▽╰)╭@</label>\
						</div>\
					</div>';
	}
	else{
		totalShow = '<div class="ff-shopping-cart-detail" onclick="event.cancelBubble=true;">\
						<table class="ff-sc-detail-table">\
							<tr>\
								<th width="5"/>\
								<th class="bottomline first-td" width="30%">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;书名</th>\
								<th class="bottomline first-td" width="15%">作者</th>\
								<th class="bottomline" width="10%">单价</th>\
								<th class="bottomline" width="15%">数量</th>\
								<th class="bottomline" width="10%">总价</th>\
								<th class="bottomline" width="10%"><span id="clearfont" onClick="cookieclear()">清空</span></th>\
								<th width="5"/>\
							</tr>' + totalShow + '</table></div>';;
	totalShow += '<div class="order-line" id="order-line1" onclick="event.cancelBubble=true;"><br>\
					  &nbsp;&nbsp;&nbsp;共<font size=4 color="red">' + sumBook()[0] + '</font>本\
					  &nbsp;&nbsp;&nbsp;应付总额<font size=4 color="red" id="totalPrice">' + sumBook()[1] + '</font>元&nbsp;&nbsp;&nbsp;\
					  <br><label id="behalf-message">（不包含代购图书价格）</label>&nbsp;&nbsp;&nbsp;\
				  </div>\
                  <form id="order-info" method="post" action="/shopping/order/">\
                  <input type="hidden" name="csrfmiddlewaretoken" value="' + csrftoken + '"/>\
				  <div class="order-line" id="order-line2" onclick="event.cancelBubble=true;">\
 					  <br><label class="carlabel">&nbsp;&nbsp;联系电话<sup><font color="red">*</font></sup></label>\
					  <input type="text" id="tmpphone" name="phone" style="width:30%;float:left;"/>\
					  <label class="carlabel">&nbsp;&nbsp;收货地址<sup><font color="red">*</font></sup></label>\
					  <input type="text" id="tmpaddress" name="address" style="width:30%;float:left;" placeholder="例如：上海海事大学42号楼"/>\
					  <font size=2 style="float:left;left:12%;padding:0 50px 0 43px;">支付方式：货到付款</font><br><br>\
				  </div>\
				  <div class="order-line" id="order-line3" onclick="event.cancelBubble=true;">\
					  <label class="carlabel">&nbsp;&nbsp;备注</label>\
					  <textarea id="tmpremark" name="remark" style="width:30%;height:35px;float:left;"/>'
	var score = $.cookie('score');
	if (score >= 0){
		totalShow += '<label class="carlabel">&nbsp;&nbsp;使用积分</label>\
                      <input type="text" id="tmpscore" name="score" style="width:10%;float:left;" value="0"/>\
                      <label class="carlabel" style="width:20%;">&nbsp;&nbsp;(剩余积分点数：<span id="myScore">' + score.toString() + '</span>)</label>'
                      //<img src="/static/image/sc_score.png" id="sc_score_img"></img>
	}
	else if (score == -1){
		totalShow += '<label class="carlabel" id="unregister-label">&nbsp;&nbsp;会员独享积分服务，抵现金，让买卖书更划算！</label>\
                      <input type="hidden" id="tmpscore" name="score" value="0"/>\
                      <a href="/account/login/" class="sc-a">登陆</a>&nbsp;&nbsp;\
                      <a href="/account/register/" class="sc-a">注册</a>'
	}
	totalShow += '</form><button type="button" id="shoppingbuttonsmall" onClick = "order(' + score + ')">确认订单</button>\
				  <span id="continuefont" onClick="continuebuy()">继续购物</span><br><br>\
			  </div>';
	}
	$('#fixed-frame-second').html(totalShow);
}

//书籍购买购物车显示
function bookBuyShow(url){
	var typenum = $.cookie('typenum') * 1;
	var imgurl = url + 'image/cancel.png';
	var ffnum = '';
	var carString = '';
	var not0 = 0;
	carString = '';
	if (typenum >= 0){
		for(var i = 0; i < typenum; i++) {
			var tmpid = $.cookie('bookid' + i);
			var tmpname = $.cookie('bookname' + i);
			var tmpauthor = $.cookie('bookauthor' + i);
			var tmpprice = $.cookie('bookprice' + i);
			var tmpnum = $.cookie('booknum' + i) * 1;
			if (tmpnum != 0){
				not0++;
				ffnum = 'ff-sc-detail-num' + i;
				carString += '' +
						'<tr class="' + getTableLineClass(i+1) + '">\
							<td/>\
							<td class="first-td">\
								<span>' + tmpname + '</span>\
							</td>\
							<td class="first-td">\
								<span>' + tmpauthor + '</span>\
							</td>\
							<td>&#65509;' + tmpprice + '</td>\
							<td class="num-wrapper">\
								<button class="numbutton" onClick="nummin(' + i + ', ' + url + ', 1)">—</button>\
								<input style="width:60px;" id="' + ffnum + '" value="' + tmpnum + '" class="num1 num" maxlength=2></input>\
								<button class="numbutton" onClick="numadd(' + i + ', ' + url + ', 1)">+</button>\
							</td>\
							<td>&#65509;' + (tmpprice*tmpnum).toFixed(2) + '</td>\
							<td>\
								<img id="ff-sc-delete" style="cursor:pointer;" \
								src="' + imgurl + '" onClick="bookdel(' + i + ', ' + url + ', 1);"/>\
							</td>\
							<td/>\
						</tr>';
			}
		}
	}
	if (not0 > 0){
		return carString;
	}
	else{
		return '';
	}
}

//书名代购购物车显示
function bookBehalfShow(url){
	var bookbehalftotalnum = $.cookie('bookbehalftotalnum') * 1;
	var imgurl = url + 'image/cancel.png';
	var ffnum = '';
	var carString = '';
	var not0 = 0;
	carString = '';
	if (bookbehalftotalnum >= 0){
		for(var i = 0; i < bookbehalftotalnum; i++) {
			var tmpname = $.cookie('bookbehalfname' + i);
			var tmpauthor = $.cookie('bookbehalfauthor' + i);
			var tmppublisher = $.cookie('bookbehalfpublisher' + i);
			var tmpisbn = $.cookie('bookbehalfisbn' + i);
			var tmpnum = $.cookie('bookbehalfnum' + i) * 1;
			if (tmpnum != 0){
				not0++;
				ffnum = 'ff-sc-detail-num-book' + i;
				carString += '' +
						'<tr class="' + getTableLineClass(i+1) + '">\
							<td/>\
							<td class="first-td">\
								<span>' + tmpname + '（代购）</span>\
							</td>\
							<td class="first-td">\
								<span>' + tmpauthor + '</span>\
							</td>\
							<td>\
								<span>—</span>\
							</td>\
							<td>\
								<button class="numbutton" onClick="nummin(' + i + ', ' + url + ', 3)">—</button>\
								<input style="width:60px;" id="' + ffnum + '" value="' + tmpnum + '" class="num3 num" maxlength=2></input>\
								<button class="numbutton" onClick="numadd(' + i + ', ' + url + ', 3)">+</button>\
							</td>\
							<td>\
								<span>—</span>\
							</td>\
							<td>\
								<img id="ff-sc-delete" style="cursor:pointer;" src="' + imgurl + '" \
								onClick="bookdel(' + i + ', ' + url + ', 3);"/>\
							</td>\
							<td/>\
						</tr>';
			}
		}
	}
	if (not0 > 0){
		return carString;
	}
	else{
		return '';
	}
}

//计算书本总量、总价
function sumBook(){
	var sumNum = 0;
	var sumPrice = 0;
	var typenum = $.cookie('typenum') * 1;
	if (typenum >= 0){
		for(var i = 0; i < typenum; i++) {
			var tmpnum = $.cookie('booknum' + i) * 1;
			var tmpprice = $.cookie('bookprice' + i);
			sumNum += tmpnum;
			sumPrice += parseFloat((tmpprice*tmpnum).toFixed(2))
		}
	}
	var urlnum = $.cookie('urlbehalftotalnum') * 1;
	if (urlnum >= 0){
		for(var i = 0; i < urlnum; i++) {
			var tmpnum = $.cookie('urlbehalfnum' + i) * 1;
			sumNum += tmpnum;
		}
	}
	var bookbehalfnum = $.cookie('bookbehalftotalnum') * 1;
	if (bookbehalfnum >= 0){
		for(var i = 0; i < bookbehalfnum; i++) {
			var tmpnum = $.cookie('bookbehalfnum' + i) * 1;
			sumNum += tmpnum;
		}
	}
	sumPrice = sumPrice.toFixed(2)
	return [sumNum, sumPrice];
}

//减少按钮
function nummin(i, url, type){
	var tmpphone = $('#tmpphone').val();
	var tmpaddress = $('#tmpaddress').val();
	if(type == 1){
		var tmpnum = $.cookie('booknum' + i) * 1;
		if(tmpnum >= 1){
			$('#ff-sc-detail-num' + i).val($('#ff-sc-detail-num' + i).val() * 1 - 1)
			$.cookie('booknum' + i, tmpnum-1, {path:'/' });
			shoppingCarShow(url);
			$('#tmpphone').val(tmpphone);
			$('#tmpaddress').val(tmpaddress);
		}
		else{
			shuAlert('请输入1-99之间的整数', 2);
		}
	}
	else if(type == 2){
		var tmpnum = $.cookie('urlbehalfnum' + i) * 1;
		if(tmpnum >= 1){
			$('#ff-sc-detail-num-url' + i).val($('#ff-sc-detail-num-url' + i).val() * 1 - 1)
			$.cookie('urlbehalfnum' + i, tmpnum-1, {path:'/' });
			shoppingCarShow(url);
			$('#tmpphone').val(tmpphone);
			$('#tmpaddress').val(tmpaddress);
		}
		else{
			shuAlert('请输入1-99之间的整数', 2);
		}
	}
	else if(type == 3){
		var tmpnum = $.cookie('bookbehalfnum' + i) * 1;
		if(tmpnum >= 1){
			$('#ff-sc-detail-num-book' + i).val($('#ff-sc-detail-num-book' + i).val() * 1 - 1)
			$.cookie('bookbehalfnum' + i, tmpnum-1, {path:'/' });
			shoppingCarShow(url);
			$('#tmpphone').val(tmpphone);
			$('#tmpaddress').val(tmpaddress);
		}
		else{
			shuAlert('请输入1-99之间的整数', 2);
		}
	}
}

//增加按钮
function numadd(i, url, type){
	var tmpphone = $('#tmpphone').val();
	var tmpaddress = $('#tmpaddress').val();
	if(type == 1){
		var tmpnum = $.cookie('booknum' + i) * 1;
		if(tmpnum <= 98){
			$('#ff-sc-detail-num' + i).val($('#ff-sc-detail-num' + i).val() * 1 + 1)
			$.cookie('booknum' + i, tmpnum+1, {path:'/' });
			shoppingCarShow(url);
			$('#tmpphone').val(tmpphone);
			$('#tmpaddress').val(tmpaddress);
		}
		else{
			shuAlert('请输入1-99之间的整数', 2);
		}
	}
	else if(type == 2){
		var tmpnum = $.cookie('urlbehalfnum' + i) * 1;
		if(tmpnum <= 98){
			$('#ff-sc-detail-num-url' + i).val($('#ff-sc-detail-num-url' + i).val() * 1 + 1)
			$.cookie('urlbehalfnum' + i, tmpnum+1, {path:'/' });
			shoppingCarShow(url);
			$('#tmpphone').val(tmpphone);
			$('#tmpaddress').val(tmpaddress);
		}
		else{
			shuAlert('请输入1-99之间的整数', 2);
		}
	}
	else if(type == 3){
		var tmpnum = $.cookie('bookbehalfnum' + i) * 1;
		if(tmpnum <= 98){
			$('#ff-sc-detail-num-book' + i).val($('#ff-sc-detail-num-book' + i).val() * 1 + 1)
			$.cookie('bookbehalfnum' + i, tmpnum+1, {path:'/' });
			shoppingCarShow(url);
			$('#tmpphone').val(tmpphone);
			$('#tmpaddress').val(tmpaddress);
		}
		else{
			shuAlert('请输入1-99之间的整数', 2);
		}
	}
}

//数量设置
function numset(i, url, type){
	var tmpphone = $('#tmpphone').val();
	var tmpaddress = $('#tmpaddress').val();
	if(type == 1){
		var tmpnum = $('#ff-sc-detail-num' + i).val();
		if(tmpnum > 0 && tmpnum < 100){
			$.cookie('booknum' + i, tmpnum, {path:'/' });
			shoppingCarShow(url);
			$('#tmpphone').val(tmpphone);
			$('#tmpaddress').val(tmpaddress);
		}
		else{
			shuAlert('请输入1-99之间的整数', 2);
			$('#ff-sc-detail-num' + i).val($.cookie('booknum' + i));
		}
	}
	else if(type == 2){
		var tmpnum = $('#ff-sc-detail-num-url' + i).val();
		if(tmpnum > 0 && tmpnum < 100){
			$.cookie('urlbehalfnum' + i, tmpnum, {path:'/' });
			shoppingCarShow(url);
			$('#tmpphone').val(tmpphone);
			$('#tmpaddress').val(tmpaddress);
		}
		else{
			shuAlert('请输入1-99之间的整数', 2);
			$('#ff-sc-detail-num-url' + i).val($.cookie('urlbehalfnum' + i));
		}
	}
	else if(type == 3){
		var tmpnum = $('#ff-sc-detail-num-book' + i).val();
		if(tmpnum > 0 && tmpnum < 100){
			$.cookie('bookbehalfnum' + i, tmpnum, {path:'/' });
			shoppingCarShow(url);
			$('#tmpphone').val(tmpphone);
			$('#tmpaddress').val(tmpaddress);
		}
		else{
			shuAlert('请输入1-99之间的整数', 2);
			$('#ff-sc-detail-num-book' + i).val($.cookie('bookbehalfnum' + i));
		}
	}
}

//取消购买
function bookdel(i, url, type){
	var tmpphone = $('#tmpphone').val();
	var tmpaddress = $('#tmpaddress').val();
	if(type == 1){
		$.cookie('booknum' + i, 0, {path:'/' });
	}
	else if(type == 2){
		$.cookie('urlbehalfnum' + i, 0, {path:'/' });
	}
	else if(type == 3){
		$.cookie('bookbehalfnum' + i, 0, {path:'/' });
	}
	shoppingCarShow(url);
	$('#tmpphone').val(tmpphone);
	$('#tmpaddress').val(tmpaddress);
}

//继续购物
function continuebuy(){
	$('#ff-sc').attr('class', 'menu-head-normal');
	$('#ff-sc').children('#sc-logo').attr('src', '/static/image/sc_logo.png');
    $('#ff-sc').children('#sc-ico-arrow').attr('src', '/static/image/ico_down_arrow.png');
    $('#fixed-frame-first-main').css('border-bottom-color','#282828');
    $('#fixed-frame-second').hide();
}