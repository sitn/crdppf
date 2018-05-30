[app:main]
use = egg:crdppfportal
 
pyramid_oereb.cfg.file = ${directory}/pyramid_oereb_standard.yml
pyramid_oereb.cfg.section = pyramid_oereb

pyramid.reload_templates = false
pyramid.debug_authorization = false
pyramid.debug_notfound = false
pyramid.debug_routematch = false
pyramid.default_locale_name = en
pyramid.includes =
    pyramid_tm

app.cfg = %(here)s/.build/config.yaml

[server:main]
use = egg:waitress#main
host = 0.0.0.0
port = ${waitress_port}

# Begin logging configuration

[loggers]
keys = root, crdppf

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARN
handlers = console

[logger_crdppf]
level = WARN
handlers =
qualname = crdppf

[logger_sqlalchemy]
level = WARN
handlers =
qualname = sqlalchemy.engine
# "level = INFO" logs SQL queries.
# "level = DEBUG" logs SQL queries and results.
# "level = WARN" logs neither.  (Recommended for production systems.)

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(asctime)s %(levelname)-5.5s [%(name)s][%(threadName)s] %(message)s

# End logging configuration
