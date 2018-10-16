import cherrypy
from mako.template import Template
import crawler
import os


class Main(object):
    @cherrypy.expose
    def index(self, *args, **kwargs):
        data = {}
        if kwargs.get('search'):
            c = crawler.Crawler()
            r = c.fetch(kwargs['search'])
            data['recipes'] = r
            data['search'] = kwargs['search']
        mytemplate = Template(filename='search.html')
        return mytemplate.render(**data)


cherrypy.config.update({
    'server.socket_port': 8080,
    'tools.encode.on': True,
    'tools.encode.encoding': 'utf-8'
    })
conf = {
    '/': {'tools.staticdir.root': os.path.abspath(os.getcwd())},
    '/css': {
        'tools.staticdir.on':True,
        'tools.staticdir.dir':"css"
    },
    '/js': {
        'tools.staticdir.on':True,
        'tools.staticdir.dir':"js"
    }
}
if __name__ == '__main__':
    cherrypy.tree.mount(Main(), '/', conf)
    cherrypy.engine.start()
    cherrypy.engine.block()
