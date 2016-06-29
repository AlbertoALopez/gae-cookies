"""Creates a simple signup page with rudimentary validation and redirection."""
from BaseHandler import Handler
import re
import hmac
from secret import SECRET


USER_RE = re.compile(r"[a-zA-Z0-9_-]{3,20}$")
PASSWORD_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")

def hash_str(s):
    """Hashes a string produced with hmac."""
    return hmac.new(SECRET, s).hexdigest()


def make_secure_val(s):
    """Returns a string of format s,HASH."""
    return "%s|%s" % (s, hash_str(s))


def check_secure_val(h):
    """Checks if the given hash is secure and valid."""
    string = h.split('|')[0]
    if h == make_secure_val(string):
        return string
    else:
        return None

class FormHandler(Handler):
    def valid_username(self, username):
        """Returns true if matches a valid username"""
        return username and USER_RE.match(username)

    def valid_password(self, password):
        """Returns true if matches valid password"""
        return password and PASSWORD_RE.match(password)

    def verify_password(self, first_password, verify):
        """Returns true if both passwords match"""
        return first_password and verify and first_password == verify

    def valid_email(self, email):
        """Returns true if matches valid email"""
        return not email or EMAIL_RE.match(email)

    def get(self):
            self.render("signup.html")

    def post(self):
        """Validates user input and return errors if tests fail"""
        user_name = self.request.get("username")
        user_password = self.request.get("password")
        user_verify = self.request.get("verify")
        user_email = self.request.get("email")

        # Error messages
        username_error = "" if self.valid_username(user_name) else "Please enter a valid username."
        password_error = "" if self.valid_password(user_password) else "Please enter a valid password."
        verify_error = "" if self.verify_password(user_password, user_verify) else "Your passwords do not match."
        email_error = "" if self.valid_email(user_email) else "That's not a valid email."

        if username_error == "" and password_error == "" and verify_error == "":
            self.response.headers['Content-Type'] = 'text/plain'
            user_id_string = user_name
            new_cookie_val = make_secure_val(str(user_id_string))
            # Set cookie for visit
            self.response.headers.add_header('Set-Cookie', 'user_id=%s, Path=/' % new_cookie_val)
            self.redirect('/welcome')

        else:
            self.render('signup.html',
                        username_error=username_error,
                        password_error=password_error,
                        verify_error=verify_error,
                        email_error=email_error)
