from email.mime import image
import json, re

from django.views    import View
from django.http     import JsonResponse
from users.models    import User
from postings.models import Posting, Image
from json.decoder    import JSONDecodeError

class PostingView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            user = User.objects.get(email=data.get('user',None))
            content = data.get('content',None)
            image_url_list = data.get('image_url',None)

            if not (user and image_url_list):
                return JsonResponse({'message':'에러!!'}, status=400)

            posting = Posting.objects.create(
                user    = user,
                content = content,
            )

            return JsonResponse({'message':'성공'},status=200)
        except JSONDecodeError:
            return JsonResponse({'meaage':'디코드에러!!'}, status=400)

    def get(self, request):
        posting_list = [{
            'username'  : User.objects.get(id=posting.user.id).username,
            'content'   : posting.content,
            'image_url' : [i.image_url for i in Image.objects.filter(posting_id=posting.id)],
            'create_at' : posting.create_at
            } for posting in Posting.objects.all()
        ]

        return JsonResponse({'data':posting_list},status=200)


# Create your views here.
