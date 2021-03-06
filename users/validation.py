from django.http import JsonResponse
import re
from users.models import User
from django.core.exceptions import ValidationError

regex_email    = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9_-]+\.[a-zA-Z0-9-.]+$'
regex_password =  "^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$"

class Validation:
    def email_validate(value):
        if not re.match(regex_email,value):
            raise ValidationError('이메일이상함')

    def password_validate(value):
        if not re.match(regex_password,value):
            raise ValidationError('비번틀림')