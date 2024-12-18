import machine
import network
import socket
+import time
import math

UDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
packet = bytearray(4)

ESCout_1 = 0
ESCout_2 = 0
ESCout_3 = 0
ESCout_4 = 0
input_PITCH = 50
input_ROLL = 50
input_YAW = 50
input_THROTTLE = 0
Mode = 0
wall_car_init = False
set_motor_const_speed = False
target_axis = 0
target_dirr = 0
wheal_state = False
pwm_stops = 0
arr = [20, 10, 20, 10]
order = [0, 0, 0, 0]
temp_arr = [0, 0, 0, 0]
pulldown_time_temp = [0, 0, 0, 0, 0]
pulldown_time = [0, 0, 0, 0, 0]
pulldown_time_temp_loop = [0, 0, 0, 0, 0]
pin = [14, 12, 13, 15]
i = 0
j = 0
temp_i = 0
temp = 0
orderState1 = False
orderState2 = False
orderState3 = False
orderState4 = False
gyro_x = 0
gyro_y = 0
gyro_z = 0
acc_x = 0
acc_y = 0
acc_z = 0
temperature = 0
acc_total_vector = 0
angle_pitch = 0
angle_roll = 0
angle_yaw = 0
prev_roll = 0
prev_pitch = 0
prev_yaw = 0
set_gyro_angles = False
angle_roll_acc = 0
angle_pitch_acc = 0
angle_pitch_output = 0
angle_roll_output = 0
angle_yaw_output = 0
Time = 0
timePrev = 0
elapsedTime = 0
P_factor = 0
acceleration_x = 0
acceleration_y = 0
acceleration_z = 0
gyro_x_cal = 0
gyro_y_cal = 0
gyro_z_cal = 0
pitch_PID = 0
roll_PID = 0
yaw_PID = 0
roll_error = 0
roll_previous_error = 0
pitch_error = 0
pitch_previous_error = 0
yaw_error = 0
yaw_previous_error = 0
roll_pid_p = 0
roll_pid_d = 0
roll_pid_i = 0
pitch_pid_p = 0
pitch_pid_i = 0
pitch_pid_d = 0
yaw_pid_p = 0
yaw_pid_i = 0
yaw_pid_d = 0
roll_desired_angle = 0
pitch_desired_angle = 0
yaw_desired_angle = 0
twoX_kp = 5
twoX_ki = 0.003
twoX_kd = 1.4
yaw_kp = 8
yaw_ki = 0
yaw_kd = 4

def PWM_callback(timer):
    global pwm_stops, pulldown_time_temp, order, pin
    if pwm_stops == 0:
        pulldown_time_temp[0] = pulldown_time_temp_loop[0]
        pulldown_time_temp[1] = pulldown_time_temp_loop[1]
        pulldown_time_temp[2] = pulldown_time_temp_loop[2]
        pulldown_time_temp[3] = pulldown_time_temp_loop[3]
        pulldown_time_temp[4] = pulldown_time_temp_loop[4]
        pwm_stops = 1
        if input_THROTTLE != 0:
            machine.Pin(pin[order[0]], machine.Pin.OUT).value(1)
            machine.Pin(pin[order[1]], machine.Pin.OUT).value(1)
            machine.Pin(pin[order[2]], machine.Pin.OUT).value(1)
            machine.Pin(pin[order[3]], machine.Pin.OUT).value(1)
        timer.init(period=80 * pulldown_time_temp[0], mode=machine.Timer.ONE_SHOT, callback=PWM_callback)
    elif pwm_stops == 1:
        pwm_stops = 2
        machine.Pin(pin[order[0]], machine.Pin.OUT).value(0)
        timer.init(period=80 * pulldown_time_temp[1], mode=machine.Timer.ONE_SHOT, callback=PWM_callback)
    elif pwm_stops == 2:
        pwm_stops = 3
        machine.Pin(pin[order[1]], machine.Pin.OUT).value(0)
        timer.init(period=80 * pulldown_time_temp[2], mode=machine.Timer.ONE_SHOT, callback=PWM_callback)
    elif pwm_stops == 3:
        pwm_stops = 4
        machine.Pin(pin[order[2]], machine.Pin.OUT).value(0)
        timer.init(period=80 * pulldown_time_temp[3], mode=machine.Timer.ONE_SHOT, callback=PWM_callback)
    elif pwm_stops == 4:
        pwm_stops = 0
        machine.Pin(pin[order[3]], machine.Pin.OUT).value(0)
        timer.init(period=80 * pulldown_time_temp[4], mode=machine.Timer.ONE_SHOT, callback=PWM_callback)

