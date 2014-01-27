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
			if b.isbn is not None and b.isbn != '' and (b.description is None or b.description == ''):
				con = get_info_from_douban_by_isbn(b.isbn)
				desc = filter_info(con)
				b.description = desc
				b.save()
		except Exception, e:
			print e
			print b.name
			print b.isbn
			print con

if __name__ == '__main__':
	get_info_auto()
	print 'end'

