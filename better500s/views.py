import datetime
import logging

from django.utils import simplejson
from django.core.mail import mail_admins
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.loader import render_to_string
from django.core.urlresolvers import reverse
from django.conf import settings

from better500s import BETTER_500_DEFAULT_RETURN_URL_NAME
from better500s.helpers import exception_string
from better500s.models import CaughtError

try:
    import telegram
except:
    telegram = None


def create_caught_error(request, epoch, traceback, subject_prefix=""):
    error_obj = CaughtError.objects.create(
                            epoch_time=epoch,
                            user=request.user,
                            error_time=datetime.datetime.now(),
                            simple_traceback=traceback
                            )
    try:
        detail_page_url = request.build_absolute_uri(error_obj.view_url)
        subject = "%s500 - %s" % (subject_prefix, error_obj)
        body = render_to_string("better500s/admin_email.txt", locals(), context_instance=RequestContext(request))
        mail_admins(subject, body, fail_silently=True)
        if telegram and getattr(settings, 'BETTER_500_NOTIFICATION_CHANNEL', False):
            telegram.broadcast(settings.BETTER_500_NOTIFICATION_CHANNEL, subject, detail_page_url, add_to_queue=False)
    except:
        log = logging.getLogger("better500s")
        log.error(exception_string())
        pass

def ajax_error_save(request):

    try:
        if request.method == "POST" and "epoch" in request.POST:
            epoch = int(request.POST["epoch"])
            simple_traceback = request.POST['simple_traceback'].replace("\\n","\n\n")
            create_caught_error(request, epoch, simple_traceback)
    except:
        print exception_string()
            
    return HttpResponse(simplejson.dumps({"success": True}))

@csrf_exempt
def user_error_submit(request):
    try:
        if request.method == "POST" and "epoch" in request.POST:
            error_obj = CaughtError.objects.get(epoch_time=int(request.POST['epoch']))
            error_obj.user_notes = request.POST['user_notes']
            error_obj.save()
            detail_page_url = request.build_absolute_uri(error_obj.view_url)
            
            subject = " User Bug Report - %s" % (error_obj)
            body = render_to_string("better500s/error_with_notes_email.txt", locals(), context_instance=RequestContext(request))
            mail_admins(subject, body, fail_silently=True)
            if telegram and getattr(settings, 'BETTER_500_NOTIFICATION_CHANNEL', False):
                telegram.broadcast(settings.BETTER_500_NOTIFICATION_CHANNEL, subject, detail_page_url, add_to_queue=False)
            home_url = BETTER_500_DEFAULT_RETURN_URL_NAME
            if home_url:
                try:
                    home_url = request.build_absolute_uri(reverse(home_url))
                except:
                    if home_url[0] != "/":
                        home_url = "/%s" % home_url

    except:
        pass
    
    return render_to_response('better500s/feedback_saved.html',locals(), context_instance=RequestContext(request))

def view_error(request, error_id):
    error_obj = CaughtError.objects.get(pk=error_id)
    
    return render_to_response('better500s/view_error.html',locals(), context_instance=RequestContext(request))

def traceback_source(request, error_id):
    error_obj = CaughtError.objects.get(pk=error_id)
    
    return render_to_response('better500s/traceback.html',locals(), context_instance=RequestContext(request))
