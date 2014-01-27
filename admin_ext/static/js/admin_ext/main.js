/*
 * main js for web most pages
 */

function showOneImageChangeDialog(postUrl, csrfToken) {
    html = '\
           <form id="one-image-change-form" method="POST" encType="multipart/form-data" action="'+ postUrl +'">\
                <input type="hidden" name="csrfmiddlewaretoken" value="' + csrfToken + '" />\
                <div class="fileupload fileupload-new text-center" data-provides="fileupload">\
                    <div class="fileupload-preview thumbnail" style="width: 150px; height: 150px;"></div>\
                    <div>\
                        <span class="fileupload-new btn btn-primary" onClick="$(\'#id_image\').click();">Select</span>\
                        <span class="fileupload-exists btn btn-primary" onClick="$(\'#id_image\').click();">Change</span>\
                        <input id="id_image" type="file" class="none" name="image">\
                        <span class="fileupload-exists btn btn-danger" data-dismiss="fileupload">Remove</span>\
                    </div>\
                </div>\
           </form>\
        ';
    bootbox.dialog(html, [
        {
            'label':'保存',
            'class':'btn-success',
            'callback':function(){
                var image = $('#id_image').val();
                if(image == ''){
                    bootbox.alert('请选择一张图片.');
                }else{
                    $('#one-image-change-form').submit();
                }
            },
        },
        {
            'label':'返回',
            'class':'btn',
        },
        ]
    );
}

function showSimpleCreateBookDialog() {
    var html_form = '\
        <form id="create-book-form-tmp" class="form-horizontal" method="POST" action="">\
            <div class="control-group">\
                <label class="control-label" for="name-input">书名:</label>\
                <div class="controls">\
                    <input type="text" id="name-input" name="name"/>\
                </div>\
            </div>\
            <div class="control-group">\
                <label class="control-label" for="author-input">作者:</label>\
                <div class="controls">\
                    <input type="text" id="author-input" name="author"/>\
                </div>\
            </div>\
            <div class="control-group">\
                <label class="control-label" for="press-input">出版社:</label>\
                <div class="controls">\
                    <input type="text" id="press-input" name="press"/>\
                </div>\
            </div>\
            <div class="control-group">\
                <label class="control-label" for="isbn-input">ISBN:</label>\
                <div class="controls">\
                    <input type="text" id="isbn-input" name="isbn"/>\
                </div>\
            </div>\
            <div class="control-group">\
                <label class="control-label" for="position-input">库存:</label>\
                <div class="controls">\
                    <input type="text" id="position-input" name="position"/>\
                </div>\
            </div>\
        </form>\
        </form>\
    ';
    bootbox.dialog(
            html_form, 
            [{
                "label":"下一步",
                "class":"btn-success",
                "callback":function(postUrl){
                    var addFormTmp = $('#create-book-form-tmp');
                    var name = addFormTmp.find('#name-input').val().replace(',', '').replace(' ', '');;
                    var author = addFormTmp.find('#author-input').val().replace(',', '').replace(' ', '');;
                    var press = addFormTmp.find('#press-input').val().replace(',', '').replace(' ', '');;
                    var isbn = addFormTmp.find('#isbn-input').val().replace(',', '').replace(' ', '');;
                    var position = addFormTmp.find('#position-input').val();
                    $('#simple-create-book-form #name-input').val(name);
                    $('#simple-create-book-form #author-input').val(author);
                    $('#simple-create-book-form #press-input').val(press);
                    $('#simple-create-book-form #isbn-input').val(isbn);
                    $('#simple-create-book-form #position-input').val(position);
                    if(( name.length > 0) ||( author.length > 0) ||( press.length > 0) || ( isbn.length > 0)){
                        $.ajax({ 
                            type: 'GET', 
                            url: '/admin-ext/search', 
                            data: { 'name':name, 'author':author, 'press':press, 'isbn':isbn }, 
                            dataType:'json',
                            success: function(res){
                                var books = res;
                                var html = '<table class="table table-striped table-hover">';
                                html += '<tr><th>ID</th><th>书名</th><th>作者</th><th>出版社</th><th>ISBN</th></tr>';
                                for (var i in books){
                                    html += '<tr>';
                                    html += '<td>' + books[i].id + '</td>';
                                    html += '<td><a href="/admin-ext/book/' + books[i].id + '/edit/" target="_blank">' + books[i].name + '</a></td>';
                                    html += '<td>' + books[i].author + '</td>';
                                    html += '<td>' + books[i].press + '</td>';
                                    html += '<td>' + books[i].isbn + '</td>';
                                    html += '</tr>';
                                }
                                html += '</table>';
                                bootbox.classes('modal-large');
                                bootbox.dialog(
                                    html,
                                    [{
                                        "label":"创建新书",
                                        "class":"btn-success",
                                        "callback":function(){
                                            $('#simple-create-book-form #control-input').val(1);
                                            $('#simple-create-book-form').submit();
                                        },
                                    },{
                                        "label":"创建新书并编辑",
                                        "class":"btn-success",
                                        "callback":function(){
                                            $('#simple-create-book-form #control-input').val(2);
                                            $('#simple-create-book-form').submit();
                                        },
                                    },{
                                        "label":"返回",
                                        "class":"btn",
                                    },
                                    ]    
                                );
                                bootbox.classes('');
                            }
                        });
                    }else{
                        bootbox.alert('请输入书本信息。');
                    }
                },
            },{
            "label":"返回",
            "class":"btn",
            },
        ]
    );
}

