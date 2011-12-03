import sys, os, time, datetime
import traceback
import logging

from django.views.debug import technical_500_response
from django.core.exceptions import PermissionDenied
from django.conf import settings

from better500s import BETTER_500_LOG_DIR, BETTER_500_UNCAUGHT_DIR, BETTER_500_AJAX_URL, BETTER_500_POST_URL
from better500s.helpers import exception_string

class Better500s(object):
    """Middleware saves nice tracebacks, and gets user feedback on what went wrong."""

    def save_traceback_to_epoch_file(self, request, exc_info):
        try:
            resp = technical_500_response(request, *exc_info)

            if BETTER_500_LOG_DIR:
                epoch = int(time.mktime(datetime.datetime.now().timetuple()))
                epoch_file = "%s.html" % (epoch,)

                folder = os.path.join(BETTER_500_LOG_DIR, BETTER_500_UNCAUGHT_DIR)
                debug_log_file = os.path.join(folder, epoch_file)
            
                if not os.path.exists(folder):
                       os.makedirs(folder)

                try:
                    from django.core.files.storage import default_storage
                    from django.core.files.base import ContentFile
                    default_storage.save(debug_log_file, ContentFile(resp._container[0]))
                except:
                    f = open(debug_log_file,"a")
                    f.write(resp._container[0])
                    f.close()

                return epoch
        except:
            try:
                log = logging.getLogger("better500s")
                log.error(exception_string())
            except:
                pass
            pass
        return None

    def process_exception(self, request, exception):
        if hasattr(settings,"DEBUG") and settings.DEBUG == False and type(exception) != PermissionDenied:
            exc_info = sys.exc_info()
            try:
                from django.template import Context
                from django.utils.encoding import smart_unicode
                from django.template.loader import render_to_string
                from django.http import HttpResponseServerError, HttpResponseNotFound
                from django.http import Http404  

                epoch = self.save_traceback_to_epoch_file(request, exc_info)
                context = {}
                if epoch:
                    try:
                        context = {}
                        context['epoch'] = epoch
                        context['MEDIA_URL'] = getattr(settings, "MEDIA_URL", None)
                        context['STATIC_URL'] = getattr(settings, "STATIC_URL", None)
                        context['ajax_url'] = BETTER_500_AJAX_URL
                        context['post_url'] = BETTER_500_POST_URL

                        context['simple_traceback'] = ""

                        try:
                            exception_value = smart_unicode(exc_info[1])
                            if exception_value != u"":
                                context['exception_value'] = exception_value
                        except:
                            pass
                        try:
                            context['simple_traceback'] = "\\n".join(traceback.format_exception(*exc_info))
                        except:
                            pass

                        from django.core.urlresolvers import reverse
                        context['ajax_url'] = reverse("better_500_response",)
                        context['post_url'] = reverse("better_500_saved",)
                    except:
                        try:
                            log = logging.getLogger("better500s")
                            log.error(exception_string())
                        except:
                            pass                        

                
                
                html = render_to_string("better500s/500_handler.html", context, context_instance=Context())

                if type(exception) == type(Http404):
                    return HttpResponseNotFound(html, mimetype='text/html')
                else:
                    return HttpResponseServerError(html, mimetype='text/html')

            except:
                try:
                    log = logging.getLogger("better500s")
                    log.error(exception_string())
                except:
                    pass

        return None

