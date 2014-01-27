(function($) {
    var tips;
    var tipsDivs = [];
    //���ڱ仯�ض�λ���ڴ�С
    window.onresize = function() {
        $.each(tipsDivs,
        function(n, value) {
            tips.setPosition(value.opts, value.obj, value.tipsDiv);
        })
    }
    var lastID = {};
    $.fn.tips = function(opts) {
        var obj = $(this);
		$(this).css("cursor","pointer");
        opts = opts || {};
        opts = $.extend({},tips.config, opts); //��ʼ������
        if (opts.showOn != 'none') {
            switch (opts.showOn) {
            case 'click':
                obj.bind({
                    'click':
                    function(event) {
						tips.eventIn($(this), lastID, opts);
                    },
                    'mouseleave': function(event) {
                        var the = $(this);
                        $("body").bind({
                            'click': function() {
                                var tipDiv = $('#' + the.attr("tips"));
                                tips.setAniDuration(opts, "out", tipDiv);
                            }

                        });
                        $(this).click(function(event) {
                            event.stopPropagation();
                        });
                    }
                });
				if (opts.goshow == true) {
					obj.trigger("click").trigger("mouseleave");
				}
                break;
            case 'focus':
                obj.bind({
                    'focusin':
                    function() {
                        tips.eventIn($(this), lastID, opts);
                    },
                    'focusout': function() {
                        var tipDiv = $('#' + $(this).attr("tips"));
                        tips.setAniDuration(opts, "out", tipDiv);
                    }
                });
                break;
            case 'hover':
                {
                    var timeOut = null;
                    obj.bind({
                        'mouseleave': function() {
                            var tipDiv = $('#' + $(this).attr("tips"));
                            if (opts.alignTo == "target" && opts.allowTipHover == true) {
                                timeOut = setTimeout(function() {
                                    tips.setAniDuration(opts, "out", tipDiv);
                                },
                                opts.timeOnScreen);
                            } else {
                                tips.setAniDuration(opts, "out", tipDiv);
                            }
                        },
                        'mouseenter': function() {
                            var tipDiv = tips.eventIn($(this), lastID, opts);
                            if (opts.alignTo == "target" && opts.allowTipHover == true) {
                                //��tipsע��һ���¼�
                                tipDiv.bind({
                                    'mouseenter': function() {
                                        clearTimeout(timeOut);
                                    },
                                    'mouseleave': function() {
                                        tips.setAniDuration(opts, "out", tipDiv);
                                    }
                                })
                            }
                            if (opts.alignTo == "cursor") {
                                $(this).bind({
                                    mousemove: function(event) {
                                        //�����������
                                        var tipDiv = $('#' + $(this).attr("tips"));
                                        var pageX = event.clientX + $(window).scrollLeft() + 5;
                                        var pageY = event.clientY + $(window).scrollTop() + 5;
                                        tipDiv.css({
                                            top: pageY + "px",
                                            left: pageX + "px"
                                        });
                                    }
                                })
                            }

                        }

                    });
                    break;

                }
            }
        } else {
            $.each(obj,
            function() {
                tips.insertTips(opts, $(this));
                var tipDiv = $('#' + $(this).attr("tips"));
                tipDiv.hide();
            });

        }
		return obj;		
    }

    tips = {
        index: 0,
        config: {
            width: "auto",
			maxWidth: 240,
            height: "auto",
            //NUM
            url: false,
            content: "",
			img:"",
			imgMaxWidth:400,
			goshow:false,
			closeBtn:false,
            style: "blue",//blue red green
            showTimeout: 200,
            hideTimeout: 200,
            timeOnScreen: 1000,
            showOn: "hover",
            //hover focus click none
            alignTo: "target",
            //cursor
            alignX: "center",
            //right left center
            alignY: "top",
			arrowX: "50%",
			arrowY: "10px",
            //bottom center top 
            offsetX: 0,
            offsetY: 0,
            allowTipHover: false,
            //	followCursor:     true,
            bubble: true,
			fade: false,
			bubbleDistance: 20,
			bubbleSpeed:250,
            iframe: false,
            callback: function() {
				}

        },
        eventIn: function(the, theLastID, opts) {
			if (opts.content == "") {
				opts.content = the.attr("title");		//ȡԪ�ص�title����ֵ
				
			}
            if (!jQuery.isEmptyObject(theLastID)) {
                if (the.attr("tips") != theLastID.tipDiv.attr("id")) {
                    tips.setAniDuration(lastID.opts, "out", theLastID.tipDiv);
                }
            
            }
            if (the.attr("tips") == null) {
                tips.insertTips(opts, the);
                var tipDiv = $('#' + the.attr("tips"));
                theLastID = {
                    tipDiv: tipDiv,
                    opts: opts
                };
            }
			else {
				var tipDiv = $('#' + the.attr("tips"));
                if (tipDiv.is(":hidden")) {
                    tips.setAniDuration(opts, "in", tipDiv);
                    theLastID = {
                        tipDiv: tipDiv,
                        opts: opts
                    };
                } else {
                    if (opts.alignTo != "cursor") {
                        tips.setAniDuration(opts, "out", tipDiv);
                    }

                }
			}
            lastID = theLastID;
            return tipDiv;
        },
        setPosition: function(opts, obj, div) {
            var t = obj.offset().top;
            var l = obj.offset().left;
            var w = obj.outerWidth();
            var h = obj.outerHeight();
			var arrowMiddleX = opts.arrowX;
			var arrowMiddleY = opts.arrowY;
			if (opts.alignY == "top"){
				if(opts.alignX == "left") {
					l = l - div.outerWidth();
					div.find(".ico").css("top",arrowMiddleY);
				}
				else if(opts.alignX == "right"){
					  l = l + obj.outerWidth();
					  div.find(".ico").css("top",opts.arrowY);
				}
				else {
					l = l + obj.outerWidth()/2 - div.outerWidth()/2;
					t = t - div.outerHeight();
					div.find(".ico").css("left",arrowMiddleX);
				}
			}
			if (opts.alignY == "bottom"){
				 t = t + obj.outerHeight();
				 if(opts.alignX == "right"){
					  l = l + obj.outerWidth() - div.outerWidth();
				 }
				 if(opts.alignX == "center") {
					 l = l + obj.outerWidth()/2 - div.outerWidth()/2;
				 }
				div.find(".ico").css("left",opts.arrowX);

			}
			if (opts.alignY == "center"){
				t = t + obj.outerHeight()/2 - div.outerHeight()/2 ;
				if(opts.alignX == "left") {
					l = l - div.outerWidth();
					div.find(".ico").css("top",arrowMiddleY);
				}
				else if(opts.alignX == "right"){
					  l = l + obj.outerWidth();
					  div.find(".ico").css("top",arrowMiddleY);
				}
			}
            l = l + opts.offsetX;
            t = t + opts.offsetY;
			div.css({left:l,top:t});
        },
        setDirection: function(opts) {
            var direction;
			if (opts.alignY == "top") direction = "dn";
			if (opts.alignX == "left") direction = "rt";
            else if (opts.alignX == "right") direction = "lt";
			if (opts.alignY == "bottom") direction = "up";
            if (opts.alignTo == "cursor") direction = null;
            return direction;
        },
        insertTips: function(opts, obj) {
			var tipsDiv;
            var direction = tips.setDirection(opts);
            the = obj;
            if (opts.url) {
                if (!opts.iframe) {
                    $.ajax({
                        type: (opts.ajaxType || 'GET'),
                        data: (opts.data || ''),
                        url: opts.url,
                        success: function(data) {
                            tipsDiv.find(".tipBd").html(data);
                            var position = tips.setPosition(opts, obj, tipsDiv);
                            tips.setAniDuration(opts, "in", tipsDiv);
                            opts.content = data;
                            opts.callback(the,data);
                        }

                    });
                    opts.content = "Loading...";
                } else opts.content = '<iframe class="tipsif " id=tip' + tips.index + ' style="width:100%; height:' + opts.height + 'px"  frameborder="0" hspace="0" src="' + opts.url + ' "></iframe>';
            }
			var closeBtn = "";
			if (opts.closeBtn) {
			    closeBtn = '<a href="#" class="close-ico" onclick="return false"></a>';
			}
			
			if (opts.img != "") {
				tipsDiv = $('<div style="display:none; width:48px; height:32px" class="tips ' + opts.style+'_'+direction + '"id=tip' + tips.index + '><i class="ico" id="iB"></i><div class="tipHd '+opts.style+'_tipHd"><b></b></div><div class="tipBd '+opts.style+'_tipBd">' + '<img src="tips/i/loading.gif" width="16" height="16" />' + ''+closeBtn+'</div><div class="tipFt '+opts.style+'_tipFt"><b></b></div></div>');
			}else {
				tipsDiv = $('<div  style="display:none" class="tips ' + opts.style+'_'+direction + '"id=tip' + tips.index + '><i class="ico" id="iB"></i><div class="tipHd '+opts.style+'_tipHd"><b></b></div><div class="tipBd '+opts.style+'_tipBd">' + opts.content + ''+closeBtn+'</div><div class="tipFt '+opts.style+'_tipFt"><b></b></div></div>');
				if (opts.closeBtn) {
					tipsDiv.find(".tipBd").css("paddingRight",parseInt(tipsDiv.find(".tipBd").css("paddingRight")) + 16);
				}
			}
	
            the.attr("tips", "tip" + tips.index);
            lastID = tips.index;
     	    tipsDiv.appendTo("body");			
            var position = tips.setPosition(opts, the, tipsDiv);
			tips.setAniDuration(opts, "in", tipsDiv);
			
			/*ͼƬδ�����Ȼ�óߴ粢����*/
  			if (opts.img != "") {
				imgReady(opts.img, function () {
					 var thiswidth  = this.width;
					 var thisheight = this.height;
					 var wait=setInterval(function(){
		                if(!tipsDiv.is(":animated")){
						  	if (thiswidth > opts.imgMaxWidth){
							    maxWidth = opts.imgMaxWidth +"px";
							    tipsDiv.width(opts.imgMaxWidth + 12);
						        tipsDiv.height("auto");
					        } else{
							    maxWidth = thiswidth +"px";
								tipsDiv.width(thiswidth + 12);
							    tipsDiv.height(thisheight + 10);
						    }
							tipsDiv.find(".tipBd").html('<img style="width:'+maxWidth+'" src="'+opts.img+'">');
		                    clearInterval(wait);
							tips.setPosition(opts, obj, tipsDiv);
		                }
		            },200);
				});
			
			}
			
            tipsDivs[tips.index] = {
                obj: the,
                tipsDiv: tipsDiv,
                opts: opts
            };
			if(!opts.iframe && !opts.url){
				opts.callback(the);
			}
            tips.index++;
        },
        setAniDuration: function(opts, status, obj) {
			$(".tips:animated").stop(false,true);  //��ʼ�¶���֮ǰ��֤�϶����ر�
            $.each(obj,
            function() {					
				var the = $(this);
                if (opts.fade || opts.alignTo == "cursor") {
                    if (status == "in") {
					   $(this).fadeIn(opts.showTimeout);
                    } else if (status == "out") {
                       $(this).fadeOut(opts.hideTimeout);
                    }

                } else if (opts.bubble && opts.alignTo != "cursor") {
					var direction = tips.setDirection(opts);
                    if (status == "in") {
							 the.css({"display":"block"});
							 if (direction == "dn"){
							 	the.css("top",parseInt(the.css("top")) - opts.bubbleDistance);
							    the.not(":animated").animate({top: '+='+opts.bubbleDistance+'px'},opts.bubbleSpeed);
							 }
							 else if (direction == "up"){
							 	the.css("top",parseInt(the.css("top")) + opts.bubbleDistance);
							    the.not(":animated").animate({top: '-='+opts.bubbleDistance+'px'},opts.bubbleSpeed);
							 }
							 else if (direction == "lt"){
							 	the.css("left",parseInt(the.css("left")) + opts.bubbleDistance);
							    the.not(":animated").animate({left: '-='+opts.bubbleDistance+'px'},opts.bubbleSpeed);
							 }
						     else {
							 	the.css("left",parseInt(the.css("left")) - opts.bubbleDistance);
							    the.not(":animated").animate({left: '+='+opts.bubbleDistance+'px'},opts.bubbleSpeed);
							 }
;                      
                    } else if (status == "out") {
						 if (direction == "dn"){
								  the.not(":animated").animate({top: '-='+opts.bubbleDistance+'px'},opts.bubbleSpeed,function() {
								  the.css("top",parseInt(the.css("top")) + opts.bubbleDistance);
								  the.css({"display":"none"});
								 });
						 }
						 else if (direction == "up"){
								  the.not(":animated").animate({top: '+='+opts.bubbleDistance+'px'},opts.bubbleSpeed,function() {
							      the.css("top",parseInt(the.css("top")) - opts.bubbleDistance);
								  the.css({"display":"none"});
								 });
						 }
						 else if (direction == "lt"){
								  the.not(":animated").animate({left: '+='+opts.bubbleDistance+'px'},opts.bubbleSpeed,function() {
								  the.css("left",parseInt(the.css("left")) - opts.bubbleDistance);
								  the.css({"display":"none"});
								 });
						 }
					     else {
								  the.not(":animated").animate({left: '-='+opts.bubbleDistance+'px'},opts.bubbleSpeed,function() {
								  the.css("left",parseInt(the.css("left")) + opts.bubbleDistance);
								  the.css({"display":"none"});
								 });
						 }
								 
                  	    }
					
                }
				 else if(!opts.bubble && !opts.fade) {
                    if (status == "in") {
                        $(this).show();
                    } else if (status == "out") {
                        $(this).hide();
                    }
                }

            });

        }
    }
})(jQuery);
/**
 * ͼƬͷ���ݼ��ؾ����¼� - �����ȡͼƬ�ߴ�
 * @version	2011.05.27
 * @author	TangBin
 * @see		http://www.planeart.cn/?p=1121
 * @param	{String}	ͼƬ·��
 * @param	{Function}	�ߴ����
 * @param	{Function}	������� (��ѡ)
 * @param	{Function}	���ش��� (��ѡ)
 * @example imgReady('http://www.google.com.hk/intl/zh-CN/images/logo_cn.png', function () {
		alert('size ready: width=' + this.width + '; height=' + this.height);
	});
 */
