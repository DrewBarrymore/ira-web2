#urls - for the ira app

from django.urls import path
from .views import Ira_home, send_demo_request, redirect_to_home

urlpatterns = [
    # path('home/', Ira_home.as_view(), name='Home'),
    path('', Ira_home.as_view(), name='Home'),
    path('demo_request/', send_demo_request, name='demo_request'),
    # path('redirect_home/', Ira_home.as_view(), name='back_to_home'),
    
]