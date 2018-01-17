
WSGIScriptAlias /${instanceid} ${directory}\apache\application.wsgi

<Location /${instanceid}>
    ${apache24_modwsgi}
    ${apache24_location}
</Location>
