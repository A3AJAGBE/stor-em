from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, validators, TextAreaField


class RegisterForm(FlaskForm):
    business_name = StringField("Business Name: ", [validators.InputRequired(message="This field cannot be empty."),
                                                    validators.Length(min=3, max=50,
                                                                      message="Business name must be between 3 to 50 "
                                                                              "characters.")
                                                    ])
    email = StringField("Email Address: ", [validators.InputRequired(message="This field cannot be empty."),
                                            validators.Email(message="That is not a valid email address.")])
    password = PasswordField("Password: ", [validators.InputRequired(message="This field cannot be empty."),
                                            validators.Length(min=8,
                                                              message="Password must be at least 8 characters.")])
    submit = SubmitField("Create account")


class LoginForm(FlaskForm):
    email = StringField("Email Address: ", [validators.InputRequired(message="This field cannot be empty."),
                                            validators.Email(message="That is not a valid email address.")])
    password = PasswordField("Password: ", [validators.InputRequired(message="This field cannot be empty."),
                                            validators.Length(min=8,
                                                              message="Password must be at least 8 characters.")])
    submit = SubmitField("Login")


class NewEmailConfirmationRequestForm(FlaskForm):
    email = StringField("Registered Email Address: ", [validators.InputRequired(message="This field cannot be empty."),
                                                       validators.Email(message="That is not a valid email address.")])
    submit = SubmitField("Submit request")


class ResetPasswordRequestForm(FlaskForm):
    email = StringField("Registered Email Address: ", [validators.InputRequired(message="This field cannot be empty."),
                                                       validators.Email(message="That is not a valid email address.")])
    submit = SubmitField("Submit request")


class ResetPasswordForm(FlaskForm):
    password = PasswordField("New Password: ", [validators.InputRequired(message="This field cannot be empty."),
                                                validators.Length(min=8,
                                                                  message="Password must be at least 8 characters.")])
    submit = SubmitField("Reset password")


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField("Old Password: ", [validators.InputRequired(message="This field cannot be empty."),
                                                    validators.Length(min=8,
                                                                      message="Password must be at least 8 characters.")])
    new_password = PasswordField("New Password: ", [validators.InputRequired(message="This field cannot be empty."),
                                                    validators.Length(min=8,
                                                                      message="Password must be at least 8 characters.")])
    submit = SubmitField("Change password")


class MerchantForm(FlaskForm):
    merchant_name = StringField("Merchant Name: ", [validators.InputRequired(message="This field cannot be empty."),
                                                    validators.Length(min=3, max=50,
                                                                      message="merchant name must be between 3 to 50 "
                                                                              "characters.")
                                                    ])
    contact_name = StringField("Contact Name: ")
    email = StringField("Email Address: ")
    phone_number = StringField("Phone Number: ", [validators.InputRequired(message="This field cannot be empty.")])
    submit = SubmitField("Submit")


class CustomerForm(FlaskForm):
    customer_name = StringField("Customer Name: ", [validators.InputRequired(message="This field cannot be empty."),
                                                    validators.Length(min=3, max=50,
                                                                      message="Customer name must be between 3 to 50 "
                                                                              "characters.")
                                                    ])
    email = StringField("Email Address: ")
    phone_number = StringField("Phone Number: ")
    submit = SubmitField("Submit")
