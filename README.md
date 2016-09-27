# django-simple-history-and-x-user

This package is an integration for django-simple-history , allows you to track the x-user also in the history entries. 

# What you should have

django-simple-history working in your project
Ref:- https://django-simple-history.readthedocs.io/en/latest/

# Afterwards
1. comment out(remove)  'simple_history.middleware.HistoryRequestMiddleware' from middleware settings.
2. Add our custom middleware path to the middleware ware settings.
3. The clients should request with proper HTTP_X_REQUESTED_WITH and HTTP_AUTHORIZATION headers. 


