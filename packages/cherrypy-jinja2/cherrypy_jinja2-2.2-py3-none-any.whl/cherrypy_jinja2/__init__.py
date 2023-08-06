#   Copyright 2015-2016, 2022 University of Lancaster
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import cherrypy

import jinja2


class Jinja2Tool(cherrypy.Tool):
    def __init__(self):
        super().__init__('before_handler', self.execute, priority=30)

        self._environments = {}

    def execute(self, search_path, template):
        if search_path not in self._environments:
            self._environments[search_path] = jinja2.Environment(loader=jinja2.FileSystemLoader(search_path))

        environment = self._environments[search_path]
        _template = environment.get_or_select_template(template)

        inner_handler = cherrypy.serving.request.handler

        def wrapper(*args, **kwargs):
            return _template.render(inner_handler(*args, **kwargs))

        cherrypy.serving.request.handler = wrapper


cherrypy.tools.jinja2 = Jinja2Tool()
