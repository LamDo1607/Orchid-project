from rest_framework.decorators import api_view
import json
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os
from api.apps import *
from lib.TGMT.TGMTimage import *
from lib.TGMT.TGMTutil import *

####################################################################################################

def GetThumbnailByExt(ext):
    if ext == ".pdf":
        return "/static/img/pdf.png"
    elif ext == ".doc" or ext == ".docx":
        return "/static/img/word.png"
    elif ext == ".xls" or ext == ".xlsx":
        return "/static/img/excel.png"
    elif ext == ".rar" or ext == ".zip" or ext == ".7z":
        return "/static/img/compress.png"
    else:
        return "/static/img/file.png"

####################################################################################################

@api_view(["POST"])           
def JoditUpload(request):
    try:
        saveDir = "joditUpload"

        uploadFile = request.FILES['files[0]']
        fileName = GenerateRandomName(str(uploadFile))


        upload_folder_abs = os.path.join(settings.MEDIA_ROOT, saveDir)
        fs = FileSystemStorage(upload_folder_abs, settings.MEDIA_URL)
        filename = fs.save( fileName, uploadFile)

        result = {"success": True,
                "time": utcnow(),
                "data":
                    {"baseurl": "/media/joditUpload/",
                    "messages":[],
                    "files":[filename],
                    "isImages":[True],
                    "code":220},
                "elapsedTime": None}

        return ObjResponse(result)
   
    except Exception as e:
        return ErrorResponse(str(e))