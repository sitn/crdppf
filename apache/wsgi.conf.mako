
WSGIScriptAlias /${instanceid} ${directory}\apache\application.wsgi

<Location /${instanceid}>
    WSGIApplicationGroup %{GLOBAL}
    ${apache24_location}
</Location>
