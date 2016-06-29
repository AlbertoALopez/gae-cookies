"""Base handler."""
import webapp2
import os
import jinja2

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), 'templates')
JINJA_ENV = jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATE_DIR),
                               autoescape=True)

class Handler(webapp2.RequestHandler):
    """Provides convenience functions for rendering templates and strings."""
    def write(self, *a, **kw):
        """Writes to page."""
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        """Takes a string as parameter finds the matching jinja template."""
        t = JINJA_ENV.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        """Renders the jinja template with the given parameters."""
        self.write(self.render_str(template, **kw))
