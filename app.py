from flask import Flask, render_template, request, jsonify, session
import cv2

app = Flask(__name__)
app.secret_key = "your_secret_key"  # session management



# Dummy users database
users = {"admin": "password123", "user1": "mypassword"}

# Route for the index page
@app.route('/')
def index():
    return render_template('index.html')

# Route for the take page
@app.route('/take')
def take():
    return render_template('take.html')

# Login route (POST method)
@app.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")
      
        if username in users and users[username] == password:
            session["user"] = username  # Store user in session
            return jsonify({"success": True, "message": "Login successful!"})
        else:
            return jsonify({"success": False, "message": "Invalid credentials"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Logout route
@app.route("/logout")
def logout():
    session.pop("user", None)
    return jsonify({"success": True, "message": "Logged out successfully"})

# Camera script route
@app.route("/run-script")
def run_script():
    try:
        cap = cv2.VideoCapture(0)  # Open default camera (0)
        
        if not cap.isOpened():
            raise Exception("Error: Could not open camera.")

        while True:
            ret, frame = cap.read()  # Capture frame-by-frame
            if not ret:
                raise Exception("Error: Failed to grab frame.")

            cv2.imshow("Camera Feed", frame)  # Display the frame

            # Press 'q' to quit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        return jsonify({"message": "Camera closed successfully."})  # Response after closing

    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Return error message in JSON format

    finally:
        if 'cap' in locals():  # Ensure 'cap' is defined
            cap.release()  # Release the camera
        cv2.destroyAllWindows()  # Close OpenCV windows

if __name__ == '__main__':
    app.run(debug=True)
