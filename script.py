#coding=utf-8

import urllib  
import xml.dom.minidom

ROOT = 'http://api.douban.com/book/subject/isbn/'
API_KEY = '0cc4ab4b32942419264e01e197bc6c4b'

def filter_info(text):
	res = ''
	doc = xml.dom.minidom.parseString(text)
	for node in doc.getElementsByTagName("summary"):
		res += node.firstChild.nodeValue
	return res

def get_info_from_douban_by_isbn(isbn):
	isbn = str(isbn)
	con = urllib.urlopen(ROOT + isbn + '?apikey=' + API_KEY).read()
	return con

def get_info_auto():
	from book.models import Book
	books = Book.objects.all()
	for b in books:
		try:
			if b.isbn is not None and (b.description is None or b.description == ''):
				con = get_info_from_douban_by_isbn(b.isbn)
				desc = filter_info(con)
				b.description = desc
				b.save()
		except Exception, e:
			print e
			print b.name
			print b.isbn
			print con

def set_taxonomy():
	from book.models import Book, Taxonomy
	f = open('book_all.csv', 'rb')
	bl = f.read().decode('gbk').split('\r\n')
	f.close()
	for l in bl:
		tmp = l.split(',')
		bs = Book.objects.filter(name=tmp[0])
		for b in bs:
			if not b.get_taxonomy().exists():
				try:
					t = Taxonomy.objects.get(name__icontains=tmp[2])
					b.add_taxonomy(t)
				except Exception, e:
					print e
					print tmp[0] + tmp[2]

def set_price():
	from book.models import Book, Taxonomy
	t = Taxonomy.objects.get(name='二手教材')
	bs = Book.objects.filter(taxonomy__taxonomy__parent=t)
	for b in bs:
		b.price_now = float(int(b.price_ori * 0.45))
		b.save()

def get_new_book():
	from book.models import Book
	f = open("book3.txt", 'rb')
	b_l = f.read().decode('gbk').split('\r\n')
	f.close()
	f = open("book_new.txt", 'wb')
	for l in b_l:
		if l is not None and l != '':
			try:
				tmp = l.split('\t')
				isbn = tmp[4]
				if not Book.objects.filter(isbn=isbn).exists():
					f.write(l + '\n')
			except Exception, e:
			  print e
			  print l
			  break
	f.close()

def input_book():
	from book.models import Book
	from retrieve import DangDang
	f = open("book_new.txt", 'rb')
	b_l = f.read().split('\n')
	f.close()
	for l in b_l:
		if l is not None and l != '':
			try:
				tmp = l.split('\t')
				isbn = tmp[4]
				try:
					isbn = str(int(isbn))
				except:
					isbn = None
				b,created = Book.objects.get_or_create(name=tmp[0], author=tmp[1], press=tmp[2], version=tmp[3])
				if isbn is not None:
					url = DangDang.get_book_url_by_isbn(isbn)
					raw = DangDang.get_book_html_by_target_url(url)
					b.publication_date = DangDang.filter_book_publication_date(raw)
					b.size = DangDang.filter_book_size(raw)
					b.binding = DangDang.filter_book_binding(raw)
					b.page_number = DangDang.filter_book_page_number(raw)
					b.price_ori = DangDang.filter_book_price_ori(raw)
					b.price_now = float(int(b.price_ori * 0.45))
					b.isbn = isbn
					b.status = 1
					b.language = 'zh'
					b.save()
			except Exception, e:
			  print e
			  print l
	f.close()



if __name__ == '__main__':
	get_info_auto()
	print 'end'

