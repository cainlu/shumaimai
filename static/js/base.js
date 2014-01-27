$(function() {
    $(".tTip").betterTooltip({speed:150,delay:300});

    $(".cycle-wrapper").each(function(){
        $(this).cycle({
            pager:'#img-nav', 
            pagerEvent: 'mouseover', 
            pauseOnPagerHover:true,
            fx:'scrollDown', 
            easing:'easeOutBounce', 
            timeout:7000,
            slideExpr:'img'
        });
    });
});

/*
 * my js 
 */

/*** get table line class ***/
function getTableLineClass(i){
    i = parseInt(i);
    return "odd";
}

$.fn.changeBackgroundImage = function(imageURL) {
    $(this).css('background-image', 'url(' + imageURL + ')');
}

/*** my validate ***/
$.fn.myValidate = function(offsetL,offsetT,options) {
    var defaults = {
        errorPlacement:function(error,element) {
            name = element.attr('name');
            var con = '<div class="tip" id="' + name +'"></div>';
            $('.tip#' + name).remove();
            $("body").prepend(con);
            var $this = element; 
            var tip = $('.tip#' + name);
            error.attr('class',error.attr('class')+" tText");
            error.appendTo(tip);
            var topOffset = tip.height();
            var offset = $this.offset();
            var tLeft = offset.left+offsetL;
            var tTop = offset.top+offsetT;
            var tWidth = $this.width();
            var xTip = tLeft+tWidth+"px";
            var yTip = tTop-topOffset+20+"px";
            tip.css({'top' : yTip, 'left' : xTip});
            tip.show();
        },
        success:function(label) {
            label.parent().remove();
        }
    };
    var options = $.extend(defaults, options);
    return $(this).validate(options);
}

/*** tTip ***/
$.fn.betterTooltip = function(options){
    var defaults = {
        speed: 200,
        delay: 300
    };
    var options = $.extend(defaults, options);
    getTip = function() {
        var tTip = "<div class='tip'><div class='tText'></div></div>";
        return tTip;
    }
    $("body").prepend(getTip());

    $(this).each(function(){
        var $this = $(this);
        var tip = $('.tip');
        var tipInner = $('.tip .tText');
        var tTitle = (this.title);
        this.title = "";
        var offset = $(this).offset();
        var tLeft = offset.left+25;
        var tTop = offset.top-150;
        var tWidth = $this.width();
        var tHeight = $this.height();
        $this.hover(
            function() {
                tipInner.html(tTitle);
                setTip(tTop, tLeft);
                setTimer();
            }, 
            function() {
                stopTimer();
                tip.hide();
            }
        );           
        setTimer = function() {
            $this.showTipTimer = setInterval("showTip()", defaults.delay);
        }
        stopTimer = function() {
            clearInterval($this.showTipTimer);
        }
        setTip = function(top, left){
            var topOffset = tip.height();
            var xTip = left+"px";
            var yTip = top-topOffset+"px";
            tip.css({'top' : yTip, 'left' : xTip});
        }
        /* This function stops the timer and creates the
           fade-in animation                          */
        showTip = function(){
            stopTimer();
            tip.animate({"top": "+=20px", "opacity": "toggle"}, defaults.speed);
        }
    });
};

//弹出框点击其他关闭
function clickclose(){
    $('#sellframe').hide();
    $('#buybehalfframe').hide();
    $('#confirmframe').hide();
    $('#alertframe').hide();
    $('#footer').css("opacity", "1");
    $('#content').css("opacity", "1");
    $('#header').css("opacity", "1");
    $('#fixed-frame').css("opacity", "1");
    $('body').css("filter", "alpha(opacity=100)");
    if($("#fixed-frame-second").is(":visible") && $(".ZebraDialog").length == 0){
        $('#ff-sc').removeClass().addClass("menu-head-normal");
        $('#ff-sc').children('#sc-logo').attr('src', '/static/image/sc_logo.png');
        $('#ff-sc').children('#sc-ico-arrow').attr('src', '/static/image/ico_down_arrow.png');
        $('#fixed-frame-first-main').css('border-bottom-color','#282828');
        $('#fixed-frame-second').hide();
    }
};

//显示alertframe
function alertframeshow(){
    $('#footer').css("opacity", ".30");
    $('#content').css("opacity", ".30");
    $('#header').css("opacity", ".30");
    $('#fixed-frame').css("opacity", "1");
    $('body').css("filter", "alpha(opacity=30)");
    $('#alertframe').show();
}

//alert框
function shuAlert(message, mode){
    if (mode == 1){
        $("#alertframe").contents().find("#alertimg").attr("src", "/static/image/tick.png");
    }
    else if (mode == 2){
        $("#alertframe").contents().find("#alertimg").attr("src", "/static/image/cross.png");
    }
    setTimeout(alertframeshow, 1);
    $("#alertframe").contents().find("#alertmsg").html(message);
    totalheight = (document.body.scrollTop || document.documentElement.scrollTop || window.pageYOffset) + 230;
    $("#alertframe").css({'top': totalheight});
}

//frame提示
function frameAlert(message){
    $("#blueimg").attr('src', '/static/image/bluemark.jpg');
    $("#blueimg").show();
    $("#behalffont").text(message);
    setTimeout('$("#blueimg").hide();', 2000);
    setTimeout('$("#behalffont").text("");', 2000);
}

function frameAlert2(message){
    $("#blueimg").attr('src', '/static/image/tick2.png');
    $("#blueimg").show();
    $("#behalffont").text(message);
    setTimeout('$("#blueimg").hide();', 2000);
    setTimeout('$("#behalffont").text("");', 2000);
    //scLight2();
}

//购物车动画
function scLight(){
	$('#ff-sc').fadeTo(400, 0);
    $('#ff-sc').fadeTo(400, 1);
    $('#ff-sc').fadeTo(400, 0);
    $('#ff-sc').fadeTo(400, 1);
    $('.sc_up_img').show();
    $('.sc_up_img').animate({top:"36px"}, 800, function() {
        $('.sc_up_img').hide();
        $('.sc_up_img').css('top', '300px');
    });
}

function scLight2(){
    $('#ff-sc', window.parent.document).fadeTo(400, 0);
    $('#ff-sc', window.parent.document).fadeTo(400, 1);
    $('#ff-sc', window.parent.document).fadeTo(400, 0);
    $('#ff-sc', window.parent.document).fadeTo(400, 1);
    $('.sc_up_img', window.parent.document).show();
    $('.sc_up_img', window.parent.document).animate({top:"36px"}, 1000, function() {
        $('.sc_up_img', window.parent.document).hide();
        $('.sc_up_img', window.parent.document).css('top', '300px');
    });
}

//ajax的csrf
function csrfSafeMethod(method) {
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
	cache: false,
    crossDomain: false,
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type)) {
        	var csrftoken = $.cookie('csrftoken');
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

