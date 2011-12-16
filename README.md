Overview
========

django-better500s is a library that makes 500 errors more user-friendly, and developer friendly. It logs the full error traceback (as if it were in DEBUG mode), as well as a user's description of what they were trying to do.

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

4. Add in the urls:

	```
	urlpatterns += patterns('',          
		url(r'better500s/',   include('better500s.urls',  namespace="better500s",  app_name='better500s') ),
	)
	```

5. Enjoy better error reports.


### Optional Settings:

* `BETTER_500_LOG_DIR` - Where the full log traces should be stored (on `default_storage`, or failing that, locally).
	Defaults to `"PROJECT_ROOT/logs/better500s"`.  

* `BETTER_500_FROM_EMAIL` - The email that notifications should be sent from.
	Defaults to `settings.DEFAULT_FROM_EMAIL`. 

* `BETTER_500_TO_EMAILS` - The set of email that notifications should be sent to.
	Defaults to `settings.ADMINS`. 

* `BETTER_500_UNCAUGHT_DIR` - Where to store log traces in which the 500 handling page crashed, or the user's browser crashed.
	Defaults to `"UNCAUGHT"`. 

* `BETTER_500_AJAX_URL` - URL for ajax callback, that saves the log, and sends off an email.
	Defaults to `"better-500-callback/"`. 

* `BETTER_500_POST_URL` - URL for user crash report posting.
	Defaults to `"better-500-saved/"`. 

* `BETTER_500_DEFAULT_RETURN_URL_NAME` - The url name that the "Go Home" button should link to. If none, the button is hidden.
	Defaults to `None`. 



How it works:
=============

1. 500 errors (only) are caught.
2. Full debug page traceback is generated, and saved to the `UNCAUGHT_DIR`.
3. A "We're sorry / Tell us what you were doing" page loads.
4. On load, that page ajax pings the server.
5. On ping, the view files the log into a date-organized folder, and emails the `TO_EMAILs` with a link.
6. If the user submits a report, that report is saved to the database, tied to the log file.  A second email is sent, with the user's report.
7. An admin can click the view link, and see the full traceback, and the user's report.


Templates and Customization
===========================

### Templates

* `500_handler.html` - This template is what users see when a 500 occurs, and where they can submit their report. 

* `feedback_saved.html` - If a user submits a report, this page is what they see. Links to the page that produced the error, and optionally, home.

* `view_error.html` - Developer-side template for viewing captured 500s

* `admin_email.txt` - Template for the 500 error email.

* `error_with_notes_email.txt` - Template for the user bug report email.


### Log file storage

By default, django-better500s uses the `default_backend` to store error logs. If that fails, it falls back local file storage.


Credits
=======
django-better500s was written by Steven Skoczen for Aquameta.