def setup():
    global pin, timer, UDP
    machine.Pin("D5", machine.Pin.OUT).value(0)
    machine.Pin("D6", machine.Pin.OUT).value(0)
    machine.Pin("D7", machine.Pin.OUT).value(0)
    machine.Pin("D8", machine.Pin.OUT).value(0)
    machine.Pin("D0", machine.Pin.OUT).value(0)
    machine.Pin(pin[0], machine.Pin.OUT).value(0)
    machine.Pin(pin[1], machine.Pin.OUT).value(0)
    machine.Pin(pin[2], machine.Pin.OUT).value(0)
    machine.Pin(pin[3], machine.Pin.OUT).value(0)
    machine.Pin("D0", machine.Pin.OUT).value(0)
    print(network.WLAN(network.STA_IF).ifconfig()[0])
    UDP.bind(("", 9999))
    timer = machine.Timer(1)
    timer.init(period=6000, mode=machine.Timer.ONE_SHOT, callback=init_IMU)

def init_IMU(timer):
    global gyro_x_cal, gyro_y_cal, gyro_z_cal
    i2c = machine.I2C(scl=machine.Pin(5), sda=machine.Pin(4))
    i2c.start()
    i2c.writeto(0x68, bytearray([0x6B, 0x00]))
    i2c.writeto(0x68, bytearray([0x1C, 0x08]))
    i2c.writeto(0x68, bytearray([0x1B, 0x18]))
    i2c.writeto(0x68, bytearray([0x1A, 0x03]))
    for cal_int in range(4000):
        if cal_int % 125 == 0:
            print(".")
        i2c.writeto(0x68, bytearray([0x3B]))
        data = i2c.readfrom(0x68, 14)
        acc_y = (data[0] << 8) | data[1]
        acc_x = (data[2] << 8) | data[3]
        acc_z = (data[4] << 8) | data[5]
        temperature = (data[6] << 8) | data[7]
        gyro_y = (data[8] << 8) | data[9]
        gyro_x = (data[10] << 8) | data[11]
        gyro_z = (data[12] << 8) | data[13]
        gyro_x_cal += gyro_x
        gyro_y_cal += gyro_y
        gyro_z_cal += gyro_z
        time.sleep_us(100)
    gyro_x_cal //= 4000
    gyro_y_cal //= 4000
    gyro_z_cal //= 4000
    timer.init(period=1000, mode=machine.Timer.PERIODIC, callback=loop)

