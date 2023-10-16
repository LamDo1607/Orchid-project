import base64
from rest_framework.decorators import api_view
from PIL import Image
import os
import datetime, time
from dateutil.parser import parse
from api.models import History
# from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from api.apps import *
import api.auth
from lib.TGMT.TGMTutil import GenerateRandomString
from lib.TGMT.TGMTimage import SaveImageFromRequest
from django.conf import settings


####################################################################################################


@api_view(["POST"])           
def DetectBeverage(request):
    try:
        _token = GetParam(request, "token")
        loginSession = api.auth.decode(_token)

        inputImgPath = os.path.join(settings.MEDIA_ROOT, "buildings2.jpg")



        return SuccessResponse("aaa")
    except Exception as e:
        return ErrorResponse("Có lỗi: " + str(e))