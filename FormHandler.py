"""Creates a simple signup page with rudimentary validation and redirection."""
from BaseHandler import Handler
import re
from models import User


USER_RE = re.compile(r"[a-zA-Z0-9_-]{3,20}$")
PASSWORD_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")


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

    def form_verified(self):
        """Called when form is verified."""
        # Make sure user doesn't already exist
        user = User.get_user_by_name(self.user_name)
        if user:
            message = "That user already exists."
            self.render('signup.html', error_username=message)
        else:
            # Create user object in database
            user = User.register(
                self.user_name,
                self.user_password,
                self.user_email)
            user.put()

            # Log the user in and redirect to welcome page
            self.login(user)
            self.redirect('/welcome')

    def get(self):
            self.render("signup.html")

    def post(self):
        """Validates user input and return errors if tests fail"""
        self.user_name = self.request.get("username")
        self.user_password = self.request.get("password")
        self.user_verify = self.request.get("verify")
        self.user_email = self.request.get("email")

        # Error messages
        username_error = "" if self.valid_username(self.user_name) else "Please enter a valid username."
        password_error = "" if self.valid_password(self.user_password) else "Please enter a valid password."
        verify_error = "" if self.verify_password(self.user_password, self.user_verify) else "Your passwords do not match."
        email_error = "" if self.valid_email(self.user_email) else "That's not a valid email."
        # If there are no error messages
        if username_error == "" and password_error == "" and verify_error == "":
            # Call method done() and redirect to welcome
            self.form_verified()

        else:
            # Otherwise re render form
            self.render('signup.html',
                        username_error=username_error,
                        password_error=password_error,
                        verify_error=verify_error,
                        email_error=email_error)
