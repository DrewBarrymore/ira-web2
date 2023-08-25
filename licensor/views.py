from django.shortcuts import render
from django.http import HttpResponse
from .import validater
from .models import Access_key
from datetime import datetime
from django.views.generic import TemplateView
# Create your views here - for licensor app

# ...................................
def process_passKey(request):
    if request.GET.get('lic_key'):
        try:
            key_str = request.GET.get('lic_key')
            user_macid = request.GET.get('mac_id')

            key_model = Access_key.objects.get(pass_code = key_str)
            if key_model is not None and key_model.activated == True and key_model.used_already == False:
                key_model.used_already = True
                key_model.user_macid = str(user_macid)
                key_model.first_use_date = datetime.now()
                valid_till_response = str(key_model.valid_till)

                key_model.save()
                return(HttpResponse('OK-'+ valid_till_response))
            else:
                return(HttpResponse('NO'))
        except Exception as e:
            print(f'Unable to process get request installation check view --process_passKey--{str(e)}')
            return(HttpResponse('NO'))
    else:
        print(f'no license key found in request GET parameters --process_passKey')
        return(HttpResponse('NO'))
# ...................................

def uninstall_client(request):
    if request.GET.get('mac_id'):
        try:
            macid = request.GET.get('mac_id')

            this_result = Access_key.objects.get(user_macid = macid)
            if this_result is not None and this_result.used_already == True:
                this_result.uninstalled = True
                this_result.activated = False
                this_result.save()
                return(HttpResponse('OK'))
            else:
                return(HttpResponse('NO'))
        except Exception as e:
            print(f'Unable uninstall from client side --uninstall_client--{str(e)}')
            return(HttpResponse('NO'))
    else:
        print(f'not enough information supplied by client to uninstall -- uninstall_client')
        return(HttpResponse('NO'))
# ...................................

class Show_home(TemplateView):
    template_name = 'index.html'
