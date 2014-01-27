#coding=utf-8

import os

def image_input_auto():
    ori_im_dir_list = os.listdir('image_tmp')
    from book.models import Book
    for f in ori_im_dir_list:
        ori_im_dir = os.path.join('image_tmp', f)
        if os.path.isdir(ori_im_dir):
            try:
                isbn = str(int(f))
                book = Book.objects.get(isbn=isbn)
                im_dir = os.path.join('static/image/book/', str(book.id))
                im_path = os.path.join(im_dir, 'cover.jpg')
                ori_im_path = os.path.join(ori_im_dir, 'cover.jpg')
                if not os.path.exists(im_path) and os.path.exists(ori_im_path):
                    try:
                        os.makedirs(im_dir)
                    except:
                        pass
                    ori_im = open(ori_im_path, 'rb')
                    raw = ori_im.read()
                    ori_im.close()
                    im = open(im_path,'wb')
                    im.write(raw)
                    im.close()
                    book.image_dict = {'cover':'/static/image/book/' + str(book.id) + '/cover.jpg'}
                    book.save()
            except Exception, e:
                print e



if __name__ == '__main__':
    print 'start'
    print 'end'


