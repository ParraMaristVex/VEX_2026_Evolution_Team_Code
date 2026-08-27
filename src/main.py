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

# The lift motor is connected to port 20.
lift_motor = Motor(Ports.PORT20)

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

    while True:
        # Update the controls every 20 milliseconds for smooth response.
        wait(20, MSEC)

        # Axis 3 is the vertical movement of the drive joystick.
        # It controls forward and backward movement.
        forward_speed = controller.axis3.position()

        # Axis 4 is the horizontal movement of the same joystick.
        # It controls turning left and right.
        turn_speed = controller.axis4.position()

        # Arcade drive mixes forward movement and turning.
        # During a turn, the two sides receive opposite speeds.
        left_speed = forward_speed + turn_speed
        right_speed = forward_speed - turn_speed

        # Keep the calculated motor values inside the valid -100 to 100 range.
        left_speed = max(-100, min(100, left_speed))
        right_speed = max(-100, min(100, right_speed))

        # # Run both motors on each side at the same speed.
        # run_side(left_front, left_rear, left_speed)
        # run_side(right_front, right_rear, right_speed)

        # Axis 2 controls the lift joystick direction.
        # Moving it up or down changes the lift speed in small increments.
        lift_speed = controller.axis2.position()

        print(lift_speed)

        # The lift stops and brakes automatically when Axis 2 is released.
        lift_motor.spin(FORWARD, lift_speed, PERCENT)

    # Create the VEX competition instance so the system can call the correct mode.
comp = Competition(user_control, autonomous)

    # Clear the screen when the program starts.
brain.screen.clear_screen()

