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
# Change these port numbers if the motor plugs are different on the robot.
left_front = Motor(Ports.PORT1)
left_rear = Motor(Ports.PORT2)
right_front = Motor(Ports.PORT9)
right_rear = Motor(Ports.PORT10)

lift_motor = Motor(Ports.PORT20)
claw_roll_motor = Motor(Ports.PORT11)
claw_pitch_motor = Motor(Ports.PORT12)

claw_solenoid = DigitalOut(brain.three_wire_port.a)

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

    brain.timer.reset()
    last_update_time = brain.timer.time(SECONDS)
    while True:
        this_update_time = brain.timer.time(SECONDS)
        delta_time = this_update_time - last_update_time
        last_update_time = this_update_time


        claw_pitch_speed = controller.axis2.position()
        
        if abs(claw_pitch_speed) <= 20:
            claw_pitch_speed = 0

        if claw_pitch_speed == 0:
            claw_pitch_motor.stop(HOLD)
        else:
            claw_pitch_motor.spin(FORWARD, claw_pitch_speed / 5, PERCENT)



        claw_roll_position += (controller.axis1.position() / 100) * delta_time * claw_roll_speed

        if claw_roll_position > 180:
            claw_roll_position = 180
        if claw_roll_position < -180:
            claw_roll_position = -180

        if controller.buttonX.pressing():
            claw_roll_position = 0

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

