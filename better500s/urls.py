from django.conf.urls.defaults import patterns, url

from better500s import BETTER_500_AJAX_URL, BETTER_500_POST_URL
from better500s import views

urlpatterns = patterns('',
    url(r'^%s' % BETTER_500_AJAX_URL, views.ajax_error_save, name='better_500_response'),
    url(r'^%s' % BETTER_500_POST_URL, views.user_error_submit, name='better_500_saved'),
    url(r'^better-500-view/(?P<error_id>\d+)', views.view_error, name='better_500_view_error'),    
    url(r'^better-500-traceback/(?P<error_id>\d+)', views.traceback_source, name='better_500_traceback_source'),        
)