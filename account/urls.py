from django.urls import path
from .views import *

urlpatterns = [
	path('register/', RegisterView.as_view(), name='register'),
	path('user/', UserView.as_view(), name='update_or_retrieve'),
	path('login/', LoginView.as_view(), name='login'),
	path('logout/', LogoutView.as_view(), name='logout'),
	path('user/change-password/', ChangePasswordView.as_view(), name='change_password'),
	path('activate/<str:uidb64>/<str:token>/', EmailVerificationView.as_view(), name='email_verify'),
	path('forget-password/', ForgetPasswordView.as_view(), name='forget_password'),
]