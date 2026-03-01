# Render will use this command when starting the web service.
# The project package is now `config`, not `ecompro`.  Point Gunicorn
# at the correct module and include the callable name explicitly.  Also
# bind to the port Render provides via $PORT.

web: gunicorn config.wsgi:application --bind 0.0.0.0:$PORT
