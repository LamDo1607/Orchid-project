from mongoengine import Document, ListField, StringField, DateTimeField, BooleanField, EmailField, DictField, FloatField

################################################################
#No.1
LEVELS = (
    'Root',
    'Admin', #register
    'Gate', #admin create
    'Supporter' #root create
)

USER_STATUS = (
    'Registered',
    'Verified', #verify by phone number
    'Approved', #root approve
    'Suspend',
    'Invited'
)

class User(Document):    
    email               =  StringField()
    fullname            =  StringField()
    position            =  StringField()
    password            =  StringField()
    phone               =  StringField()
    owner               =  StringField()
    orgName             =  StringField()
    org_pk              =  StringField()
    secretkey           =  StringField()
    level               =  StringField() #, choices=LEVELS
    status              =  StringField() #, choices=USER_STATUS
    timeRegister        =  DateTimeField()
    timeUpdate          =  DateTimeField()
    suspendReason       =  StringField()
    isDeleted           =  BooleanField(default = False)
    

################################################################
#No.2
class Level(Document):
    levelID             =  StringField()
    levelName           =  StringField()

################################################################
#No.3
class Option(Document):
    optionName          =  StringField()
    value               =  StringField()
  
################################################################
GENDERS = (
    'Male',
    'Female',
    'undefined',
)
STATE = (
    'Checked_in',
    'Checked_out',
    'Visitor'
)
PERSON_TYPE = (
    'Staff',
    'Guest',
)

################################################################

class LoginSession(Document):
    token               =  StringField()
    email               =  StringField()
    level               =  StringField()
    fullname            =  StringField()
    loginTime           =  DateTimeField()
    logoutTime          =  DateTimeField()
    platform            =  StringField()
    purpose             =  StringField()
    validTo             =  DateTimeField()
    isDeleted           =  BooleanField(default=False)

################################################################

class History(Document):
    inputPath           =  StringField()
    outputPath          =  StringField()
    email               =  StringField()
    fullname            =  StringField()
    results             =  ListField(DictField())
    timeCreate          =  DateTimeField()
    elapsed             =  FloatField()
    isDeleted           =  BooleanField(default=False)

################################################################
LOCATIONLEVELS =(
    'Tỉnh',
    'Huyện',
    'Xã'
)

class Location(Document):
    name               =  StringField()
    code               =  StringField()
    level              =  StringField(choices=LOCATIONLEVELS)
    owner              =  StringField()
    owner_pk           =  StringField()
    dateCreate         =  DateTimeField()
    dateUpdate         =  DateTimeField()
    isDeleted          =  BooleanField(default=False)

################################################################

class Orchid(Document):
    name               =  StringField()
    scienceName        =  StringField()
    author             =  StringField()
    address            =  StringField()
    note               =  StringField()    
    dateCreate         =  DateTimeField()
    dateUpdate         =  DateTimeField()
    isDeleted          =  BooleanField(default=False)

################################################################

class Log(Document):
    activity            =  StringField(required=True)
    exception           =  StringField(required=True)
    timeCreate          =  DateTimeField(required=True)
    isDeleted           =  BooleanField(default=False)

################################################################

class Org(Document):
    name                =  StringField(required=True)
    name_ascii          =  StringField()
    address             =  StringField()
    manager             =  StringField()
    manager_ascii       =  StringField()
    position            =  StringField()
    phone1              =  StringField() # User group
    phone2              =  StringField() # Presenter
    timeCreate          =  DateTimeField()
    isDeleted           =  BooleanField(default=False)

################################################################

class Activity(Document):
    email               =  StringField()
    activity            =  StringField()
    value               =  StringField()
    timeCreate          =  DateTimeField()
    isDeleted           =  BooleanField(default=False)

################################################################

class Species(Document):   
    vietnamesename            =  StringField()
    englishname               =  StringField()
    vietnamesename_ascii      =  StringField()
    description               =  StringField()
    isDeleted                 =  BooleanField(default=False)


   