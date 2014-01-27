# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Taxonomy'
        db.create_table('taxonomy', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('type', self.gf('django.db.models.fields.SmallIntegerField')(default=1)),
            ('weight', self.gf('django.db.models.fields.SmallIntegerField')(default=1)),
            ('level', self.gf('django.db.models.fields.SmallIntegerField')(default=1)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['book.Taxonomy'], null=True, blank=True)),
        ))
        db.send_create_signal('book', ['Taxonomy'])

        # Adding model 'TaxonomyIndex'
        db.create_table('taxonomy_index', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('taxonomy', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['book.Taxonomy'])),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='taxonomy_indexes', to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal('book', ['TaxonomyIndex'])

        # Adding unique constraint on 'TaxonomyIndex', fields ['taxonomy', 'content_type', 'object_id']
        db.create_unique('taxonomy_index', ['taxonomy_id', 'content_type_id', 'object_id'])

        # Adding model 'Book'
        db.create_table('book', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100, db_index=True)),
            ('subtitle', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('author', self.gf('django.db.models.fields.CharField')(max_length=50, db_index=True)),
            ('translator', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=100, blank=True)),
            ('isbn', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=25, null=True, blank=True)),
            ('press', self.gf('django.db.models.fields.CharField')(max_length=100, db_index=True)),
            ('publication_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('version', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('language', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('number', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, db_index=True)),
            ('page_number', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('size', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('binding', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('recommend', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('price_ori', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('price_now', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('status', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
        ))
        db.send_create_signal('book', ['Book'])

        # Adding model 'School'
        db.create_table('school', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('web', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('weight', self.gf('django.db.models.fields.SmallIntegerField')(default=1)),
            ('region', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('ip_start', self.gf('django.db.models.fields.IPAddressField')(max_length=15, null=True, blank=True)),
            ('ip_end', self.gf('django.db.models.fields.IPAddressField')(max_length=15, null=True, blank=True)),
        ))
        db.send_create_signal('book', ['School'])

        # Adding model 'Major'
        db.create_table('major', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('type', self.gf('django.db.models.fields.SmallIntegerField')(default=0)),
            ('diploma', self.gf('django.db.models.fields.SmallIntegerField')(default=0)),
            ('weight', self.gf('django.db.models.fields.SmallIntegerField')(default=1)),
        ))
        db.send_create_signal('book', ['Major'])

        # Adding unique constraint on 'Major', fields ['name', 'type', 'diploma']
        db.create_unique('major', ['name', 'type', 'diploma'])

        # Adding model 'Course'
        db.create_table('course', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('weight', self.gf('django.db.models.fields.SmallIntegerField')(default=1)),
        ))
        db.send_create_signal('book', ['Course'])

        # Adding model 'OrganizationIndex'
        db.create_table('school_course_index', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('school', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['book.School'])),
            ('major', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['book.Major'])),
            ('course', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['book.Course'], null=True, blank=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal('book', ['OrganizationIndex'])

        # Adding unique constraint on 'OrganizationIndex', fields ['school', 'major', 'course', 'content_type', 'object_id']
        db.create_unique('school_course_index', ['school_id', 'major_id', 'course_id', 'content_type_id', 'object_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'OrganizationIndex', fields ['school', 'major', 'course', 'content_type', 'object_id']
        db.delete_unique('school_course_index', ['school_id', 'major_id', 'course_id', 'content_type_id', 'object_id'])

        # Removing unique constraint on 'Major', fields ['name', 'type', 'diploma']
        db.delete_unique('major', ['name', 'type', 'diploma'])

        # Removing unique constraint on 'TaxonomyIndex', fields ['taxonomy', 'content_type', 'object_id']
        db.delete_unique('taxonomy_index', ['taxonomy_id', 'content_type_id', 'object_id'])

        # Deleting model 'Taxonomy'
        db.delete_table('taxonomy')

        # Deleting model 'TaxonomyIndex'
        db.delete_table('taxonomy_index')

        # Deleting model 'Book'
        db.delete_table('book')

        # Deleting model 'School'
        db.delete_table('school')

        # Deleting model 'Major'
        db.delete_table('major')

        # Deleting model 'Course'
        db.delete_table('course')

        # Deleting model 'OrganizationIndex'
        db.delete_table('school_course_index')


    models = {
        'book.book': {
            'Meta': {'ordering': "['id']", 'object_name': 'Book', 'db_table': "'book'"},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'}),
            'binding': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'isbn': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'}),
            'number': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'db_index': 'True'}),
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
        }
    }

    complete_apps = ['book']