
//不得不使用/static/
$.fn.taxonomy_children = function(){
    p = $(this).parent();
    pp = p.parent();
    c = p.children(".taxonomy-list-children").first();
    pc = pp.find(".taxonomy-list-children");
    pc_not = pc.not(c);
    pc_not.each(function (){
        $(this).parent().find("#ico").first().attr("src", "static/image/ico_right_v.png");
        $(this).slideUp();
    });
    c.parent().find("#ico").first().attr("src", "static/image/ico_down_v.png");
    c.slideDown();

}


