function suggestjudge(){
	var context = $('.context').val();
	if (context){
		$('#suggest').submit();
	}
	else{
		shuAlert('请填写留言板内容', 2);
	}
}