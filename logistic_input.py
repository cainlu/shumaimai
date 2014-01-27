#coding=utf-8

def logistic_input_auto(f_name):
	f = open(f_name, 'rb')
	raw = f.read()
	f.close()
	rl = raw.split('\n')
	from book.models import Book
	from logistic.models import Logistic
	f = open('not_found', 'wb')
	for l in rl:
		ll = l.split('\t')
		try:
			book = Book.objects.get(isbn=int(ll[0]))
		except Exception, e:
		 	print e
		 	f.write(l + '\n')
		 	continue
		try:
		 	Logistic.objects.create(book=book, number=0, position=ll[1])
		except Exception, e:
			print e
	f.close()



