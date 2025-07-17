from flask import Blueprint, request, jsonify

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

# In-memory users list (just for testing)
users = []

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No input provided"}), 400

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not all([username, email, password]):
        return jsonify({"error": "Missing fields"}), 400

    for user in users:
        if user['email'] == email:
            return jsonify({"error": "Email already registered"}), 400

    new_user = {
        "id": len(users) + 1,
        "username": username,
        "email": email,
        "password": password  #  Not hashed, just for mock use
    }

    users.append(new_user)
    return jsonify({"message": "User registered", "user": new_user}), 201
