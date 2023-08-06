import sys

sys.path.append('..')

import cherrypy  # noqa: E402
import cherrypy_jinja2  # noqa: E402,F401


class Root:
    @cherrypy.expose
    @cherrypy.tools.jinja2(template="index.html")
    def index(self):
        return {'message': "Hello"}


if __name__ == '__main__':
    cherrypy.quickstart(Root(), '/', {'/': {'tools.jinja2.search_path': '.'}})
