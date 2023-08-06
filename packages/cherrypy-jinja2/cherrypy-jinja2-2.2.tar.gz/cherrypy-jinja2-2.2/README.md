CherryPy-Jinja2
===============

CherryPy-Jinja2 is a simple CherryPy Tool to render output via Jinja2 templates.

Import `cherrypy_jinja2` to make the tool available in CherryPy's default toolbox.

Set `tools.jinja2.search_path` to a directory containing Jinja2 template files,
then attach the tool to exposed methods:

    class Root:
        @cherrypy.expose
        @cherrypy.tools.jinja2(template="index.html")
        def index(self):
            return {'message': "Hello"}
