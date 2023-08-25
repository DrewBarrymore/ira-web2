#urls - for the licensor app

from django.urls import path
from .views import process_passKey, Show_home, uninstall_client

urlpatterns = [
    # path('hello/', say_hello, name='sayin hello'),
    path('installation_check/', process_passKey, name='pre-installation check'),
    path('uninstall/', uninstall_client, name='uninstall_from_client'),
    path('home/', Show_home.as_view(), name='Home'),
    
]