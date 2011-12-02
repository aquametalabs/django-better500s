import datetime
import logging

from django.utils import simplejson
from django.core.mail import mail_admins
from django.views.decorators.csrf import csrf_exempt
from helpers import exception_string

from better500s.models import CaughtError
from helpers.view import render_with_context, json_view, render_to, render_string_with_context

def create_caught_error(request, epoch, traceback, subject_prefix=""):
    error_obj = CaughtError.objects.create(
                            epoch_time=epoch,
                            user=request.user,
                            error_time=datetime.datetime.now(),
                            simple_traceback=traceback
                            )
    try:    
        subject = "%s500 - %s" % (subject_prefix, error_obj)
        body = render_string_with_context(request, "better500s/admin_email.txt", locals())
        mail_admins(subject, body, fail_silently=True)
    except:
        log = logging.getLogger("better500s")
        log.error(exception_string())
        pass

@json_view
def ajax_error_save(request):
    if request.method == "POST" and "epoch" in request.POST:
        epoch = int(request.POST["epoch"])
        simple_traceback = request.POST['simple_traceback'].replace("\\n","\n\n")
        create_caught_error(request, epoch, simple_traceback)
        
    return {"success": True}

@csrf_exempt
@render_to("better500s/feedback_saved.html")
def user_error_submit(request):
    try:
        if request.method == "POST" and "epoch" in request.POST:
            error_obj = CaughtError.objects.get(epoch_time=int(request.POST['epoch']))
            error_obj.user_notes = request.POST['user_notes']
            error_obj.save()
            
            subject = " User Bug Report - %s" % (error_obj)
            body = render_string_with_context(request, "better500s/error_with_notes_email.txt", locals())
            mail_admins(subject, body, fail_silently=True)
    except:
        pass
    return locals()

@render_to("better500s/view_error.html")
def view_error(request, error_id):
    error_obj = CaughtError.objects.get(pk=error_id)
    return locals()

@render_to("better500s/traceback.html")
def traceback_source(request, error_id):
    error_obj = CaughtError.objects.get(pk=error_id)
    return locals()
