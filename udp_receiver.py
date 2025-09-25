import socket
import time
import URBasic
import URBasic.robotModel
import URBasic.urScriptExt
import math as m

hostR = '169.254.229.173'  # Right arm IP
UDP_IP = "127.0.0.1"
UDP_PORT = 5005

print("Ports set up")

# Setup right robot
robotModelR = URBasic.robotModel.RobotModel()
robotR = URBasic.urScriptExt.UrScriptExt(hostR, robotModelR)

print('robot set up')

#home pose
robotR.movej(q=[m.radians(0),m.radians(-53.7),m.radians(65.3),m.radians(-146.6),m.radians(-93.6),m.radians(231)], a=1.4, v=0.3)


# Initialize realtime control
robotR.init_realtime_control()

# Get current TCP pose
start_pose = robotR.get_actual_tcp_pose()  # [x, y, z, rx, ry, rz]


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))


print("Waiting for Unity UDP messages...")

# Wait until a message is received before starting the loop
while True:
    data, addr = sock.recvfrom(1024)
    if data:
        print("First UDP message received, starting robot control loop.")
        break

while True:
    decoded_data = data.decode()

    pos_str, rot_str = decoded_data.split('|')

    x, y, z = map(float, pos_str.split(','))

    a_rad, b_rad, c_rad = map(float, rot_str.split(','))


    #print(f"Position (m) - X: {x:.3f}, Y: {y:.3f}, Z: {z:.3f}")
    print(f"Rotation (rad) - A: {a_rad:.3f}, B: {b_rad:.3f}, C: {c_rad:.3f}")
    #print("---")

    target_pose = [
        start_pose[0] + float(z)/-30,
        start_pose[1] + float(x)/30,
        start_pose[2] + float(y)/30,
        start_pose[3],#a_rad,
        start_pose[4],# Use the received rotation values directly
        start_pose[5]#c_rad,  # Use the received rotation values directly
    ]
    robotR.set_realtime_pose(target_pose)
    time.sleep(0.002)
    # Receive next message
    data, addr = sock.recvfrom(1024)



