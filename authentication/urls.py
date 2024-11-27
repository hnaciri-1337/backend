from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
	signin,
	signup,
	signout,
	# forget_password,
	# reset_password,
    get_user_info,
)

urlpatterns = [
    path('refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('signup', signup),
    path('signin', signin),
    path('signout', signout),
    # path('forget-password', forget_password),
    # path('reset-password/<str:uidb64>/<str:token>', reset_password),
    path('user', get_user_info),
]
