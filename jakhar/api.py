from django.db import models
from django.contrib.auth.models import User, Permission, Group
from tastypie.authentication import BasicAuthentication, SessionAuthentication, ApiKeyAuthentication, MultiAuthentication
from tastypie.authorization import DjangoAuthorization, ReadOnlyAuthorization, Authorization
from tastypie.resources import ModelResource

from django.conf.urls import url
from tastypie.utils import trailing_slash
from tastypie.http import HttpUnauthorized, HttpForbidden, HttpApplicationError
from tastypie.resources import Resource, ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie.utils import trailing_slash
from tastypie.bundle import Bundle
from tastypie import fields
from tastypie.models import ApiKey, create_api_key
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.utils import timezone

from crum import get_current_request
import datetime
from datetime import timedelta, date
import dateutil.parser

import urlparse
#import urllib.parse
#from urllib.parse import urlparse
from tastypie.serializers import Serializer
#from utils import get_object_from_ct, create_activity_stream

#from logging import get_request_logger
#logger = get_request_logger()
import logging
logger = logging.getLogger()

from tastypie.exceptions import Unauthorized, ImmediateHttpResponse
from tastypie import http

import pytz

from django.contrib.gis.geoip2 import GeoIP2

from email_cronjob.models import Email_cron



class AdminApiKeyAuthentication(ApiKeyAuthentication):
    def is_authenticated(self, request, **kwargs):        
        if request.method == 'GET':
            return True
        apikey = request.GET.get('api_key', None)
        username = request.GET.get( 'username', None )
        if apikey and username:
            user = ApiKey.objects.get(key = apikey).user
            return ( ( user.username == username and user.is_authenticated() ) and ( (request.method in [ 'POST', 'DELETE','PUT','PATCH'] and user.is_staff) ) )
        return False


class MultiPartResource(object):
    def deserialize(self, request, data, format=None):
       if not format:
           format = request.Meta.get('CONTENT_TYPE', 'application/json')
       if format == 'application/x-www-form-urlencoded':
           return request.POST
       if format.startswith('multipart'):
           data = request.POST.copy()
           data.update(request.FILES)
           return data
       return super(MultiPartResource, self).deserialize(request, data, format)


    def put_detail(self, request, **kwargs):
        if request.META.get('CONTENT_TYPE').startswith('multipart') and \
                not hasattr(request, '_body'):
            request._body = ''

        return super(MultipartResource, self).put_detail(request, **kwargs)

class urlencodeSerializer(Serializer):
    formats = ['json', 'jsonp', 'xml', 'yaml', 'html', 'plist', 'urlencode']
    content_types = {
        'json': 'application/json',
        'jsonp': 'text/javascript',
        'xml': 'application/xml',
        'yaml': 'text/yaml',
        'html': 'text/html',
        'plist': 'application/x-plist',
        'urlencode': 'application/x-www-form-urlencoded',
        #'multipart': 'multipart/form-data',
        }
    def from_urlencode(self, data,options=None):
        """ handles basic formencoded url posts """
        qs = dict((k, v if len(v)>1 else v[0] )
            for k, v in urlparse.parse_qs(data).iteritems())
        return qs

    def to_urlencode(self,content): 
        pass

    def format_date(self, data):
        return data.strftime("%d-%m-%Y")


class PermissionResource(ModelResource):

    class Meta:
        queryset = Permission.objects.all()
        allowed_methods = ['get', 'post']
        resource_name = 'permission'
        #excludes = ['password']
        always_return_data = True 

class GroupResource(ModelResource):
    permissions = fields.ToManyField(PermissionResource, 'permissions', full=True, blank=True, null=True)

    class Meta:
        queryset = Group.objects.all()
        allowed_methods = ['get', 'post']
        resource_name = 'group'
        #excludes = ['password']
        always_return_data = True

