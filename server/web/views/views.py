import json
from django.shortcuts import render, redirect
from django.http import HttpResponse, StreamingHttpResponse
from rest_framework.decorators import api_view
from api.models import LoginSession, Org, User
import datetime, time
from django.conf import settings
from api.views.loginsession import FindLoginSession
import api.auth
from lib.TGMT.TGMTutil import GetSystemInfo

def changepassword(request):
    permissions = ["all"]
    return CheckToken(request, 'changepassword.html', permissions)

def histories(request):
    permissions = ["all"]
    return CheckToken(request, 'histories.html', permissions)

def option(request):
    permissions = ["all"]
    return CheckToken(request, 'option.html', permissions)

def orchid(request):
    permissions = ["all"]
    return CheckToken(request, 'orchid.html', permissions)

def activity(request):
    permissions = ["all"]
    return CheckToken(request, 'activity.html', permissions)


def location(request):
    permissions = ["all"]
    return CheckToken(request, 'location.html', permissions)

def orgs(request):
    permissions = ["Root", "Admin"]
    return CheckToken(request, 'orgs.html', permissions)

def log(request):
    permissions = ["Root", "Admin"]
    return CheckToken(request, 'log.html', permissions)

def species(request):
    permissions = ["Root", "Admin"]
    return CheckToken(request, 'species.html', permissions)

@api_view(["POST", "GET"])
def login(request):
    permissions = ["Root", "Admin", "Gate", "Supporter"]
    return CheckToken(request, 'dashboard.html', permissions)

def logout(request):
    try:        
        _token = request.COOKIES.get('token')
        loginSession = LoginSession.objects.get(token=_token, isDeleted = False)
        loginSession.isDeleted = True
        loginSession.save()        
    except Exception as e:
        print(str(e))

    res = redirect('/login')
    res.delete_cookie('token')
    res.delete_cookie('email')
    return res

def index(request):
    args = GetSystemInfo()
    
    permissions = ["Root", "Admin"]
    return CheckToken(request, 'dashboard.html', permissions, args)

def register(request):
    _token = request.COOKIES.get('token')
    if(_token == None or _token == ""):
        args = {'authorized': False}
        response = render(request, 'register.html', args)
        return response
    else:
        return redirect("/")
    
def Redirect(request):
        args = {
            'authorized': False,
            'version' : settings.VERSION,
            }
        return render(request, 'redirect.html' , args)

def users(request):
    args = {"orgs" : []}
    orgs = Org.objects(isDeleted=False)
    args["orgs"] = orgs.to_json()
    print(args)
    permissions = ["Root", "Admin"]
    return CheckToken(request, 'users.html', permissions, args)

def camera(request):
    permissions = ["Root", "Admin", "Gate", "Supporter"]
    return CheckToken(request, 'camera.html', permissions)

def gallery(request):
    permissions = ["Root", "Admin", "Gate", "Supporter"]
    return CheckToken(request, 'gallery.html', permissions)

def webcam(request):
    permissions = ["Root", "Admin", "Gate", "Supporter"]
    return CheckToken(request, 'webcam.html', permissions)

def predict(request):
    permissions = ["Root", "Admin", "Gate", "Supporter"]
    return CheckToken(request, 'predict.html', permissions)

def profile(request):
    permissions = ["Root", "Admin", "Gate", "Supporter"]
    return CheckToken(request, 'profile.html', permissions)

def upload(request):
    permissions = ["Root", "Admin"]
    return CheckToken(request, 'upload.html', permissions)

def system_info(request):
    args = GetSystemInfo()
    
    permissions = ["Root", "Admin"]
    return CheckToken(request, 'system_info.html', permissions, args)

def Redirect(request):
    args = {
        'authorized': False,
        'version' : settings.VERSION,
        }
    return render(request, 'redirect.html' , args)
    
def CheckToken(request, redirect_page, permissions, args = {}):    
    isValidToken = False
    user = None

    args['debug'] = settings.DEBUG
    args['authorized'] = False
    args['version'] = settings.VERSION,


    if("all" in permissions):
        isValidToken = True

    if(not isValidToken):
        loginSession = GetLoginSession(request)
        if loginSession != None:
            args['level'] = loginSession["level"]
            args['email'] = loginSession["email"]

            isValidToken = loginSession["level"] in permissions

        
    
    if(isValidToken):
        args['authorized'] = True
        return render(request, redirect_page , args)
    else:        
        args['fullscreen'] = True
        response = render(request, 'login.html', args)
        response.delete_cookie('token')
        response.delete_cookie('email')
        return response


def IsValidToken(request):
    try:
        _token = request.COOKIES.get('token')
        if(_token == None or _token == ""):
            _token = request.GET.get('token')
        if(_token == None or _token == ""):
            return False

        api.auth.decode(_token)
        return True
    except Exception as e:
        print(str(e))
        return False



def GetLoginSession(request):
    try:
        _token = request.COOKIES.get('token')
        if(_token == None or _token == ""):
            _token = request.GET.get('token')
        if(_token == None or _token == ""):
            return None

        loginSession = FindLoginSession(_token)
        return loginSession
    except Exception as e:
        print(str(e))

    return None



def stream(request):
    def event_stream():
        while True:
            time.sleep(0.1)
            result = {
                'backend_time' : (datetime.datetime.utcnow() + datetime.timedelta(hours = 7)).strftime("%Y-%m-%d %H:%M:%S"),
                'num_face' : settings.NUM_FACE,
            }
            yield 'data: ' + json.dumps(result) + '\n\n'
    return StreamingHttpResponse(event_stream(), content_type='text/event-stream')