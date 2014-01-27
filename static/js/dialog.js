
// dialog

$(document).ready(function() {
    $(".dialog-wrap").hide();
}); 


$.fn.dialogShow = function(){
    node = $(this);
    if(node.css('display') == 'none'){
        node.show();
    }
    else{
        node.hide()
    }
}

