import flask
import season
import os
import traceback
import time

config = season.stdClass()

config.dev = True
config.host = "__HOST__"
config.port = __PORT__
config.log_level = 2

config.jinja_variable_start_string = '{$'
config.jinja_variable_end_string = '$}'


config.filter = ['indexfilter']

def build(app, socketio):
    try:
        pass
    except:
        pass
    app.secret_key = 'dizest.net'
config.build = build

def on_error(framework, err):
    try:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
        errorlog = f"\033[91m[" + timestamp + "}][wiz][error]\n" + traceback.format_exc() + "\033[0m"
        branch = framework.wiz.branch()
        framework.socketio.emit("log", errorlog, namespace="/wiz", to=branch, broadcast=True)
    except:
        pass
    wiz = framework.wiz.instance()
    def handle_error(wiz, err):
        raise err
        pass
    handle_error(wiz, err)

config.on_error = on_error

def after_request(response):
    try:
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        response.headers['Cache-Control'] = 'public, max-age=0'
        
    except:
        pass
    return response

config.after_request = after_request

def get_resource_handler(resource_dirpath, resource_filepath):
    try:
        cache = season.cache
        if 'resources' not in cache:
            cache.resources = season.stdClass()
        
        _, ext = os.path.splitext(resource_filepath)
        filepath = os.path.join(resource_dirpath, resource_filepath)
        
        try:
            mode = flask.request.cookies.get("season-wiz-devmode")
        except:
            mode = False
        
        if mode != 'true':
            if filepath in cache.resources:
                return cache.resources[filepath]
        
        ext = ext.lower()
        
        allowed = ['.less', '.scss']
        if ext not in allowed:
            return None
        
        if ext == '.less':
            import lesscpy
            from six import StringIO
        
            f = open(filepath, 'r')
            lessfile = f.read()
            f.close()
            cssfile = lesscpy.compile(StringIO(lessfile), minify=True)
            response = flask.Response(str(cssfile))
            response.headers['Content-Type'] = 'text/css'
            cache.resources[filepath] = response
            return cache.resources[filepath]
        
        if ext == '.scss':
            import sass
            f = open(filepath, 'r')
            css = f.read()
            f.close()
            css = sass.compile(string=css)
            css = str(css)
            response = flask.Response(css)
            response.headers['Content-Type'] = 'text/css'
            cache.resources[filepath] = response
            return cache.resources[filepath]
        
    except:
        pass
    return None

config.build_resource = get_resource_handler
