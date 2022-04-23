import json, re, bcrypt, jwt

from django.http            import JsonResponse
from django.views           import View
from django.conf            import settings
from users.models           import User
from users.validation       import Validation
from django.core.exceptions import ValidationError
# Create your views here.

class SignUpView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            email          = data['email']
            password       = data['password']
            username       = data['username']
            phonenumber    = data['phonenumber']

            if User.objects.filter(email=email).exists():
                return JsonResponse({'message':'이미가입함'},status=400)
            Validation.email_validate(email)
            Validation.password_validate(password)

            User.objects.create(
                email = email,
                password = bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt()).decode('utf-8'),
                username = username,
                phonenumber = phonenumber,
            )
            return JsonResponse({'message':'가입성공'},status=200)
        except KeyError:
            return JsonResponse({'message':'키에러'},status=400)
        except ValidationError as error:
            return JsonResponse({"message": error.message}, status=400)
class SignInView(View):
    def post(self,request):
        try:
            data = json.loads(request.body)
            user = User.objects.get(email=data['email'])

            if not bcrypt.checkpw(data['password'].encode('utf-8'),user.password.encode('utf-8')):
                return JsonResponse({'message':'비번틀림'},status=400)

            access_token = jwt.encode({'id': user.id}, settings.SECRET_KEY, algorithm = settings.ALGORITHM)

            return JsonResponse({'access token':access_token},status=200)

        except KeyError:
            return JsonResponse({'message':'키에러'},status=400)
        except ValueError:
            return JsonResponse({'message':'밸류에러'},status=400)
        except User.DoesNotExist:
            return JsonResponse({'message':'계정이상함'},status=400)