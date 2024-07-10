# Main API module
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import CORS


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

auth = None

if getenv("AUTH_TYPE") == "auth":
    from api.v1.auth.auth import Auth
    auth = Auth()
elif getenv("AUTH_TYPE") == "basic_auth":
    from api.v1.auth.basic_auth import BasicAuth
    auth = BasicAuth()


@app.errorhandler(404)
def not_found(error):# -> tuple[Any, Literal[404]]:
    """ Handle 404 error """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized_error(error):# -> tuple[Any, Literal[401]]:
    """ Handle 401 error """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden_error(error):# -> tuple[Any, Literal[403]]:
    """ Handle 403 error """
    return jsonify({"error": "Forbidden"}), 403


@app.before_request
def before_request() -> None:
    """ Request filter """
    all_pathes = [
        '/api/v1/status/',
        '/api/v1/unauthorized/',
        '/api/v1/forbidden/']
    if auth:
        if auth.require_auth(request.path, all_pathes):
            if auth.authorization_header(request) is None:
                abort(401)
            if auth.current_user(request) is None:
                abort(403)


if __name__ == "__main__":
    main_host = getenv("API_HOST", "0.0.0.0")
    main_port = getenv("API_PORT", "5000")
    app.run(host=main_host, port=main_port)

