
function re(url, seconds, seconds_display){
    if(seconds>0){
        if(seconds_display!=null)
            seconds_display.text(seconds);
        seconds--;
        setTimeout(function(){re(url, seconds, seconds_display);}, 1000)
    }else{
        location.href=url;
    }
}

