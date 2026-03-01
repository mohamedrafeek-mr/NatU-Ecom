# Render will use this command when starting the web service.
# We point Gunicorn directly at the config package instead of using the
# old "ecompro" package name, which no longer exists after the
# restructuring that placed settings and wsgi in `config/`.

web: gunicorn config.wsgi
