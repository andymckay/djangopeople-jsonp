#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#




import wsgiref.handlers
from google.appengine.ext import webapp

import parse
from django.utils import simplejson as json

class JSONHandler(webapp.RequestHandler):
    def get(self):
        name = self.request.get("name")
        if not name:
            self.response.out.write("Specify a name")
            self.response.set_status(500)
            return
        try:
            data = json.dumps(parse.parse(name))
        except parse.DjangoPeopleError, err:
            self.response.out.write("DjangoPeopleError")
            self.response.set_status(err.code)
            return
            
        if self.request.get("callback"):
            data = "%s(%s)" % (self.request.get("callback"), data)
        self.response.out.write(data)

if __name__ == '__main__':
    application = webapp.WSGIApplication([
        ('/', JSONHandler)
        ], debug=True)
    wsgiref.handlers.CGIHandler().run(application)

