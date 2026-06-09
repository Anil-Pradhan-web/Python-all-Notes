# APIs and Requests Library

## Simple Explanation (Hinglish)
Jab aap Amazon se kuch order karte ho, peechay bohot saari websites aapas mein baat karti hain (payment portal, inventory, shipping). Internet par code ko aapas me baat karwane ke liye APIs (Application Programming Interface) hote hain. Python mein `requests` library postman ka kaam karti hai. Ye website se data lekar aati hai aur bhejti hai.

## Theory (Clear + Structured)
The `requests` library is the de facto standard for making HTTP requests in Python. 
Common HTTP Methods:
- **GET**: Used to retrieve data from a server.
- **POST**: Used to send new data to a server (e.g., submitting a form).
- **PUT / PATCH**: Used to update existing data.
- **DELETE**: Used to remove data.

## Syntax
```python
import requests

response = requests.get("https://api.url.com")
data = response.json()
```

## Examples

```python
import requests

# Example 1: Basic GET Request
url = "https://jsonplaceholder.typicode.com/users/1"
response = requests.get(url)

# Check if request was successful (Status Code 200)
if response.status_code == 200:
    user_data = response.json() # Converts JSON text to Python Dictionary
    print(f"Name: {user_data['name']}")
    print(f"Email: {user_data['email']}")
else:
    print("Error linking to API", response.status_code)

# Example 2: Sending data using POST
post_url = "https://jsonplaceholder.typicode.com/posts"
new_post = {
    "title": "Learning Python",
    "body": "Requests library is great!",
    "userId": 1
}

res = requests.post(post_url, json=new_post)
print("Created Post ID:", res.json()["id"])
```

## Dry Run / Explanation
* `requests.get()`: Isne background me bilkul wahi kiya jo humara browser karta hai jab hum url enter karte hain. Farak itna hai ki server ne webpage return karne ki jagah raw JSON data (text) return kiya.
* `response.status_code`: Har response ke sath ek code aata hai. `200` matlab 'OK Sab badhiya'. `404` matlab 'Not Found'. `500` matlab 'Server khud fat gaya'.
* `response.json()`: Internet se humesha JSON me data travel karta hai jo string hota hai. Ye function literally us string ko `dict` me badal deta hai taaki hum keys access kar sake.

## Common Mistakes
1. Not handling timeouts. If the remote API server is down, your Python code will hang infinitely waiting for a response. Always use `requests.get(url, timeout=5)`.
2. Assuming `response.text` is a dictionary. You have to explicitly parse it using `.json()` or using the `json.loads` module.

## Interview Notes
1. **Status Codes**: Memorize common HTTP status codes (200, 201, 400, 401, 403, 404, 500).
2. **REST APIs**: Know what REST architecture means ideally (Representational State Transfer).

## Practice Questions (Sirf 5 -- Concept Clear Karne Wale)

1. **(Basic)** GET request bhejo to https://api.github.com, status code print karo.
2. **(Basic)** JSON response parse karo, keys print karo.
3. **(Medium)** POST request bhejo with JSON body: {"name":"test"}.
4. **(Medium)** URL se image download karo aur local file mein save karo.
5. **(Hard)** Public API ko parameters ke saath call karo, response parse karo.