class UserResource(ModelResource):
    groups = fields.ToManyField(GroupResource, 'groups', full=True, blank=True, null=True)
    user_permissions = fields.ToManyField(PermissionResource, 'user_permissions', full=True, blank=True)
    class Meta:
        queryset = User.objects.all()
        allowed_methods = ['get', 'post']
        resource_name = 'user'
        excludes = ['password']
        always_return_data = True
        filtering = {
            'username': 'exact'
        }

    # def build_filters( self, filters=None ):
    #     if filters is None:
    #         filters = {}

    #     orm_filters = super(UserResource, self).build_filters( filters )

    #     #If we need to serve the field username in User, the username in authentication info acts as a filter key. Removing it here.
    #     if orm_filters.has_key( "username__exact" ):
    #         orm_filters.pop( "username__exact" )
    #     else:
    #         #Do not serve unfiltered requests
    #         orm_filters[ 'pk' ] = "-1"

    #     return orm_filters

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/login%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('login'), name='api_login'),
            url(r"^(?P<resource_name>%s)/logout%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('logout'), name='api_logout'),
            url(r"^(?P<resource_name>%s)/create%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('create'), name='api_create'),
        ]

    def login(self, request, **kwargs):
        logger.debug( request )
        self.method_check(request, allowed=['post'])
        try:
            data = self.deserialize(request, request.body, format=request.META.get('CONTENT_TYPE', 'application/json'))
            username = data.get('username', '')
            password = data.get('password', '')
        except:
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')

        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                #api_key = ApiKey.objects.create(user='vsjakhar')
                #username_user = str(user.username)
                fname = str(user.first_name)
                lname = str(user.last_name)
                email1 = str(user.email)
                ip = str(request.META['REMOTE_ADDR']) #+ ',' + request.user_agent.browser.family + ',' + request.user_agent.os.family + ',' + request.user_agent.device.family
                browser = str(request.user_agent.browser.family)
                os = str(request.user_agent.os.family)
                date_tim = timezone.now().astimezone(pytz.timezone('Asia/Kolkata'))
                date_time = str(date_tim.strftime("%Y-%m-%d %H:%M:%S"))
                g = GeoIP2()
                h = g.city(ip)

                html_content = '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"><html xmlns="http://www.w3.org/1999/xhtml"><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/><meta name="viewport" content="width=device-width, initial-scale=1"/><title>loginttemp</title><style type="text/css">@import url(http://fonts.googleapis.com/css?family=Droid+Sans);img{max-width: 600px;outline: none;text-decoration: none;-ms-interpolation-mode: bicubic;}a{text-decoration: none;border: 0;outline: none;color: #bbbbbb;}a img{border: none;}td, h1, h2, h3{font-family:Arial;font-weight: 400;}td{text-align: center;}body{-webkit-font-smoothing:antialiased;-webkit-text-size-adjust:none;width: 100%;height: 100%;color: #37302d;background: #ffffff;font-size: 16px;}table{border-collapse: collapse !important;}.headline{color: #ffffff;font-size: 36px;}.force-full-width{width: 100% !important;}</style><style type="text/css" media="screen">@media screen{td, h1, h2, h3{font-family: Arial !important;}}</style><style type="text/css" media="only screen and (max-width: 480px)">@media only screen and (max-width: 480px){table[class="w320"]{width: 320px !important;}}</style></head><body class="body" style="padding:0; margin:0; display:block; background:#ffffff; -webkit-text-size-adjust:none" bgcolor="#ffffff"><table align="center" cellpadding="0" cellspacing="0" width="100%" height="100%" ><tr><td align="center" valign="top" bgcolor="#ffffff" width="100%"><center><table style="margin: 0 auto;" cellpadding="0" cellspacing="0" width="600" class="w320"><tr><td align="center" valign="top"><table style="margin: 0 auto;" cellpadding="0" cellspacing="0" width="100%" bgcolor="#3BCDB0"><tr><td style="text-align: center;"><a href="http://auragoa.com/"><img class="w320" width="120" height="100" src="http://auragoa.com/wp-content/uploads/2017/01/aura-goa-logofinal.png" style=" z-index: 99;position: inherit;padding-top: 50px;"></a></td></tr><tr><td><br><img src="http://demodevelopment.in/mail_img/mail-alert.png" width="150" height="150" alt="mail"></td></tr><tr><td class="headline">Dear '+fname+' '+lname+'</td></tr><tr><td><center><table style="margin: 0 auto;" cellpadding="0" cellspacing="0" width="60%"><tr><td style="color:#187272;font-size: 14px;"><br>There has been a new login in your account.<br>Following are the details:<br></td></tr></table></center></td></tr><tr><td height="60" width="100%"></td></tr></table><table style=" text-align: center; margin-top:48px;margin-bottom:48px" cellspacing="0" cellpadding="0" border="0"><tbody><tr valign="middle"><td width="32px"></td><td align="center"><img src="https://cdn4.iconfinder.com/data/icons/green-shopper/1068/user.png" width="50" height="50" alt="robot picture"></td><td width="16px"></td><td style="line-height:1.2; text-align:left; "><span style="font-family:Arial;font-size:20px;color:#202020">'+fname+' '+lname+'</span><br><span style="font-family:Arial;font-size:13px;color:#727272"><a>'+email1+'</a></span></td></tr><tr valign="middle"><td height="24px" width="32px"></td></tr><tr valign="top"><td width="32px"></td><td><img src="http://www.free-icons-download.net/images/security-shield-icon-32307.png" width="50" height="50" alt="robot picture"></td><td width="16px"></td><td style="line-height:1.2; text-align:left;"><span style="font-family:Arial;font-size:16px;color:#202020">'+os+'</span><br><span style="font-family:Arial;font-size:13px;color:#727272">'+date_time+' (India Time)<br>'+str(h['country_name'])+'<br>'+browser+'</span></td></tr><tr valign="middle"><td height="24px" width="32px"></td></tr><tr valign="top"><td width="32px"></td><td><img src="http://demodevelopment.in/mail_img/location_map_pin_light_blue6.png" width="50" height="60" alt="robot picture"></td><td width="16px"></td><td style="line-height:1.2; text-align:left;"><span style="font-family:Arial;font-size:16px;color:#202020">Ip Address</span><br><span style="font-family:Arial;font-size:13px;color:#727272">'+ip+'<br>'+str(h['city'])+', '+str(h['country_name'])+'</span></td></tr></tbody></table><table class="full" cellspacing="0" cellpadding="0" align="center" border="0" width="100%"><tbody><tr><td valign="top" bgcolor="#414141" align="center" width="100%"><table class="mobile" cellspacing="0" cellpadding="0" align="center" border="0" width="100%"><tbody><tr><td align="center"><table class="full" cellspacing="0" cellpadding="0" align="center" border="0" width="100%"><tbody><tr><td height="10" width="100%"></td></tr></tbody></table><table class="full" cellspacing="0" cellpadding="0" align="center" border="0" width="600"><tbody><tr><td align="center" width="100%"><table style="border-collapse:collapse; mso-table-lspace:0pt; mso-table-rspace:0pt;" class="fullCenter" cellspacing="0" cellpadding="0" align="left" border="0" width="140"><tbody><tr><td style="text-align: center;font-family: Helvetica, Arial, sans-serif;font-size: 12px;color: #ffffff;line-height: 15px;font-weight: 400;padding-left: 30px;" class="fullCenter" valign="middle" width="200px">Aura Goa Wellness Resort, Mandrem, North Goa<br>+91 76653-22222<br>info@auragoa.com<br><a href="http://auragoa.com/" style="text-decoration: none; color: #ffffff;">auragoa.com</a></td></tr></tbody></table><table style="border-collapse:collapse; mso-table-lspace:0pt; mso-table-rspace:0pt;" class="full" cellspacing="0" cellpadding="0" align="left" border="0" width="20"><tbody><tr><td height="1" width="100%"></td></tr></tbody></table><table style="text-align: right; border-collapse:collapse; mso-table-lspace:0pt; mso-table-rspace:0pt;" class="buttonScale" cellspacing="0" cellpadding="0" align="right" border="0" width="96"><tbody><tr><td class="icons17" style="text-align: left;" valign="middle" align="center" height="45" width="32"><a href="https://twitter.com/aurasparetreat" style="text-decoration: none;"><img src="http://demodevelopment.in/mail_img/social_icon_1.png" alt="" class="hover" border="0" width="17"></a></td><td class="icons17" style="text-align: left;" valign="middle" align="center" height="45" width="32"> <a href="https://www.facebook.com/aurasparetreat" style="text-decoration: none;"><img src="http://demodevelopment.in/mail_img/social_icon_2.png" alt="" class="hover" border="0" width="17"></a></td><td class="icons17" style="text-align: left;" valign="middle" align="center" height="45" width="32"> <a href="https://plus.google.com/u/0/103796393489619851236" style="text-decoration: none;"><img src="http://demodevelopment.in/mail_img/social_icon_3.png" alt="" class="hover" border="0" width="17"></a></td></tr></tbody></table></td></tr></tbody></table><table class="full" cellspacing="0" cellpadding="0" align="center" border="0" width="100%"><tbody><tr><td height="10" width="100%"></td></tr></tbody></table></td></tr></tbody></table></td></tr></tbody></table></td></tr></table></center></td></tr></table></body></html>'
                #send_mail('AuraGoa Login Attention', 'Someone Just Logined from your Account if that was not you then Contact to Admin. Logined at '+str(timezone.now())+' Time ', 'Auragoa <donotreply@auragoa.com>', [user.email], html_message=html_content, fail_silently=False)

                sender = 'donotreply@auragoa.com'
                receiver = user.email
                subject = 'Login alert'
                body = html_content
                purpose = 'Login'
                Email_cron.objects.create(email_uid_id = user.id, email_from=sender, email_to=receiver, email_subject=subject, email_body=body, email_purpose=purpose)



                try:
                    #key = ApiKey.objects.get(user=user)
                    api_key = ApiKey.objects.get(user=user)
                    api_key.key = None
                    api_key.save()
                except ApiKey.DoesNotExist:
                    api_key = ApiKey.objects.create(user=user)
                    return self.create_response( request, { 'success': False, 'reason': 'missing key' }, HttpForbidden )

                return self.create_response( request, { 'success': True, 'username': user.username, 'first_name': user.first_name, 'last_name': user.last_name, 'key': api_key.key, 'is_superuser': user.is_superuser, 'id': user.id } )
            else:
                return self.create_response( request, { 'success': False, 'reason': 'disabled' }, HttpForbidden )
        else:
            return self.create_response( request, { 'success': False, 'reason': 'invalid login', 'skip_login_redir': True }, HttpUnauthorized )

    def logout(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        self.is_authenticated( request )
        if request.user:
            logout(request)
            return self.create_response(request, {'success': True})
        else:
            return self.create_response(request, {'success': False}, HttpUnauthorized)
    
    def check_password( self, pwd, confirm ):
        regex = re.compile(PWD_REGEX)        
        return ( pwd == confirm ) and ( regex.match( pwd ) and regex.match( confirm ) )

    def create(self, request, **kwargs):
        logger.debug( request )
        self.method_check(request, allowed=['post'])
        try:  
            email = request.REQUEST.get('email')
            firstname = request.REQUEST.get('firstname')
            lastname = request.REQUEST.get('lastname')

            username = request.REQUEST.get('username')
            password = request.REQUEST.get('password')
            confirm = request.REQUEST.get('confirm')
                
            if not self.check_password( password, confirm ):
                raise Exception('Password criteria doesnt match')

            user = User.objects.create_user(username = username, email = email, password = password )
            profile = User_profile( user = user, email = email, firstname = firstname, lastname = lastname, role = 'ru' )
            profile.save()
            
            return self.create_response( request, { 'success': True, 'user_id': user.id } )            
            
        except Exception as e:
            logger.exception('exception while creating user: %s' %(e))
            return self.create_response( request, { 'success': False, 'reason': ('%s' %(e)) }, HttpApplicationError )
            
            #http://hostname/api/user/login with data  { 'username' : 'me', 'password' : 'l33t' }


# 31 Days Date List

class DatesObject(object):
    def __init__(self, initial=None):
        self.__dict__['_data'] = {}
        if initial:
            self.update(initial)

    def __getattr__(self, name):
        return self._data.get(name, None)

    def __setattr__(self, name, value):
        self.__dict__['_data'][name] = value

    def update(self, other):
        for k in other:
            self.__setattr__(k, other[k])

    def to_dict(self):
        return self._data

class DatesResource(Resource):
    
    class Meta:
        resource_name = 'dates'
        fields = ['value']
        allowed_methods = ['get']
        object_class = DatesObject
        serializers = urlencodeSerializer
        include_resource_uri = False

    def detail_uri_kwargs(self, bundle_or_obj):
        kwargs = {}

        if isinstance(bundle_or_obj, Bundle):
            kwargs['value'] = bundle_or_obj.obj.value
        else:
            kwargs['value'] = bundle_or_obj.value
        return kwargs

    def get_object_list(self, request):
        return [self.obj_get()]

    def obj_get_list(self, request=None, **kwargs):
        return [self.obj_get()]

    def obj_get(self, request=None, key=None, **kwargs):
        setting = DatesObject()
        
        return setting

    def dehydrate(self, bundle):
        request = get_current_request()
        dat = request.GET.get('date', None)
        
        if not dat:
            start_date = datetime.date.today()
            date = dateutil.parser.parse(str(start_date))
            end_date = start_date + datetime.timedelta(days=32)
            for n in range(int((end_date - start_date).days)):
                x = start_date + timedelta(n)
                y = date + timedelta(n)
                bundle.data[n] = {'date':x, 'datetime':y, 'day':x.day, 'month':x.month, 'year':x.year, 'week_day1':x.strftime('%a'), 'week_day2':x.strftime('%A'), 'month2':x.strftime('%b'), 'month3':x.strftime('%B')}

        else:
            datetimes = dateutil.parser.parse(dat)
            date = dateutil.parser.parse(dat).date()
            end_date = date + (datetime.timedelta(days=32))
            for n in range(int((end_date-date).days)):
                x = date + timedelta(n)
                y = datetimes + timedelta(n)
                bundle.data[n] = {'date':x, 'datetime':y, 'day':x.day, 'month':x.month, 'year':x.year, 'week_day1':x.strftime('%a'), 'week_day2':x.strftime('%A'), 'month2':x.strftime('%b'), 'month3':x.strftime('%B')}

        return bundle

# class DatesObject(object):
#     def __init__(self, initial=None):
#         self.__dict__['_data'] = {}
#         if initial:
#             self.update(initial)

#     def __getattr__(self, name):
#         return self._data.get(name, None)

#     def __setattr__(self, name, value):
#         self.__dict__['_data'][name] = value

#     def update(self, other):
#         for k in other:
#             self.__setattr__(k, other[k])

#     def to_dict(self):
#         return self._data

# class DatesResource(Resource):
    


#     class Meta:
#         resource_name = 'dates'
#         fields = ['value']
#         allowed_methods = ['get']
#         object_class = DatesObject
#         serializers = urlencodeSerializer
#         include_resource_uri = False

#     def detail_uri_kwargs(self, bundle_or_obj):
#         kwargs = {}

#         if isinstance(bundle_or_obj, Bundle):
#             kwargs['value'] = bundle_or_obj.obj.value
#         else:
#             kwargs['value'] = bundle_or_obj.value
#         return kwargs

#     def get_object_list(self, request):
#         return [self.obj_get()]

#     def obj_get_list(self, request=None, **kwargs):
#         return [self.obj_get()]

#     def obj_get(self, request=None, key=None, **kwargs):
#         setting = DatesObject()
       
#         return setting

#     def dehydrate(self, bundle):
       
        
#         start_date = datetime.date.today()
#         end_date = start_date + datetime.timedelta(days=31)
#         for n in range(int((end_date - start_date).days)):
#             bundle.data[n] = start_date + timedelta(n)
       

#         return bundle            



import re

from django.utils.text import compress_string
from django.utils.cache import patch_vary_headers

from django import http

try:
    import settings 
    XS_SHARING_ALLOWED_ORIGINS = settings.XS_SHARING_ALLOWED_ORIGINS
    XS_SHARING_ALLOWED_METHODS = settings.XS_SHARING_ALLOWED_METHODS
except:
    XS_SHARING_ALLOWED_ORIGINS = '*'
    XS_SHARING_ALLOWED_METHODS = ['POST','GET','OPTIONS', 'PUT', 'DELETE']


class XsSharing(object):
    """
        This middleware allows cross-domain XHR using the html5 postMessage API.
         
        Access-Control-Allow-Origin: http://foo.example
        Access-Control-Allow-Methods: POST, GET, OPTIONS, PUT, DELETE
    """
    def process_request(self, request):

        if 'HTTP_ACCESS_CONTROL_REQUEST_METHOD' in request.META:
            response = http.HttpResponse()
            response['Access-Control-Allow-Origin']  = XS_SHARING_ALLOWED_ORIGINS 
            response['Access-Control-Allow-Methods'] = ",".join( XS_SHARING_ALLOWED_METHODS ) 
            
            return response

        return None

    def process_response(self, request, response):
        # Avoid unnecessary work
        if response.has_header('Access-Control-Allow-Origin'):
            return response

        response['Access-Control-Allow-Origin']  = XS_SHARING_ALLOWED_ORIGINS 
        response['Access-Control-Allow-Methods'] = ",".join( XS_SHARING_ALLOWED_METHODS )

        return response
