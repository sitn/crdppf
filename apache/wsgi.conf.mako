
WSGIScriptAlias /${instanceid} ${directory}\apache\application.wsgi

<Location /${instanceid}>
    ${apache24_location}
</Location>
