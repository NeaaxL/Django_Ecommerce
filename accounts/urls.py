from accounts.views import signup, logout_user, login_user, profile
from django.urls import path

urlpatterns = [
    path('profile/', profile, name="profile"),
    path('signup/', signup, name="signup"),
    path('login/', login_user, name="login"),
    path('logout/', logout_user, name="logout"),]


