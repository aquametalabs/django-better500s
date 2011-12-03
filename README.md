Overview
========

django-better500s is a library that makes 500 errors more user-friendly, and developer friendly.  It logs the full error traceback (as if it were in DEBUG mode), as well as a user's description of what they were trying to do.

Pull requests are quite welcome!


Usage
=====

## Installation ##

1. `pip install django-better500s`

2. Edit your `settings.py:`

	```
	INSTALLED_APPS += ("better500s",)
	MIDDLEWARE_CLASSES += ("better500s.middleware.Better500s",)

	# Set any optional settings (below)
	BETTER_500_DEFAULT_RETURN_URL_NAME = "home_page"
	BETTER_500_LOG_DIR = join(PROJECT_ROOT, 'logs', 'better_500')
	BETTER_500_FROM_EMAIL = "foo@example.com"
	BETTER_500_TO_EMAILS = ["bar@example.com",]
	BETTER_500_UNCAUGHT_DIR = "Uncaught Logs"

	```

4. (optional) Add in the urls:

	```
	urlpatterns += patterns('',          
		url(r'better500s/',   include('better500s.urls',  namespace="better500s",  app_name='better500s') ),
	)
	```

5. Enjoy better error reports.


### Optional Settings:

* `BETTER_500_DEFAULT_RETURN_URL_NAME` - The url name that the "Go Home" button should link to. If none, the button is hidden.
	Defaults to None. 

* `BETTER_500_LOG_DIR` - Where the full log traces should be stored.
	Defaults to `PROJECT_ROOT/logs/better500s`.  

* `BETTER_500_FROM_EMAIL` - The email that notifications should be sent from.
	Defaults to `DEFAULT_FROM_EMAIL`. 

* `BETTER_500_TO_EMAILS` - The set of email that notifications should be sent to.
	Defaults to `ADMINS`. 

* `BETTER_500_UNCAUGHT_DIR` - Where to store log traces in which the 500 handling page crashed, or the user's browser crashed.
	Defaults to `UNCAUGHT`. 

* `BETTER_500_AJAX_URL` - URL for ajax callback, that saves the log, and sends off an email.
	Defaults to `500-callback`. 

* `BETTER_500_POST_URL` - URL for user crash report posting.
	Defaults to `500-saved`. 




### How it works:




