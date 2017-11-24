ScriptAlias /${instanceid}/wmscrdppf ${mapserverexec}
<Location /${instanceid}/wmscrdppf>
   # If you use tilecache and want to prevent direct WMS access, uncomment 
   # the following lines:
   ${mapserv_access_control}
   ${mapserv_allow}
   SetHandler fcgid-script
   SetEnv MS_MAPFILE ${directory}/mapserver/crdppf.map
</Location>

