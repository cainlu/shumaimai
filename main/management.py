#coding=utf-8

import traceback

from django.db.models.signals import post_syncdb
from django.db import connection
from django.dispatch import receiver
from django.db.models.signals import *
from django.core.signals import * 

import models as main_models

#search_indexes_has_set_up = False
#
#@receiver(post_syncdb)
#def set_up_search_indexes(**kwargs):
#    global search_indexes_has_set_up
#    if not search_indexes_has_set_up:
#        created_models = kwargs['created_models']
#        for mo in created_models:
#            try:
#                meta = mo._meta
#                if hasattr(meta, 'search_indexes'):
#                    search_indexes = meta.search_indexes
#                    for k, v in search_indexes.items():
#                        table_name = str(meta.db_table)
#                        index_name = str(k)
#                        index_fields = [meta.get_field(name, many_to_many=False).column for name in v]
#                        index_fields_wrapped = ['`' + str(name) + '`' for name in index_fields]
#                        index_fields_str = ",".join(index_fields_wrapped)
#                        cursor = connection.cursor()
#                        cursor.execute("SHOW INDEX FROM `" + table_name + "` WHERE `Key_name`='" + index_name + "';")
#                        rows = cursor.fetchall()
#                        if len(rows) == 0:
#                            print 'Creating fulltext index "' + index_name + '" on table "' + table_name + '"'
#                            cursor.execute("ALTER TABLE `" + table_name + "` ADD FULLTEXT INDEX `" + index_name + "` (" + index_fields_str + "); ")
#                            #cursor.execute("ALTER TABLE `" + table_name + "` ADD FULLTEXT INDEX `" + index_name + "` (" + index_fields_str + ") WITH PARSER mysqlcft; ")
#            except Exception, e:
#                print e
#                print traceback.print_exc()
#
#        search_indexes_has_set_up = True
#        print "Set up search indexes done."
#
