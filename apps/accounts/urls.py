from django.urls import path

from .views import SignupAPIView, VerifyAPIView, GetNewVerifyAPIView, ChangeUserInformationAPIView, \
    ChangeUserAvatarAPIView, CustomLoginAPIView, LoginRefreshAPIView, LogoutAPIView, ForgotPasswordAPIView, \
    ResetPasswordAPIView, GetMeGenericAPIView, ChangeUserAPIView

urlpatterns = [
    path('signup/', SignupAPIView.as_view(), name='signup'),
    path('verify/', VerifyAPIView.as_view(), name='verify'),
    path('send-again-verify-code/', GetNewVerifyAPIView.as_view(), name='send_again_verify_code'),
    path('change-user-information/', ChangeUserInformationAPIView.as_view(), name='change_user_information'),
    path('change-user-avatar/', ChangeUserAvatarAPIView.as_view(), name='change_user_avatar'),

    path('login/', CustomLoginAPIView.as_view(), name='login'),
    path('login/refresh/', LoginRefreshAPIView.as_view(), name='login-refresh'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('forgot-password/', ForgotPasswordAPIView.as_view(), name='forgot_password'),
    path('reset-password/', ResetPasswordAPIView.as_view(), name='reset_password'),

    path('get-me/', GetMeGenericAPIView.as_view(), name='get_me'),
    path('update/', ChangeUserAPIView.as_view(), name='update_user'),
]