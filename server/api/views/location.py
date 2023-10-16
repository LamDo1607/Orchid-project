from rest_framework.decorators import api_view
import json
import hashlib
import datetime
from dateutil.parser import parse
from api.models import User, LoginSession, Location
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from api.apps import *
import api.auth
from django.conf import settings
from lib.TGMT.TGMTpaging import Paging
from lib.TGMT.TGMTemail import SendEmailAsync

####################################################################################################

@api_view(["POST"])
def GetLocationList(request):
    try:
        _token = GetParam(request, "token")
        loginSession = api.auth.decode(_token)       
            
        _code = GetParam(request, 'code')
        _name = GetParam(request, 'name')
        _level =RequireParamExist(request, 'level')
        _search_string = GetParam(request, 'search_string')
        _owner_pk = GetParam(request, 'owner_pk')

        locations = Location.objects(level=_level, isDeleted=False)

        if(IsPk(_owner_pk)):
            locations = locations(owner_pk=_owner_pk)

        if(_search_string != None and _search_string != ""):
            locations = locations(name__icontains=_search_string)
        
        respond = Paging(request, locations)
        return ObjResponse(respond)
    except Exception as e:
        return ErrorResponse(str(e))
####################################################################################################

@api_view(["POST"])
def UpdateLocation(request):
    try:
        _token = RequireParamExist(request, "token")
        jwt = api.auth.decode(_token)

        _pk = GetParam(request, 'pk')
        _code = GetParam(request, 'code')
        _name = RequireParamExist(request, 'name')
        _level = RequireParamExist(request, 'level')
        _owner_pk = GetParam(request, 'owner_pk')

        location = None
        if(IsPk(_pk)):
            try:
                location = Location.objects.get(pk=_pk, isDeleted=False)
            except Location.DoesNotExist:
                pass

        if(location == None):            
            location = Location( dateCreate = utcnow())
            
        if(IsPk(_owner_pk)):
            owner = Location.objects.get(pk=_owner_pk, isDeleted=False)
            location.owner = owner.name
            location.owner_pk = _owner_pk

        location.code = _code
        location.name = _name
        location.level = _level
        location.save()
        return SuccessResponse("cập nhật thành công")
    except Exception as e:
        return ErrorResponse("Có lỗi: " + str(e))
    
####################################################################################################

@api_view(["POST"])
def DeleteLocation(request):
    try:
        _token = RequireParamExist(request, "token")
        jwt = api.auth.decode(_token)

        _pk = RequireParamExist(request, 'pk')

        if(IsPk(_pk)):
            try:
                location = Location.objects.get(pk=_pk, isDeleted=False)
            except Location.DoesNotExist:
                pass
        location.isDeleted = True 
        location.save()
        return SuccessResponse("Xóa thành công")
    except Exception as e:
        return ErrorResponse("Có lỗi: " + str(e))