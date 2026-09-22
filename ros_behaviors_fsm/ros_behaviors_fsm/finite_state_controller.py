"""
Finite State Machine

State 1: Drive Arch
State 2: Bump Deteceted
State 3: Follow Person
"""

import numpy as np
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import Int8, Int32, Bool
from math import pi
from enum import Enum


class STATE(Enum):
    """Names and numbers for each FSM state"""
    DRIVE_ARCH = 1 
    BUMP_DETECTED = 2
    FOLLOW_PERSON = 3


class FSMNode(Node):
    """Chooses which behavior should currently run"""
    def __init__(self):
        super().__init__("fsm")
        self.state = Int8() # Store current state
        self.state.data = 1 # Start in drive arch state
        self.time_per_turn = 0.1 # Run every .1 seconds
        self.found_following_state = Bool() # Has follower found target
        self.bumped_reversing_state = Bool() # Is bump behavior active
        self.create_timer(self.time_per_turn, self.run_loop) # Run state selection contiuously
        # Publish current FSM state
        self.fsm_state_pub = self.create_publisher(
            Int8, "/fsm_state", 10
        )
        # Listen for target detection
        self.create_subscription(
            Bool, "/found_following_state", self.follower_sub, 10
        )
        # Listen for bump detection
        self.create_subscription(
            Bool, "/bumped_reversing", self.bumped_sub, 10
        )

    # subscription created for follower
    def follower_sub(self, msg: Bool):
        """Save whether or not follower has found a target"""
        self.found_following_state = msg

    # subscription created for bumped msg
    def bumped_sub(self, msg: Bool):
        """Save whether the bumb behaviour is active"""
        self.bumped_reversing_state = msg

    def run_loop(self):
        """Choose current FSM state"""
        # State selector logic
        # if bump and follow happen at the same time, choose bump
        if (
            self.bumped_reversing_state.data == True
            and self.found_following_state.data == True
        ):
            print("Choice 1")
            self.state.data = 2
        # if target is found follow it
        elif self.found_following_state.data == True:
            self.state.data = 3
            print("Choice 2")
        # if bump detected, follow the bump
        elif self.bumped_reversing_state.data == True:
            self.state.data = 2
            print("Choice 3")
        # else, drive normally
        else:
            self.state.data = 1
            print("Choice 4")

        # tell all behavior nodes which state is active
        self.fsm_state_pub.publish(self.state)
        print(f"The current state is: {self.state.data}")


def main(args=None):
    """Start FSM Node"""
    rclpy.init(args=args)
    node = FSMNode()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()
