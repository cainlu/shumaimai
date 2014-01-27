//订单细节展示
function detailShow(deals, deal){
	trStri = "<tr id='book" + deal.id + "-detail' class='book-detail'>\
		<td colspan=5>\
			<table class='table-detail'>\
				<tr class='first-tr-detail''>\
					<th width='10%'></th>\
					<th width='30%'>书本名称</th>\
					<th width='20%'>作者</th>\
					<th width='15%'>麦麦价</th>\
					<th width='10%'>数量</th>\
					<th width='15%'>小计</th>\
				</tr>\
				{% for tmpbook in deals[deal]['books'].keys() %}\
				<tr>\
					<td><img height='50' width='40' src=" + tmpbook.get_cover_url() + "></td>\
					<td>\
					<font style='color:rgb(56,103,131);'>" + tmpbook.name + "</font>\
					{% if tmpbook.price_old == 0 %}\
					<font style='color:red;'>(代购)</font>\
					{% endif %}\
					</td>\
					<td>" + tmpbook.author + "</td>\
					<td>\
					{% if tmpbook.price_old == 0 %}\
					未知\
					{% else %}\
					" + tmpbook.price_old + "\
					{% endif %}\
					</td>\
					<td>" + deals[deal]['books'][tmpbook] + "</td>\
					<td>\
					{% if tmpbook.price_old == 0 %}\
					未知\
					{% else %}\
					" + tmpbook.price_old * deals[deal]['books'][tmpbook] + "\
					{% endif %}\
					</td>\
				</tr>\
				{% endfor %}\
				<tr>\
					<td colspan=6>\
						<div style='float:left;'>&nbsp;&nbsp;&nbsp;收货信息&nbsp;&nbsp;&nbsp;</div>\
						<div style='float:left;'>联系电话：" + deal.phone + "&nbsp;&nbsp;&nbsp;</div>\
						<div style='float:left;'>收货地址：" + deal.address + "&nbsp;&nbsp;&nbsp;</div>\
						<div style='float:right;'>\
							<b>合计：</b>\
							<font size=4 color='red'>￥" + deals[deal]['totalPrice'] + "&nbsp;&nbsp;&nbsp;</font>\
						</div>\
					</td>\
				</tr>\
			</table>\
		</td>\
	</tr>"
	$(trStri).insertAfter($("#table-id tr:eq(1)"));
}