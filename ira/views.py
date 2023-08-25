from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.core.mail import send_mail
from django.conf import settings
# Create your views here. -- for ira app


#...........................
class Ira_home(TemplateView):
    template_name = 'index.html'
#...........................
def redirect_to_home(request):
    return render(request, 'index.html')
#...........................
def send_demo_request(request):
    email_to = ['ashootosh.sharma@gmail.com', 'shuchiksharma@gmail.com', 'ashootosh@27two.com', 'shuchi@27two.com'],
    
    if request.POST:
        try:
            email_dict = {
                "subject" : "New demo request: "+ request.POST['email'],
                "body" : "A new demo request or enquiry has been submitted, details below:",
                "sender_email" : request.POST['email'],
                "sender_name" : request.POST['name'],
                "sender_tel" : request.POST['telephone'],
                "sender_type": request.POST['sender_type'],
                "all_details" : f"Email: {request.POST['email']}\nName:{request.POST['name']}\nTelephone:{request.POST['telephone']}\nEnquirer type:{request.POST['sender_type']}"

            }
            send_message = email_dict['body']+"\n"+email_dict["all_details"]
        except Exception as e:
            print(f'unable to find POST data in demo request {str(e)}')
            return HttpResponse(f'unable to find POST data in demo request')

        try:
            for mail in email_to:
                send_mail(
                    email_dict['subject'],
                    send_message,
                    '27twocreative.@gmail.com',
                    mail,
                    fail_silently=False,
                )
            return redirect('/ira/home/')
        except Exception as e:
            print(f'unable to send demo request emails - {str(e)}')
            return HttpResponse('Cannot send demo request')
        
#...........................
