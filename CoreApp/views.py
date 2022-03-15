from django.db.models import Count
from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.template import loader
from .models import * 
import secrets,smtplib, ssl,traceback,datetime,sys,os,csv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils import timezone

def ShowException(e):
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    print(exc_type, fname, exc_tb.tb_lineno)    
    print (e)   
def SendEmail(receiver_email):
    try:
        AuthentiationCode = secrets.token_hex(7)
        sender_email = "futurex.on.the.go@gmail.com"
        password = "Futurex.on.the.go123"
        subject='You have received your Verification Code.'
        html='<p><strong>Your Verification code is :</strong></p><blockquote><p><span style="font-size:18px"><span style="font-family:Georgia,serif"><strong>'+str(AuthentiationCode)+'</strong></span></span></p></blockquote> '
        message = MIMEMultipart(subject)
        message["Subject"] = subject
        message["From"] = sender_email
        message["To"] = receiver_email
        # Create the plain-text and HTML version of your message
        body = MIMEText(html, "html")
        message.attach(body)
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=ssl.create_default_context()) as server:
            server.login(sender_email, password)
            server.sendmail(
                sender_email, receiver_email, message.as_string()
            )
        return AuthentiationCode
    except Exception as e:
        ShowException(e)
        return False
            
def SignUp(request):
    try:
        request.session['displayname']
        return HttpResponseRedirect('/YourApps/')
    except:
        template = loader.get_template("Signup.html")
        context = {
            "session":request.session,
        }
        return HttpResponse(template.render(context, request))
@api_view(['POST'])
def RegisterUser(request):
    input_data=request.data    
    username = input_data['username']    
    receiver_email =input_data['email'] 
    password =  input_data['password']
    if User.objects.filter(Email=receiver_email).exists():
        context = {"flag":False,"Msg": 'Email already registered. Please login if this email id belongs to you.' }                    
    else:
        try:
            AuthentiationCode=SendEmail(receiver_email)
            if AuthentiationCode:
                User(UserName=username,Email=receiver_email,Password=password,AuthentiationCode=AuthentiationCode,RegisterDate=timezone.now()).save()
                template = loader.get_template("AuthenticationVerification.html")
                context = {"flag":True,"AuthType":"Register","email":receiver_email,"Msg": 'Authentication Code successfully sent to your email.'}                    
            else:
                context = { "flag":False,"Msg": 'Email not sent due to problem in email service. Please try again.' }                    
        except Exception as e:
            ShowException(e)  
            context = {"flag":False, "Msg": 'Error in authentication process. Please try again.' }
    return Response(context)      
@api_view(['POST'])
def AuthenticationProcess(request):
    input_data=request.data    
    code = input_data['code']   
    email = input_data['email']
    AuthType = input_data['AuthType']   
    
    if User.objects.filter(AuthentiationCode=code,Email=email).exists():
        if AuthType=='Register':
            context = { "flag": True,"AuthType":"Register",  "Msg": 'Account created.' }      
        else:
            context = { "flag": True,"AuthType":"Forgot", "email":email,"Msg": "Please Enter Your New Password" }                     
    else:   
        template = loader.get_template("AuthenticationVerification.html")            
        context = { "flag": False, "AuthType":AuthType,"Msg": 'Code Not Matched.' ,"email":email}
    return Response(context)      

def Login(request):
    try:
        
        request.session['displayname']
        return HttpResponseRedirect('/YourApps/')

    except:
        template = loader.get_template("login.html")
        context = {
            "session":request.session,
        }
        return HttpResponse(template.render(context, request))       
@api_view(['POST'])
def Authentication(request):
    input_data=request.data
    try:
        email = input_data['email']
        password = input_data['password']
        if User.objects.filter(Email=email,Password=password).exists():
            UserObj=User.objects.get(Email=email, Password=password)
            request.session['displayname']=UserObj.UserName
            request.session['Id']=UserObj.Id            
            return Response({"flag":True,"Msg":"Logged In"})      
        else:                
            return Response({"flag":False,"Msg":"Wrong Credentials. Please try again."})      

    except Exception as e:
        ShowException(e)
        return Response({"flag":False,"Msg":"There seems some problems in performing your operations. Please try again."})      
        
    
@api_view(['POST'])
def Logout(request):
    try:
        del request.session['displayname']
        return Response({"flag":True,"Msg":"Logged Out"})      
    except:
        return Response({"flag":True,"Msg":"Logged Out"})      
@api_view(['POST'])
def ForgotPassword(request):
    input_data=request.data        
    forgot_email =input_data['forgot_email']
    template = loader.get_template("login.html")  
    AuthentiationCode=SendEmail(forgot_email)
    if AuthentiationCode:
        if User.objects.filter(Email=forgot_email).exists():
            User.objects.filter(Email=forgot_email).update(AuthentiationCode=AuthentiationCode)
            template = loader.get_template("AuthenticationVerification.html")
            context = { "flag":True,"AuthType":"Forgot","email":forgot_email,"Msg": 'Authentication Code successfully sent to your email.'}                    
        else:
            context = {  "flag":False,"email":forgot_email,"Msg": 'Email is not associated with any account.'}                                
    else:
        context = { "flag":False,"receiver_email":forgot_email, "Msg": 'Email not sent due to problem in email service. Please try again.' }                            
    return Response(context)      
