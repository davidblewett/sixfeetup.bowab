# The API that should be available to templates.

import datetime

from pyramid.security import authenticated_userid


class TemplateAPI(object):
    def __init__(self, request, rendering_val):
        if not request:
            return
        self.request = request
        self.init_forms(rendering_val)

    @property
    def settings(self):
        return self.request.registry.settings

    @property
    def utc_now(self):
        # totally naive as to timezone.
        return datetime.datetime.utcnow()

    def init_forms(self, rendering_val):
        # Initialize any necessary form resources
        self.css_resources = []
        self.js_resources = []
        for form in rendering_val.get('forms', []):
            resources = form.get_widget_resources()
            # XXX: Is the path always going to have this prefix?
            self.css_resources.extend([
                'deform:static/%s' % css_path
                for css_path in resources['css']
            ])
            self.js_resources.extend([
                'deform:static/%s' % js_path
                for js_path in resources['js']
            ])
        print "Ran init_forms"

    def is_active_tab(self, route_name):
        if self.request.matched_route and \
           self.request.matched_route.name == route_name:
            return 'active'
        else:
            return ''

    @property
    def current_userid(self):
        userid = authenticated_userid(self.request)
        if not userid:
            return ''
        return userid
