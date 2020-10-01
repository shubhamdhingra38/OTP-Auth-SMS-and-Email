from django.urls import path
from .views import signup, signup_view, authenticate, verification, home, login, logout

urlpatterns = [
    path('register/', signup_view),
    path('verify/<type>/', verification, name='verify'),
    path('api/auth/', signup),
    path('api/verify/', authenticate),
    path('home/', home, name='home'),
    path('login/', login),
    path('logout/', logout)
]