def loop(timer):
    global gyro_x_cal, gyro_y_cal, gyro_z_cal, angle_pitch, angle_roll, angle_yaw, set_gyro_angles, angle_pitch_output, angle_roll_output, angle_yaw_output, roll_desired_angle, pitch_desired_angle, input_ROLL, input_PITCH, input_THROTTLE, Mode, wall_car_init, set_motor_const_speed, target_axis, target_dirr, arr, temp_arr, order, pulldown_time, pulldown_time_temp_loop, orderState1, orderState2, orderState3, orderState4, wheal_state, Time, timePrev, elapsedTime, gyro_x, gyro_y, gyro_z, acc_x, acc_y, acc_z, acceleration_x, acceleration_y, acceleration_z, roll_error, roll_previous_error, pitch_error, pitch_previous_error, yaw_error, yaw_previous_error, roll_pid_p, roll_pid_d, roll_pid_i, pitch_pid_p, pitch_pid_i, pitch_pid_d, yaw_pid_p, yaw_pid_i, yaw_pid_d, roll_PID, pitch_PID, yaw_PID, roll_desired_angle, pitch_desired_angle, yaw_desired_angle, twoX_kp, twoX_ki, twoX_kd, yaw_kp, yaw_ki, yaw_kd, ESCout_1, ESCout_2, ESCout_3, ESCout_4, pulldown_time_temp, pulldown_time_temp_loop, pulldown_time, order, pin, i, j, temp_i, temp, packet, UDP
    timePrev = Time
    Time = time.ticks_us()
    elapsedTime = (Time - timePrev) / 1000000
    i2c = machine.I2C(scl=machine.Pin(5), sda=machine.Pin(4))
    i2c.start()
    i2c.writeto(0x68, bytearray([0x3B]))
    data = i2c.readfrom(0x68, 14)
    acc_y = (data[0] << 8) | data[1]
    acc_x = (data[2] << 8) | data[3]
    acc_z = (data[4] << 8) | data[5]
    temperature = (data[6] << 8) | data[7]
    gyro_y = (data[8] << 8) | data[9]
    gyro_x = (data[10] << 8) | data[11]
    gyro_z = (data[12] << 8) | data[13]
    gyro_x -= gyro_x_cal
    gyro_y -= gyro_y_cal
    gyro_z -= gyro_z_cal
    acceleration_x = gyro_x * (-0.0610687023)
    acceleration_y = gyro_y * (-0.0610687023)
    acceleration_z = gyro_z * (-0.0610687023)
    angle_pitch += acceleration_x * elapsedTime
    angle_roll += acceleration_y * elapsedTime
    angle_yaw += acceleration_z * elapsedTime
    if angle_yaw >= 180.00:
        angle_yaw -= 360
    elif angle_yaw < -180.00:
        angle_yaw += 360
    angle_roll_acc = math.atan(acc_x / math.sqrt(acc_y * acc_y + acc_z * acc_z)) * (-57.296)
    angle_pitch_acc = math.atan(acc_y / math.sqrt(acc_x * acc_x + acc_z * acc_z)) * 57.296
    angle_pitch_acc -= 4
    angle_roll_acc += 9
    if set_gyro_angles:
        angle_pitch = angle_pitch * 0.9996 + angle_pitch_acc * 0.0004
        angle_roll = angle_roll * 0.9996 + angle_roll_acc * 0.0004
    else:
        angle_pitch = angle_pitch_acc
        angle_roll = angle_roll_acc
        set_gyro_angles = True
    angle_pitch_output = angle_pitch_output * 0.9 + angle_pitch * 0.1
    angle_roll_output = angle_roll_output * 0.9 + angle_roll * 0.1
    angle_yaw_output = angle_yaw_output * 0.9 + angle_yaw * 0.1
    if wall_car_init == False:
        roll_desired_angle = 3 * (input_ROLL - 50) / 10.0
        pitch_desired_angle = 3 * (input_PITCH - 50) / 10.0
    P_factor = 0.001286376 * input_THROTTLE + 0.616932
    roll_error = angle_roll_output - roll_desired_angle
    pitch_error = angle_pitch_output - pitch_desired_angle
    yaw_error = angle_yaw_output
    roll_pid_p = P_factor * twoX_kp * roll_error
    pitch_pid_p = P_factor * twoX_kp * pitch_error
    yaw_pid_p = yaw_kp * yaw_error
    roll_pid_i += twoX_ki * roll_error
    pitch_pid_i += twoX_ki * pitch_error
    yaw_pid_i += yaw_ki * yaw_error
    roll_pid_d = twoX_kd * acceleration_y
    pitch_pid_d = twoX_kd * acceleration_x
    yaw_pid_d = yaw_kd * acceleration_z
    if roll_pid_i > 0 and roll_error < 0:
        roll_pid_i = 0
    elif roll_pid_i < 0 and roll_error > 0:
        roll_pid_i = 0
    if pitch_pid_i > 0 and pitch_error < 0:
        pitch_pid_i = 0
    elif pitch_pid_i < 0 and pitch_error > 0:
        pitch_pid_i = 0
    if yaw_pid_i > 0 and yaw_error < 0:
        yaw_pid_i = 0
    elif yaw_pid_i < 0 and yaw_error > 0:
        yaw_pid_i = 0
    roll_PID = roll_pid_p + roll_pid_i + roll_pid_d
    pitch_PID = pitch_pid_p + pitch_pid_i + pitch_pid_d
    yaw_PID = yaw_pid_p + yaw_pid_i + yaw_pid_d
    ESCout_1 = input_THROTTLE + pitch_PID - roll_PID + yaw_PID
    ESCout_2 = input_THROTTLE + pitch_PID + roll_PID - yaw_PID
    ESCout_3 = input_THROTTLE - pitch_PID + roll_PID + yaw_PID
    ESCout_4 = input_THROTTLE - pitch_PID - roll_PID - yaw_PID
    if Mode == 1 and (abs(input_ROLL - 50) > 30 or abs(input_PITCH - 50) > 30):
        wall_car_init = True
        if input_ROLL > 30:
            target_axis = 1
            target_dirr = 1
        elif input_ROLL < -30:
            target_axis = 1
            target_dirr = -1
        elif input_PITCH > 30:
            target_axis = 2
            target_dirr = 1
        elif input_PITCH < -30:
            target_axis = 2
            target_dirr = -1
    elif Mode == 0:
        wall_car_init = False
        set_motor_const_speed = False
    if wall_car_init == True:
        if target_axis == 1:
            roll_desired_angle = 90 * target_dirr
        elif target_axis == 2:
            pitch_desired_angle = 90 * target_dirr
        if (abs(acceleration_x) < 15 and abs(acceleration_y) < 15) and (abs(angle_roll_output) > 45 or abs(angle_pitch_output) > 45):
            set_motor_const_speed = True
        if set_motor_const_speed == True:
            ESCout_1 = 1100
            ESCout_2 = 1103
            ESCout_3 = 1106
            ESCout_4 = 1109
            if input_ROLL > 50 and wheal_state == True:
                machine.Pin("D0", machine.Pin.OUT).value(1)
    if ESCout_1 > 1199:
        ESCout_1 = 1199
    elif ESCout_1 < 1:
        ESCout_1 = 1
    if ESCout_2 > 1199:
        ESCout_2 = 1199
    elif ESCout_2 < 1:
        ESCout_2 = 1
    if ESCout_3 > 1199:
        ESCout_3 = 1199
    elif ESCout_3 < 1:
        ESCout_3 = 1
    if ESCout_4 > 1199:
        ESCout_4 = 1199
    elif ESCout_4 < 1:
        ESCout_4 = 1
    arr[0] = ESCout_1
    arr[1] = ESCout_2
    arr[2] = ESCout_3
    arr[3] = ESCout_4
    temp_arr[0] = arr[0]
    temp_arr[1] = arr[1]
    temp_arr[2] = arr[2]
    temp_arr[3] = arr[3]
    for i in range(3):
        temp_i = i
        for j in range(i + 1, 4):
            if temp_arr[j] < temp_arr[temp_i]:
                temp_i = j
        temp = temp_arr[temp_i]
        temp_arr[temp_i] = temp_arr[i]
        temp_arr[i] = temp
    pulldown_time[0] = temp_arr[0]
    pulldown_time[1] = temp_arr[1] - temp_arr[0]
    pulldown_time[2] = temp_arr[2] - temp_arr[1]
    pulldown_time[3] = temp_arr[3] - temp_arr[2]
    pulldown_time[4] = 1200 - temp_arr[3]
    if pulldown_time[1] == 0:
        pulldown_time[1] = 1
    if pulldown_time[2] == 0:
        pulldown_time[2] = 1
    if pulldown_time[3] == 0:
        pulldown_time[3] = 1
    if pulldown_time[4] == 0:
        pulldown_time[4] = 1
    pulldown_time_temp_loop[0] = pulldown_time[0]
    pulldown_time_temp_loop[1] = pulldown_time[1]
    pulldown_time_temp_loop[2] = pulldown_time[2]
    pulldown_time_temp_loop[3] = pulldown_time[3]
    pulldown_time_temp_loop[4] = pulldown_time[4]
    orderState1 = False
    orderState2 = False
    orderState3 = False
    orderState4 = False
    for k in range(4):
        if temp_arr[0] == arr[k] and orderState1 == False:
            order[0] = k
            orderState1 = True
        elif temp_arr[1] == arr[k] and orderState2 == False:
            order[1] = k
            orderState2 = True
        elif temp_arr[2] == arr[k] and orderState3 == False:
            order[2] = k
            orderState3 = True
        elif temp_arr[3] == arr[k] and orderState4 == False:
            order[3] = k
            orderState4 = True
    packetSize = UDP.recv_into(packet, 4)
    if packetSize > 0:
        input_ROLL = int(packet[0])
        input_PITCH = int(packet[1])
        input_THROTTLE = int(packet[2]) * 24
        Mode = int(packet[3])
    if input_THROTTLE == 0:
        angle_yaw_output = 0
        angle_yaw = 0
        yaw_PID = 0
        yaw_pid_p = 0
        yaw_pid_i = 0
        yaw_pid_d = 0
        twoX_ki = 0
    if wheal_state == False:
        machine.Pin("D0", machine.Pin.OUT).value(0)
    if Timer_Init == False:
        timer.init(period=80, mode=machine.Timer.PERIODIC, callback=PWM_callback)
        Timer_Init = True
    wheal_state = not wheal_state
    while time.ticks_diff(Time, timePrev) < 1200:
        pass

setup()


