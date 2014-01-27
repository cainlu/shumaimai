#coding=utf-8

import re

from django.conf import settings
from django.http import *

from compressor.templatetags.compress import CompressorMixin


class StaticFileMiddleware(object):

    def get_original_content(self, context):
        return context['original_content']

    def js_file_processor(self, html):
        p_js_node = re.compile('<script .*combine.*>')
        return self.node_processor(p_js_node, html, 'js')


    def css_file_processor(self, html):
        p_css_node = re.compile('<link .*combine.*>')
        return self.node_processor(p_css_node, html, 'css')

    def node_processor(self, p, html, kind):
        html_clean = p.sub(repl="", string=html)
        file_node_list = list(set(p.findall(html)))
        return self.node_render(file_node_list, html_clean, kind)


    def node_render(self, file_node_list, html, kind):
        """ reader the file nodes before '</head>' """
        file_html = ' '.join(file_node_list)
        try:
            file_html = file_html.decode('utf-8')
        except:
            pass
        context = {
            'original_content':file_html
        }
        compressor = CompressorMixin()
        compressor.get_original_content = self.get_original_content
        target = compressor.render_compressed(context, kind, 'file', False)
        res = html.replace('</head>', target + '\n</head>')
        return res

    def process_response(self, request, response):
        try:
            if response.status_code == 200 and response['Content-Type'].find('text/html') >= 0:
                return HttpResponse(self.js_file_processor(self.css_file_processor(response.content)))
        except Exception, e:
            pass
        return response



