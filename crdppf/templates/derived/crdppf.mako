<%inherit file="/base/index.mako"/>

% if debug:
    <%!
    from jstools.merge import Merger
    %>
    <%
    jsbuild_cfg = request.registry.settings.get('jsbuild_cfg')
    jsbuild_root_dir = request.registry.settings.get('jsbuild_root_dir')
    %>
    % for script in Merger.from_fn(jsbuild_cfg.split(), root_dir=jsbuild_root_dir).list_run(['crdppf.js']):
    <script type="text/javascript" src="${request.static_url(script.replace('/', ':', 1))}"></script>
    % endfor

% else:
    <script type="text/javascript" src="${request.static_url('crdppf:static/build/crdppf.js')}"></script>
% endif

    <script type="text/javascript">
        OpenLayers.Util.extend(OpenLayers.Lang.fr, {
            'plan_ville_${request.tile_date[1]}': 'Plan de ville',
            'plan_cadastral_${request.tile_date[0]}': 'Plan cadastral'
        });
    </script>
    
<div id="main"></div>
