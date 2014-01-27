/*
 * basic css for all pages
 */


function csrfSafeMethod(method) {
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

String.prototype.replaceAll  = function(s1, s2){   
    return this.replace(new RegExp(s1,"gm"), s2);   
} 

function msgClear() {
    $('#main-body').children(".alert.alert-block").remove();
}

function msgPrepend(type, content){
    var msg = {};
    msg['content'] = content;
    switch(type) {
        case 'success': 
            msg['css'] = 'alert-success'; 
            msg['header'] = 'Success!';
            break;
        case 'warning': 
            msg['css'] = ''; 
            msg['header'] = 'Warning!';
            break;
        case 'error': 
            msg['css'] = 'alert-error'; 
            msg['header'] = 'Error!';
            break;
        default: 
            msg['css'] = 'alert-info'; 
            msg['header'] = 'Info!';
            break;
    }
    $('#main-body').prepend($('<div class="alert alert-block ' + msg['css'] + '"><button type="button" class="close" data-dismiss="alert">&times;</button> <h4>' + msg['header'] + '!</h4> <p>' + msg['content'] + '</p> </div> '));
}


/*
 * URL 
 */

function isNumeric(arg) {
    return !isNaN(parseFloat(arg)) && isFinite(arg);
}

function urlDecode(arg, url) {
    var _ls = url || window.location.toString();

    if(_ls.substring(0,2) === '//') _ls = 'http:' + _ls;
    else if(_ls.split('://').length === 1) _ls = 'http://' + _ls;

    url = _ls.split('/');
    var _l = {auth:''}, host = url[2].split('@');

    if(host.length === 1) host = host[0].split(':');
    else{ _l.auth = host[0]; host = host[1].split(':'); }

    _l.protocol=url[0], _l.hostname=host[0], _l.port=(host[1]||'80'), _l.pathname='/' + url.slice(3, url.length).join('/').split('?')[0].split('#')[0];
    var _p = _l.pathname;
    if(_p.split('.').length === 1 && _p[_p.length-1] !== '/') _p += '/';
    var _h = _l.hostname, _hs = _h.split('.'), _ps = _p.split('/');

    if(!arg) return _ls;
    else if(arg === 'hostname') return _h;
    else if(arg === 'domain') return _hs.slice(-2).join('.');
    else if(arg === 'tld') return _hs.slice(-1).join('.');
    else if(arg === 'sub') return _hs.slice(0, _hs.length - 2).join('.');
    else if(arg === 'port') return _l.port || '80';
    else if(arg === 'protocol') return _l.protocol.split(':')[0];
    else if(arg === 'auth') return _l.auth;
    else if(arg === 'user') return decodeURIComponent(_l.auth.split(':')[0]);
    else if(arg === 'pass') return decodeURIComponent(_l.auth.split(':')[1] || '');
    else if(arg === 'path') return _p;
    else if(arg === 'raw') return _ls.split('?')[0];
    else if(arg[0] === '.'){
        arg = arg.substring(1);
        if(isNumeric(arg)) {arg = parseInt(arg); return _hs[arg < 0 ? _hs.length + arg : arg-1] || ''; }
    }
    else if(isNumeric(arg)){ arg = parseInt(arg); return _ps[arg < 0 ? _ps.length - 1 + arg : arg] || ''; }
    else if(arg === 'file') return decodeURIComponent(_ps.slice(-1)[0]);
    else if(arg === 'filename') return decodeURIComponent(_ps.slice(-1)[0].split('.')[0]);
    else if(arg === 'fileext') return decodeURIComponent(_ps.slice(-1)[0].split('.')[1] || '');
    else if(arg[0] === '?' || arg[0] === '#'){
        var params = _ls, param = null;

        if(arg[0] === '?') params = (params.split('?')[1] || '').split('#')[0];
        else if(arg[0] === '#') params = (params.split('#')[1] || '');

        params = params.split('&');
        var parsD = {}
        if(params.length > 0){
            for(par in params){
                tmp = params[par].split('=');
                if(tmp.length > 1) parsD[decodeURIComponent(tmp[0])] = decodeURIComponent(tmp[1] || '');
            }
        }

        if(!arg[1]) return parsD;
        else {arg = arg.substring(1);return parsD[arg] || '';}

        return null;
    }

    return '';
}

function urlParsEncode(parsD){
    res = [];
    for(var key in parsD) res.push(encodeURIComponent(key) + '=' + encodeURIComponent(parsD[key]));
    resStr = res.join('&');
    return resStr
}


function urlEncode(parsD, url){
    raw = urlDecode('raw', url);
    oriParsD = urlDecode('?', url);
    resParsD = $.extend({}, oriParsD, parsD);
    if($.isEmptyObject(resParsD)) return raw;
    else return raw + '?' + urlParsEncode(resParsD);
}


function urlParRemove(parName, url) {
    raw = urlDecode('raw', url);
    oriParsD = urlDecode('?', url);
    delete oriParsD[parName];
    return urlEncode(oriParsD, raw);
}

$(function(){
    /*
     * ajax的csrf
     */
     
    $.ajaxSetup({
        crossDomain: false,
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type)) {
                var csrftoken = $.cookie('csrftoken');
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    /* 
     * table
     */

    // order
    $('th[order]').each(function(){
        html = $(this).html();
        postive = null
        orderPar = $(this).attr('order');
        orderParM = '-' + orderPar;
        urlOrder = urlDecode('?order');
        if(urlOrder){ ol = $.unique(urlOrder.split(',')).reverse();
            if((i = $.inArray(orderPar, ol)) >= 0) {
                ol.splice(i, 1);
                ol_remove = $.merge([], ol);
                ol.splice(0, 0, orderParM);
                postive = true;
            }
            else if((i = $.inArray(orderParM, ol)) >= 0) {
                ol.splice(i, 1);
                ol_remove = $.merge([], ol);
                ol.splice(0, 0, orderPar);
                postive = false;
            }
            else {
                ol_remove = $.merge([], ol);
                ol.splice(0, 0, orderPar);
            }
        }else{
            ol_remove = [];
            ol = [orderPar];
        }
        order = ol.join(',');
        order_remove = ol_remove.join(',');
        link = urlEncode({'order':order});
        link_remove = urlEncode({'order':order_remove});
        html = '<a href="' + link + '">' + html;
        if(postive != null){
            if(postive) html += ' <i class="icon-chevron-up"></i>';
            else html += ' <i class="icon-chevron-down"></i>';
            html += '</a><a href="'+ link_remove +'"><i class="icon-remove"></i>'
        }
        html += '</a>';
        $(this).html(html);
    });

    // toggle tr
    $('.tr-toggle').each(function(){
        var data = $(this).parent().next('.tr-toggle-data');
        $(this).click(function(){
            data.toggle('1');
        });
    });


    /*
     * datetime input
     */
    $('.datepicker').datetimepicker({
        todayBtn:true,
        todayHighlight:true,
        forceParse:false,
        autoclose:true,
        startView:4,
        minView:2,
        format:'yyyy-mm-dd',
    });
    $('.datetimepicker').datetimepicker({
        todayBtn:true,
        todayHighlight:true,
        minuteStep:10,
        forceParse:false,
        autoclose:true,
        startView:4,
        minView:0,
        format: 'yyyy-mm-dd hh:ii',
    });
    $(".bs-select").chosen();
    $(".bs-select-deselect").chosen({
        allow_single_deselect:true,
    });
});