@api_view(['POST'])
def Update_Password(request):
    input_data=request.data    
    email = input_data['email']
    password = input_data['password'] 
    if User.objects.filter(Email=email).exists():
        User.objects.filter(Email=email).update(Password=password)
        context = {"flag":True,"Msg": 'Password Updated Successfully.'}  
    else:
        context = {"flag":False, "Msg": 'Error Updating your Password.'}    
    return Response(context)      
        
def CreateApp(request):
    try:
        request.session['displayname']
    except:
        return HttpResponseRedirect('/login/')
    template = loader.get_template("CreateApp.html")
    data=[]
    return HttpResponse(template.render({}, request))

@api_view(['POST'])
def SaveApps(request):
    input_data=request.data    
    app_name = input_data['app_name']
    description = input_data['description'] 
    try:
        APP(UserId=User.objects.filter(Id=request.session['Id'])[0],AppName=app_name,Description=description,CreatedDate=timezone.now(),UpdatedDate=timezone.now(),SubscriptionDate=timezone.now(),EndDate=timezone.now()+datetime.timedelta(days=30)).save()
        context = {"flag":True,"Msg": 'App created Successfully.'}  
    except Exception as e:
        ShowException(e)
        context = {"flag":False,"Msg": 'Error!.Please try again later...'}  
        
    return Response(context)      

def YourApps(request):
    try:
        request.session['displayname']
    except:
        return HttpResponseRedirect('/login/')
    template = loader.get_template("AllApps.html")
    data=[]
    for apps in APP.objects.filter(UserId=User.objects.filter(Id=request.session['Id'])[0]):
        data.append([apps.Id,apps.AppName,apps.Description,apps.SubscriptionName,apps.SubscriptionPrice,apps.active,apps.CreatedDate,apps.SubscriptionDate,apps.EndDate])
    context={"Data":data, "session":request.session}
    return HttpResponse(template.render(context, request))

@api_view(['POST'])
def Detail_App(request):
    input_data=request.data    
    app_id = input_data['app_id']
    data=[]
    try:
        apps=APP.objects.filter(Id=app_id)[0]
        data=[apps.Id,apps.AppName,apps.Description,apps.SubscriptionName,apps.SubscriptionPrice,apps.active,apps.CreatedDate,apps.SubscriptionDate,apps.EndDate]
        context = {"flag":True,"Data": data}  
    except Exception as e:
        context = {"flag":False,"Data": data}  
    return Response(context)      

@api_view(['POST'])
def SaveUpdatedApp(request):
    input_data=request.data    
    app_id = input_data['app_id']
    app_name = input_data['app_name']
    description = input_data['description']
    SubscriptionId = input_data['SubscriptionId']
    price=0 if SubscriptionId=='Free' else 10 if SubscriptionId=='Standard' else 25
    try:
        app_obj=APP.objects.filter(Id=app_id)
        if app_obj[0].SubscriptionName==SubscriptionId:
            app_obj.update(AppName=app_name,Description=description,UpdatedDate=timezone.now())
            context = {"flag":True,"Msg": 'App updated Successfully.'}                    
        else:
            app_obj.update(AppName=app_name,Description=description,SubscriptionName=SubscriptionId,SubscriptionPrice=price,UpdatedDate=timezone.now(),SubscriptionDate=timezone.now(),EndDate=timezone.now()+datetime.timedelta(days=30))
            context = {"flag":True,"Msg": 'App and Subscription updated Successfully.'}    
    except Exception as e:
        print(e)
        context = {"flag":False,"Msg": 'Error!.Please try again later...'}  
    return Response(context)      

@api_view(['POST'])
def DeleteApp(request):
    input_data=request.data    
    app_id = input_data['app_id']
    try:
        apps=APP.objects.filter(Id=app_id).delete()
        context = {"flag":True,"Msg": 'App deleted Successfully.'}                    
    except Exception as e:
        context = {"flag":False,"Msg": 'Error!.Please try again later...'}  
    return Response(context)      

@api_view(['POST'])
def CancelSubscription(request):
    input_data=request.data    
    app_id = input_data['app_id']
    try:
        app_obj=APP.objects.filter(Id=app_id)
        if app_obj[0].active=='True':
            app_obj.update(active=False,SubscriptionName='Free',SubscriptionPrice=0,UpdatedDate=timezone.now(),SubscriptionDate=timezone.now(),EndDate=timezone.now()+datetime.timedelta(days=30))
            context = {"flag":True,"Msg": 'Subscription cancelled Successfully.'}                    
        else:
            context = {"flag":False,"Msg": 'Subscription is already cancelled.'}    
    except Exception as e:
        context = {"flag":False,"Msg": 'Error!.Please try again later...'}  
    return Response(context)      