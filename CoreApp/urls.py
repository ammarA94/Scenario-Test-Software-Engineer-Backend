from django.urls import path
from . import views
urlpatterns = [
    path('login/', views.Login, name= 'login'),
    path('login/login_authentication/', views.Authentication, name='login_authentication'),
    path('logout/', views.Logout, name= 'logout'),    
    path('Signup/', views.SignUp, name= 'Signup'),    
    path('RegisterUser/', views.RegisterUser, name= 'RegisterUser'), 
    path('AuthenticationProcess/', views.AuthenticationProcess, name= 'AuthenticationProcess'),     
    
    path('forgot_password/', views.ForgotPassword, name='forgot_password'),
    path('UpdatePassword/', views.Update_Password, name='UpdatePassword'),
    path('create_app/', views.CreateApp, name='create_app'),
    path('SaveApps/', views.SaveApps, name='SaveApps'),
    path('YourApps/', views.YourApps, name='YourApps'),
    path('detail_app/', views.Detail_App, name='detail_app'),
    path('SaveUpdatedApp/', views.SaveUpdatedApp, name='SaveUpdatedApp'),
    path('delete_app/', views.DeleteApp, name='delete_app'),
    path('cancelsubscription/', views.CancelSubscription, name='cancelsubscription'),
    
    
   ]