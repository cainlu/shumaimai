# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Sell_Deal.price_all'
        db.add_column('sell_deal', 'price_all',
                      self.gf('django.db.models.fields.FloatField')(default=0),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Sell_Deal.price_all'
        db.delete_column('sell_deal', 'price_all')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'book.book': {
            'Meta': {'ordering': "['id']", 'object_name': 'Book', 'db_table': "'book'"},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'}),
            'binding': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'isbn': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'}),
            'page_number': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'press': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'}),
            'price_now': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'price_ori': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'publication_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'recommend': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'size': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'subtitle': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'translator': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '100', 'blank': 'True'}),
            'version': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'})
        },
        'book.course': {
            'Meta': {'ordering': "['-weight']", 'object_name': 'Course', 'db_table': "'course'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'weight': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'})
        },
        'book.major': {
            'Meta': {'ordering': "['-weight']", 'unique_together': "(('name', 'type', 'diploma'),)", 'object_name': 'Major', 'db_table': "'major'"},
            'diploma': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'type': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'weight': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'})
        },
        'book.organizationindex': {
            'Meta': {'unique_together': "(('school', 'major', 'course', 'content_type', 'object_id'),)", 'object_name': 'OrganizationIndex', 'db_table': "'school_course_index'"},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'course': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['book.Course']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'major': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['book.Major']"}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'school': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['book.School']"})
        },
        'book.school': {
            'Meta': {'ordering': "['-weight']", 'object_name': 'School', 'db_table': "'school'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_end': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'ip_start': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'web': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'weight': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'})
        },
        'book.taxonomy': {
            'Meta': {'ordering': "['-weight']", 'object_name': 'Taxonomy', 'db_table': "'taxonomy'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['book.Taxonomy']", 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'}),
            'weight': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'})
        },
        'book.taxonomyindex': {
            'Meta': {'unique_together': "(('taxonomy', 'content_type', 'object_id'),)", 'object_name': 'TaxonomyIndex', 'db_table': "'taxonomy_index'"},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'taxonomy_indexes'", 'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'taxonomy': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['book.Taxonomy']"})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'shopping.book_deal': {
            'Meta': {'object_name': 'Book_Deal', 'db_table': "'book_deal'"},
            'book': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['book.Book']", 'null': 'True', 'blank': 'True'}),
            'deal': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['shopping.Deal']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'price_buy': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'price_sell': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'type': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'shopping.deal': {
            'Meta': {'object_name': 'Deal', 'db_table': "'deal'"},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'deliverMan': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'deliverTime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'finishTime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '100', 'primary_key': 'True'}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'payway': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'remark': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'resultRemark': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'submitTime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'})
        },
        'shopping.sell_book_deal': {
            'Meta': {'object_name': 'Sell_Book_Deal', 'db_table': "'sell_book_deal'"},
            'book': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['book.Book']", 'null': 'True', 'blank': 'True'}),
            'deal': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['shopping.Sell_Deal']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        'shopping.sell_deal': {
            'Meta': {'object_name': 'Sell_Deal', 'db_table': "'sell_deal'"},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'deliverMan': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'deliverTime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'finishTime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '100', 'primary_key': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'price_all': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'remark': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'resultRemark': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'submitTime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['shopping']