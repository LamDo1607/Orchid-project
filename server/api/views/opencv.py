from rest_framework.decorators import api_view
from rest_framework.response import Response
import os
import base64
import datetime, time
from dateutil.parser import parse
from api.models import Level, User
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from api.apps import *
from lib.TGMT.TGMTimage import SaveImageFromRequest
from django.conf import settings
import cv2

####################################################################################################

@api_view(["POST"])           
def DetectFace(request):
    try:
        folder = "uploaded_image"
        _randFilename = datetime.datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S") + "_" + GenerateRandomString() + ".jpg"
        uploaded_file_abs = os.path.join(settings.MEDIA_ROOT, folder, _randFilename)

        SaveImageFromRequest(request, folder, _randFilename)

        startTime = time.time()

        mat = cv2.imread(uploaded_file_abs)
        mat, rects = DetectFaceByCascade(mat)

        elapsed = time.time() - startTime
        elapsed = round(elapsed, 2)

        retval, buffer = cv2.imencode('.jpg', mat)
        strBase64 = base64.b64encode(buffer)
        
        return Response(
            {'image_base64': strBase64,
            'elapsed' : elapsed},
            status=SUCCESS_CODE,
            content_type="application/json")
        
    except Exception as e:
        return ErrorResponse("Có lỗi: " + str(e))

