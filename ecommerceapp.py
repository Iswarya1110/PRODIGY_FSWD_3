from http.server import HTTPServer, SimpleHTTPRequestHandler
import urllib.parse

users = {"admin": "admin123"}
products = ["Apple", "Banana", "Orange"]
cart = []

# HTML template for adding style
def html_template(content):
    return f"""
    <html>
    <head>
        <title>Shopping Cart</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background: #d3d3d3; /* Grey background */
                color: #333;
                text-align: center;
                padding: 50px;
            }}
            h2 {{
                color: #555; /* Darker grey for headings */
            }}
            ul {{
                list-style-type: none;
                padding: 0;
            }}
            li {{
                margin: 10px;
                font-size: 18px;
            }}
            a {{
                color: #333; /* Dark grey for links */
                text-decoration: none;
                padding: 5px 10px;
                border-radius: 5px;
            }}
            a:hover {{
                background-color: #888; /* Lighter grey on hover */
                color: white;
            }}
            .container {{
                max-width: 600px;
                margin: auto;
                padding: 20px;
                background: white;
                border-radius: 8px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }}
            form {{
                font-size: 18px;
                text-align: left;
            }}
            input[type="text"], input[type="password"] {{
                padding: 10px;
                margin: 5px 0;
                width: 100%;
                border: 1px solid #ccc;
                border-radius: 5px;
            }}
            button {{
                padding: 10px 20px;
                background-color: #555;
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
            }}
            button:hover {{
                background-color: #888;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            {content}
        </div>
    </body>
    </html>
    """

class MyHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/login":
            # Display the login page
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            login_form = """
            <h2>Login</h2>
            <form action="/login" method="POST">
                Username: <input type="text" name="username"><br>
                Password: <input type="password" name="password"><br>
                <button type="submit">Login</button>
            </form>
            """
            self.wfile.write(html_template(login_form).encode())

        elif self.path == "/products":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            items = "".join(f"<li>{p} <a href='/add?item={p}'>Add to cart</a></li>" for p in products)
            cart_link = "<a href='/cart'>View Cart</a>"
            self.wfile.write(html_template(f"<h2>Products</h2><ul>{items}</ul>{cart_link}").encode())

        elif self.path.startswith("/add"):
            item = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query).get("item", [""])[0]
            if item:
                cart.append(item)
            self.send_response(302)
            self.send_header("Location", "/products")
            self.end_headers()

        elif self.path == "/cart":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            cart_items = "".join(f"<li>{c}</li>" for c in cart)
            self.wfile.write(html_template(f"<h2>Cart</h2><ul>{cart_items}</ul><a href='/products'>Back</a>").encode())

        else:
            super().do_GET()

    def do_POST(self):
        if self.path == "/login":
            length = int(self.headers["Content-Length"])
            body = self.rfile.read(length).decode()
            data = urllib.parse.parse_qs(body)
            username = data.get("username", [""])[0]
            password = data.get("password", [""])[0]
            if users.get(username) == password:
                self.send_response(302)
                self.send_header("Location", "/products")
                self.end_headers()
            else:
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(html_template(b"Invalid login. <a href='/login'>Try again</a>").encode())

if __name__ == "__main__":
    server = HTTPServer(("localhost", 8000), MyHandler)
    print("Server running at http://localhost:8000")
    server.serve_forever()