var imgReady = (function () {
	var list = [], intervalId = null,

	// ����ִ�ж���
	tick = function () {
		var i = 0;
		for (; i < list.length; i++) {
			list[i].end ? list.splice(i--, 1) : list[i]();
		};
		!list.length && stop();
	},

	// ֹͣ���ж�ʱ������
	stop = function () {
		clearInterval(intervalId);
		intervalId = null;
	};

	return function (url, ready, load, error) {
		var onready, width, height, newWidth, newHeight,
			img = new Image();
		
		img.src = url;

		// ���ͼƬ�����棬��ֱ�ӷ��ػ�������
		if (img.complete) {
			ready.call(img);
			load && load.call(img);
			return;
		};
		
		width = img.width;
		height = img.height;
		
		// ���ش������¼�
		img.onerror = function () {
			error && error.call(img);
			onready.end = true;
			img = img.onload = img.onerror = null;
		};
		
		// ͼƬ�ߴ����
		onready = function () {
			newWidth = img.width;
			newHeight = img.height;
			if (newWidth !== width || newHeight !== height ||
				// ���ͼƬ�Ѿ��������ط����ؿ�ʹ��������
				newWidth * newHeight > 1024
			) {
				ready.call(img);
				onready.end = true;
			};
		};
		onready();
		
		// ��ȫ������ϵ��¼�
		img.onload = function () {
			// onload�ڶ�ʱ��ʱ��Χ�ڿ��ܱ�onready��
			// ������м�鲢��֤onready����ִ��
			!onready.end && onready();
		
			load && load.call(img);
			
			// IE gif������ѭ��ִ��onload���ÿ�onload����
			img = img.onload = img.onerror = null;
		};

		// ��������ж���ִ��
		if (!onready.end) {
			list.push(onready);
			// ���ۺ�ʱֻ�������һ����ʱ��������������������
			if (intervalId === null) intervalId = setInterval(tick, 40);
		};
	};
})();