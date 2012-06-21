import os

from django.db import models
from django.core.urlresolvers import reverse

from better500s import BETTER_500_LOG_DIR, BETTER_500_UNCAUGHT_DIR

class CaughtError(models.Model):
    """
    Object that represents a better 500 error.
    """
    user = models.ForeignKey("auth.User", blank=True, null=True)
    error_time = models.DateTimeField(blank=True, null=True)

    page_url = models.TextField(blank=True, null=True)
    epoch_time = models.IntegerField(blank=True, null=True, unique=True)

    simple_traceback = models.TextField(blank=True, null=True)
    exception_type = models.TextField(blank=True, null=True)
    user_notes = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return "%s - %s" % (self.exception_type, self.page_url)

    @property
    def epoch_file(self):
        return "%s.html" % (self.epoch_time)

    @property
    def view_url(self):
        return reverse("better_500_view_error", args=(self.pk,) )

    @property
    def traceback_file_contents(self):
        if BETTER_500_LOG_DIR:
            file_name = os.path.join(BETTER_500_LOG_DIR, self.error_time.strftime("%Y-%m-%d"), self.epoch_file)
            try:
                # Try to use the default storage. If not, fall back to local disk.
                from django.core.files.storage import default_storage
                f = default_storage.open(file_name)
            except:
                f = open(file_name,"r")

            full_trace = f.read()
            f.close()
            return full_trace
        else:
            return None

    def save(self, *args, **kwargs):
        first_save = False
        if not self.id:
            first_save = True
        super(CaughtError, self).save(*args, **kwargs)

        if first_save:
            if BETTER_500_LOG_DIR:
                folder = os.path.join(BETTER_500_LOG_DIR, BETTER_500_UNCAUGHT_DIR)
                debug_log_file = os.path.join(folder, self.epoch_file)

                new_folder = os.path.join(BETTER_500_LOG_DIR,self.error_time.strftime("%Y-%m-%d"))
                try:
                    # Try to use the default storage. If not, fall back to local disk.
                    from django.core.files.storage import default_storage
                    from django.core.files.base import ContentFile
                    f = default_storage.open(debug_log_file)
                    full_trace = f.read()
                    f.close()

                    new_file = os.path.join(new_folder, self.epoch_file)
                    default_storage.save(new_file, ContentFile(full_trace))
                    default_storage.delete(debug_log_file)
                except:
                    if not os.path.exists(new_folder):
                           os.makedirs(new_folder)

                    new_file = os.path.join(new_folder, self.epoch_file)

                    if os.path.exists(debug_log_file):
                        os.rename(debug_log_file, new_file)
                    
                    try:
                        f = open(new_file,"r")
                        full_trace = f.read()
                        f.close()
                    except:
                        pass

                # Fragile pulling of page URL and exception type    
                try:
                    request_url_index = full_trace.find("<th>Request URL:</th>")
                    page_url_start = full_trace.find("<td>",request_url_index)
                    page_url_end = full_trace.find("</td>",page_url_start)
                    self.page_url = full_trace[page_url_start+4:page_url_end]
                except:
                    pass

                try:
                    request_url_index = full_trace.find("<th>Exception Type:</th>")
                    exception_type_start = full_trace.find("<td>",request_url_index)
                    exception_type_end = full_trace.find("</td>",exception_type_start)
                    self.exception_type = full_trace[exception_type_start+4:exception_type_end]
                except:
                    pass

                self.save()
