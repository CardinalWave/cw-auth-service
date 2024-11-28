
from flask import Flask, jsonify, request
from flask import request as FlaskRequest

from .auth import AuthCredentials, AuthRequest

from .http_types.http_request import HttpRequest


def init_routes(app):
    @app.route('/login', methods=['POST'])  # Mudamos para POST
    def login_rqst():
        try:
            http_request = get_request(request)
            if not http_request:
                return jsonify({"error": "Request must be JSON"}), 400

            data = http_request.body
            credentials = AuthCredentials(
                email=data.get("email"),
                password=data.get("password"))
            result = AuthRequest().login(credentials)
            return result, 200
        except Exception as e:
            print(e)
            return jsonify({"error": str(e)}), 401

    @app.route('/register', methods=['POST'])
    def register_rqst():
        try:
            http_request = get_request(request)
            if not http_request:
                return jsonify({"error": "Request must be JSON"}), 400

            data = http_request.body
            credentials = AuthCredentials(
                username=data.get("username"),
                email=data.get("email"),
                password=data.get("password")
            )
            result = AuthRequest().register(credentials)
            return result, 200
        except Exception as e:
            print(e)
            return jsonify({"error": str(e)}), 400

    @app.route('/logout', methods=['POST'])
    def logout_rqst():
        try:
            http_request = get_request(request)
            if not http_request:
                return jsonify({"error": "Request must be JSON"}), 400

            data = http_request.body
            return AuthRequest().logout(AuthCredentials(user_token=data.get("token")))
        except Exception as e:
            return f"Error: {e}"

def get_request(request_: FlaskRequest):
    body = None
    if request_.data: body = request_.json
    http_request = HttpRequest(
        body=body,
        headers=request_.headers,
        query_params=request_.args,
        path_params=request_.view_args,
        url=request_.full_path
    )

    return http_request

