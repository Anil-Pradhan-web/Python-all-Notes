# Building REST APIs with Flask

### Simple Explanation (Hinglish)
**REST API** wo interface hai jisse frontend (React, Mobile App) backend se baat karta hai. **Flask** ek lightweight Python framework hai APIs banane ke liye. JSON format mein data exchange hota hai.

### Theory (Clear + Structured)
- **HTTP Methods**: GET (read), POST (create), PUT/PATCH (update), DELETE (delete).
- **Endpoints**: URLs jahan API requests bheji jati hain.
- **JSON**: Data exchange format (JavaScript Object Notation).
- **Status Codes**: 200 (OK), 201 (Created), 400 (Bad Request), 404 (Not Found), 500 (Server Error).

### Examples with Hinglish Comments

```python
# Pehle install karo: pip install flask

from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# In-memory database (temporary storage)
users = [
    {"id": 1, "name": "Rahul", "email": "rahul@example.com"},
    {"id": 2, "name": "Priya", "email": "priya@example.com"}
]

# Root endpoint
@app.route('/')
def home():
    return jsonify({"message": "Welcome to the API!"})
    # # JSON response bhejo

# GET - Saare users fetch karna
@app.route('/users', methods=['GET'])
def get_users():
    return jsonify({
        "success": True,
        "count": len(users),
        "data": users
    }), 200
    # # 200 status code ke saath response

# GET - Ek user fetch karna
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = next((u for u in users if u['id'] == user_id), None)
    
    if user is None:
        return jsonify({"error": "User not found"}), 404
        # # 404 agar user na mile
    
    return jsonify({"success": True, "data": user}), 200

# POST - Naya user banana
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    # # Request body se JSON data nikalo
    
    # Validation
    if not data or 'name' not in data or 'email' not in data:
        return jsonify({"error": "Name and email are required"}), 400
    
    # New user create karna
    new_user = {
        "id": len(users) + 1,
        "name": data['name'],
        "email": data['email'],
        "created_at": datetime.now().isoformat()
    }
    
    users.append(new_user)
    
    return jsonify({
        "success": True,
        "message": "User created successfully",
        "data": new_user
    }), 201
    # # 201 Created status code

# PUT - User update karna
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = next((u for u in users if u['id'] == user_id), None)
    
    if user is None:
        return jsonify({"error": "User not found"}), 404
    
    data = request.get_json()
    
    # Update fields
    if 'name' in data:
        user['name'] = data['name']
    if 'email' in data:
        user['email'] = data['email']
    
    return jsonify({
        "success": True,
        "message": "User updated",
        "data": user
    }), 200

# DELETE - User delete karna
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    global users
    user = next((u for u in users if u['id'] == user_id), None)
    
    if user is None:
        return jsonify({"error": "User not found"}), 404
    
    users = [u for u in users if u['id'] != user_id]
    
    return jsonify({
        "success": True,
        "message": "User deleted successfully"
    }), 200

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

# Run the server
if __name__ == '__main__':
    app.run(debug=True, port=5000)
    # # debug=True se auto-reload hota hai changes pe
```

### Testing API with curl
```bash
# Saare users fetch karo
curl http://localhost:5000/users

# Ek user fetch karo
curl http://localhost:5000/users/1

# Naya user banao
curl -X POST http://localhost:5000/users \
  -H "Content-Type: application/json" \
  -d '{"name": "Aman", "email": "aman@example.com"}'

# User update karo
curl -X PUT http://localhost:5000/users/1 \
  -H "Content-Type: application/json" \
  -d '{"name": "Rahul Kumar"}'

# User delete karo
curl -X DELETE http://localhost:5000/users/1
```

### Common Mistakes
1. **Validation na karna**: User input ko hamesha validate karo.
2. **Error handling na karna**: Proper error messages aur status codes bhejo.
3. **Sensitive data expose karna**: Passwords aur sensitive info response mein mat bhejo.

### Interview Notes
1. **REST Principles**: Statelessness, Client-Server architecture, Uniform Interface.
2. **Authentication**: JWT tokens, OAuth, API keys for securing endpoints.

## Practice Questions (Sirf 5 -- Concept Clear Karne Wale)

1. **(Basic)** Create a simple API with one endpoint that returns "Hello World".
2. **(Basic)** Create a GET route that accepts a parameter in the URL and returns it in JSON.
3. **(Medium)** Build a CRUD API for a "Products" resource with name, price, and description.
4. **(Medium)** Add input validation to a POST endpoint and return a 400 Bad Request error if validation fails.
5. **(Hard)** Add authentication simulation or JWT tokens handling to protect specific routes in your Flask API.
