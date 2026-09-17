# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       adamp                                                        #
# 	Created:      14/05/2026, 15:03:53                                         #
# 	Description:  V5 project                                                   #
#                                                                              #
# ---------------------------------------------------------------------------- #

# Library imports
from vex import *

brain = Brain()
controller = Controller()

# The two motors on each side are mechanically linked by the chain.
right_front = Motor(Ports.PORT1)
left_front = Motor(Ports.PORT2)
left_rear = Motor(Ports.PORT3)
right_rear = Motor(Ports.PORT4)

lift_motor = Motor(Ports.PORT20)
claw_roll_motor = Motor(Ports.PORT11)
claw_pitch_motor = Motor(Ports.PORT12)

claw_solenoid = DigitalOut(brain.three_wire_port.a)


def drive_code():
    forward_speed = controller.axis3.position()
    turn_speed = controller.axis4.position()

    left_speed = forward_speed + turn_speed
    right_speed = forward_speed - turn_speed

    maximum_speed = max(abs(left_speed), abs(right_speed), 100)
    left_speed = left_speed / maximum_speed * 100
    right_speed = right_speed / maximum_speed * 100

    if abs(left_speed) <= 5:
        left_speed = 0
    if abs(right_speed) <= 5:
        right_speed = 0

    if lift_motor.position(DEGREES) > 500:
        crawl_multiplier = 0.10
    elif controller.buttonB.pressing():
        crawl_multiplier = 0.25
    else:
        crawl_multiplier = 1.0

    left_speed *= crawl_multiplier
    right_speed *= crawl_multiplier

    if left_speed == 0:
        left_front.stop(BRAKE)
        left_rear.stop(BRAKE)
    else:
        left_front.spin(FORWARD, left_speed, PERCENT)
        left_rear.spin(FORWARD, left_speed, PERCENT)

    if right_speed == 0:
        right_front.stop(BRAKE)
        right_rear.stop(BRAKE)
    else:
        right_front.spin(REVERSE, right_speed, PERCENT)
        right_rear.spin(REVERSE, right_speed, PERCENT)




# This function is used during the autonomous period.
# The lift and drivetrain can be programmed here later.
def autonomous():
    brain.screen.clear_screen()
    brain.screen.print("autonomous code")
    # place automonous code here



# This function is used while the driver controls the robot.
def user_control():
    
    brain.screen.clear_screen()
    brain.screen.print("driver control")

    claw_roll_position = 0
    claw_roll_speed = 180

    pitch_joystick_active = True
    drive_train_controls_active = True
    

    brain.timer.reset()
    last_update_time = brain.timer.time(SECONDS)
    while True:
        
        this_update_time = brain.timer.time(SECONDS)
        delta_time = this_update_time - last_update_time
        last_update_time = this_update_time

        drive_code()

        if controller.buttonL1.pressing():
            drive_train_controls_active = True
            lift_motor.spin(FORWARD, 85, PERCENT)
        elif controller.buttonR1.pressing():
            drive_train_controls_active = True
            lift_motor.spin(REVERSE, 85, PERCENT)
        else:
            if drive_train_controls_active:
                lift_motor.stop(HOLD)

        claw_pitch_speed = controller.axis2.position()
        print(lift_motor.position(DEGREES))
        if abs(claw_pitch_speed) <= 20:
            # Inside deadzone, stop motor
            claw_pitch_speed = 0
        else:
            # Outside deadzone. Enable joystick
            pitch_joystick_active = True

        if pitch_joystick_active:
            # Joystick is enabled, set motor speed based on joystick position
            if claw_pitch_speed == 0:
                claw_pitch_motor.stop(HOLD)
            else:
                claw_pitch_motor.spin(FORWARD, claw_pitch_speed / 5, PERCENT)
        #print(claw_pitch_motor.position(DEGREES))
        



        claw_roll_position += (controller.axis1.position() / 100) * delta_time * claw_roll_speed
#Claw Turn Limitations
        if claw_roll_position > 180:
            claw_roll_position = 180
        if claw_roll_position < -180:
            claw_roll_position = -180

        #Extra Buttons For the claw
        claw_pitch_position = claw_pitch_motor.position(DEGREES)

        if controller.buttonX.pressing():
            claw_roll_position = 0
        if controller.buttonLeft.pressing():
            claw_roll_position = -90
        if controller.buttonRight.pressing():
            claw_roll_position = 90

        if controller.buttonUp.pressing():
            # Disable joystick until outside of deadzone
            pitch_joystick_active = False
            drive_train_controls_active = False
            lift_motor.set_velocity(100, PERCENT)
            lift_motor.spin_to_position(40, DEGREES, wait=False)
            claw_pitch_motor.spin_to_position(360, DEGREES, wait=False)
         

        if controller.buttonDown.pressing():
            # Disable joystick until outside of deadzone
            pitch_joystick_active = False
            drive_train_controls_active = False
            lift_motor.set_velocity(75, PERCENT)
            lift_motor.spin_to_position(534, DEGREES, wait=False)
            claw_pitch_motor.spin_to_position(720, DEGREES, wait=False)

            
    
        
            


        claw_roll_motor.set_velocity(claw_roll_speed, VelocityUnits.DPS)
        claw_roll_motor.spin_to_position(claw_roll_position, DEGREES, wait=False)


        if controller.buttonL2.pressing():
            claw_solenoid.set(False)

        if controller.buttonR2.pressing():
            claw_solenoid.set(True)
            
    

        wait(100, MSEC)

    
    
        
    

    # Create the VEX competition instance so the system can call the correct mode.
comp = Competition(user_control, autonomous)

    # Clear the screen when the program starts.
brain.screen.clear_screen()
