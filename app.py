from flask import Flask, request, jsonify
import serial

app = Flask(__name__)

# Initialize serial communication
#ser = serial.Serial('/dev/cu.wlan-debug', 115200) # debug line
ser = serial.Serial('/dev/cu.usbserial-A1076I9P', 115200)  # Your port here

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
    

@app.route('/end_effector/grip', methods=['POST'])
def grip():
    try:
        command = "#0 M2232 V1\n"  # Command to close the gripper
        ser.write(command.encode())
        response = ser.readline().decode().strip()

        if "ok" in response:
            return jsonify({"status": "ok"}), 200
        else:
            return jsonify({"status": "error", "message": response}), 400
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/end_effector/release', methods=['POST'])
def release():
    try:
        command = "#0 M2232 V0\n"  # Command to open the gripper
        ser.write(command.encode())
        response = ser.readline().decode().strip()

        if "ok" in response:
            return jsonify({"status": "ok"}), 200
        else:
            return jsonify({"status": "error", "message": response}), 400
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/end_effector/suction_on', methods=['POST'])
def suction_on():
    try:
        command = "#0 M2231 V1\n"  # Command to turn on the suction
        ser.write(command.encode())
        response = ser.readline().decode().strip()

        if "ok" in response:
            return jsonify({"status": "ok"}), 200
        else:
            return jsonify({"status": "error", "message": response}), 400
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/end_effector/suction_off', methods=['POST'])
def suction_off():
    try:
        command = "#0 M2231 V0\n"  # Command to turn off the suction
        ser.write(command.encode())
        response = ser.readline().decode().strip()

        if "ok" in response:
            return jsonify({"status": "ok"}), 200
        else:
            return jsonify({"status": "error", "message": response}), 400
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/end_effector/set_mode', methods=['POST'])
def set_mode():
    try:
        data = request.json
        mode = data.get('mode')  # Expect mode to be 0 (Normal), 1 (Laser), etc.
        command = f"#0 M2400 S{mode}\n"
        ser.write(command.encode())
        response = ser.readline().decode().strip()

        if "ok" in response:
            return jsonify({"status": "ok"}), 200
        else:
            return jsonify({"status": "error", "message": response}), 400
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)