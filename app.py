from flask import Flask, request, jsonify
import serial

app = Flask(__name__)

# Initialize serial communication
ser = serial.Serial('/dev/cu.usbserial-A1076I9P', 115200)  # Replace with your port

@app.route('/move', methods=['POST'])
def move():
    data = request.json
    x = data.get('x')
    y = data.get('y')
    z = data.get('z')
    speed = data.get('speed', 1000)  # Default speed if not provided

    command = f"#0 G0 X{x} Y{y} Z{z} F{speed}\n"
    ser.write(command.encode())  # Send the command to the uArm
    
    # Read the response (assuming the uArm returns "ok" or an error)
    response = ser.readline().decode().strip()

    if "ok" in response:
        return jsonify({"status": "ok"}), 200
    else:
        return jsonify({"status": "error", "message": response}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)