from flask import Flask, request, jsonify
from .auth import login, logout, register, update_password, AuthCredentials


def init_routes(app):
    @app.route('/login', methods=['POST'])  # Mudamos para POST
    def login_rqst():
        try:
            data = request.json  # Espera receber dados em formato JSON
            credentials = AuthCredentials(
                email=data.get("email"),
                password=data.get("password")
            )
            result = login(credentials)
            return result, 200
        except Exception as e:
            return jsonify({"error": str(e)}), 401  # Retorna 401 em caso de erro de autenticação

    @app.route('/register', methods=['POST'])
    def register_rqst():
        try:
            data = request.json  # Espera receber dados em formato JSON
            credentials = AuthCredentials(
                username=data.get("username"),
                email=data.get("email"),
                password=data.get("password")
            )
            result = register(credentials)
            return jsonify({"message": result}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    @app.route('/logout', methods=['GET'])
    def logout_rqst():
        if request.method == 'GET':
            try:
                return logout()
            except Exception as e:
                return f"Error: {e}"

    @app.route('/get_upd', methods=['GET'])
    def update_rqst():
        if request.method == 'GET':
            try:
                credentials = AuthCredentials(
                    email=request.args.get("email"),
                    password=request.args.get("password")
                )
                token_recovery = request.args.get("token")
                return update_password(credentials, token_recovery)
            except Exception as e:
                return f"Error: {e}"
