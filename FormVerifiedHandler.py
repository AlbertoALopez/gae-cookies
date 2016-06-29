"""Handler for valid form redirect."""
from BaseHandler import Handler


class FormVerified(Handler):
    """Verifies if there is a valid user signed in and redirects."""
    def get(self):
        if self.user:
            # Render page with valid username
            self.render('welcome.html', username=self.user.name)
        else:
            self.redirect('/signup')

# """Handler for front page."""
#
# def get(self):
#     # Set header response to plain text
#     self.response.headers['Content-Type'] = 'text/plain'
#     visits = 0
#     # Create a visits object which accesses the previously set cookie
#     visit_cookie_str = self.request.cookies.get('visits')
#     # If we have a cookie
#     if visit_cookie_str:
#         # Decode cookie
#         cookie_val = check_secure_val(visit_cookie_str)
#         if cookie_val:
#             # Convert to int and store cookie value in visits
#             visits = int(cookie_val)
#
#     visits += 1
#     # Make new secure cookie
#     new_cookie_val = make_secure_val(str(visits))
#     # Set cookie for visit
#     self.response.headers.add_header('Set-Cookie', 'visits=%s' % new_cookie_val)
#
#     if visits > 1000:
#         self.write('meow!')
#     else:
#         self.write("You've been here %s times!" % visits)
