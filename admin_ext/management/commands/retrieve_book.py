#coding=utf-8

import os
import logging

from optparse import make_option

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from admin_ext.retrieve import Dangdang, Douban

from book.models import Book


class Command(BaseCommand):
    help = 'Get books info from net.'

    _logger = logging.getLogger('default')

    def handle(self, *args, **options):
        books = Book.objects.filter(status=4)
        for book in books[:3000]:
            try:
                isbn = book.isbn
                try:
                    if isbn is None or isbn == '':
                        raise "ISBN is None."
                    url = Dangdang.get_book_url_by_isbn(isbn)
                    if url is None or url == '':
                        raise Exception("ISBN: " + str(isbn) + " is not found.")
                except Exception, e:
                    q_list = list()
                    for i in [book.name, book.author, book.press]:
                        if i is not None:
                            q_list.append(i)
                    if len(q_list) < 1:
                        raise Exception("没有任何信息可以用来搜索. Book id -> " + str(book.id))
                    q = ' '.join(q_list)
                    q = q.decode('utf-8').encode('gbk')
                    url = Dangdang.get_book_url_by_keywords(q)
                raw = Dangdang.get_book_html_by_target_url(url)
                if len(raw) < 200:
                    raw = Dangdang.get_book_html_by_target_url(url)

                book.name = Dangdang.filter_book_name(raw)
                book.isbn = Dangdang.filter_book_isbn(raw)
                authors, translators = Dangdang.filter_book_author_and_translator(raw)
                book.author = ','.join(authors)
                book.translator = ','.join(translators)
                book.press = Dangdang.filter_book_press(raw)
                book.publication_date = Dangdang.filter_book_publication_date(raw)
                book.size = Dangdang.filter_book_size(raw)
                book.binding = Dangdang.filter_book_binding(raw)
                book.page_number = Dangdang.filter_book_page_number(raw)
                book.price_ori = Dangdang.filter_book_price_ori(raw)
                book.version = Dangdang.filter_book_version(raw)
                book.language = 'zh'

                im_dir = os.path.join(settings.STATIC_ROOT, 'image', 'book', str(book.id))
                im_path = os.path.join(im_dir, 'cover.jpg')
                if not (os.path.exists(im_dir) and os.path.isdir(im_dir)):
                    os.makedirs(im_dir)
                img_url = Dangdang.filter_book_img_url(raw)
                Dangdang.get_img_by_url(img_url, im_path)
                book.image_dict = {'cover':'/static/image/book/' + str(book.id) + '/cover.jpg'}

                raw = Douban.get_info_from_douban_by_isbn(book.isbn)
                if book.description is None or book.description.strip() == '':
                    book.description = Douban.filter_desc(raw)

            except Exception, e:
                self._logger.error(str(e) + ' Book id -> ' + str(book.id))
            finally:
                book.status = 5
                book.save()


