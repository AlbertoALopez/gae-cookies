"""Hashing and cookie setting example."""
import webapp2
from BaseHandler import Handler
from FormHandler import FormHandler
from FormVerifiedHandler import FormVerifiedHandler
from LoginHandler import LoginHandler
from LogoutHandler import LogoutHandler


class MainPage(Handler):
    """Handler for front page."""

    def get(self):
        # Get user id cookie
        user_id_string = self.request.cookies.get('user_id')
        # If we have a cookie
        if user_id_string:
            # Redirect to welcome page
            self.redirect('/welcome')
        else:
            # Redirect to signup page
            self.redirect('/signup')

app = webapp2.WSGIApplication([('/', MainPage),
                               ('/signup', FormHandler),
                               ('/welcome', FormVerifiedHandler),
                               ('/login', LoginHandler),
                               ('/logout', LogoutHandler)], debug=True)
