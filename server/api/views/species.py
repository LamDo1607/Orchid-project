from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json
import hashlib
import datetime
import api.auth
from api.models import Species, User, LoginSession
from api.apps import *
from api.views.loginsession import *
#from api.views.activity import AddActivity
from lib.TGMT.TGMTpaging import Paging
from unidecode import unidecode
from mongoengine.queryset.visitor import Q

####################################################################################################

@api_view(["POST"])           
def UpdateSpecies(request):
    try:
        _token = GetParam(request, "token")
        loginSession = api.auth.decode(_token)
        
        RequireLevel(loginSession, ["Root", "Admin"])
        
        _pk = GetParam(request, "pk") 
        _vietnamesename = GetParam(request, "vietnamesename") 
        _englishname = RequireParamExist(request, "englishname", "tên khoa học")    
        _description = GetParam(request, "description") 


        isExist = False
        species = None
        if(IsPk(_pk)):
            try:
                species = Species.objects.get(pk=_pk, isDeleted=False)
                isExist = True
            except Species.DoesNotExist:
                pass
            

        if(species == None):
            species = Species(englishname =_englishname, vietnamesename =_vietnamesename, description = _description)
          #  species = Species(vietnamesename =_vietnamesename)

        if(_englishname != None and _englishname != ""):
            species.englishname = _englishname

        if(_vietnamesename != None and _vietnamesename != ""):
            _vietnamesename_ascii = unidecode(_vietnamesename)
            species.vietnamesename = _vietnamesename
            species.vietnamesename_ascii = _vietnamesename_ascii
            
        if(_description != None and _description != ""):
            species.description = _description

        species.save()

        if(isExist):
            return SuccessResponse("Câp nhật thành công")
        else:
            return SuccessResponse("Thêm thành công")
    except Exception as e:
        return ErrorResponse(str(e))

####################################################################################################

@api_view(["POST"])           
def GetSpecies(request):
    try:
        _token = GetParam(request, "token")
        loginSession = FindLoginSession(_token) 
        
        speciesList = Species.objects(isDeleted=False)
        
        _search_string = GetParam(request, 'search_string')
        if(_search_string != None and _search_string != ""):
            _search_string_ascii = unidecode(_search_string)
            speciesList = speciesList.filter(Q(englishname__icontains=_search_string) |
                                             Q(vietnamesename__icontains=_search_string) |
                                             Q(vietnamesename_ascii__icontains=_search_string_ascii))

        respond = Paging(request, speciesList)
        return ObjResponse(respond)
    except Exception as e:
        return ErrorResponse("Có lỗi: "+ str(e))       

####################################################################################################

@api_view(["POST"])           
def RemoveSpecies(request):
    try:
        _token = GetParam(request, "token")
        loginSession = FindLoginSession(_token)

        _pk = RequireParamExist(request, "pk") #  

    
        species = Species.objects.get(pk=_pk)
        
        species.isDeleted =  True
        species.save()

        return SuccessResponse("Xóa thành công")
    except Exception as e:
        return ErrorResponse("Có lỗi: " + str(e))
