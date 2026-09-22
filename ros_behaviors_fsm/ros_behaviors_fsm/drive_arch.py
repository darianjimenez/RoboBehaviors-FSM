"""
Drive Arch
    This node moves the neato forward while turning.
"""

import numpy as np
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import Int8
from math import pi


class DriveArchNode(Node):
    """Drive in an arc while FSM is in state 1."""
    def __init__(self):
        """Set up subscribers, publishers, timers, and variables"""
        super().__init__("drive_arch_node")
        self.state = Int8() # Store current state
        self.time_per_turn = 0.1 # Run every .1 seconds
        self.timer = self.create_timer(self.time_per_turn, self.run_loop)
        self.linear_distance = 0.05 # Distance travelled each loop
        self.angular = pi / 30 # Amount turned each loop

        # Publish movement commands
        self.vel_pub = self.create_publisher(
            Twist, "/cmd_vel", 10
        )

        # Listen to the current FSM state
        self.state_sub = self.create_subscription(
            Int8, "/fsm_state", self.state_tracker, 10
        )

    def state_tracker(self, state: Int8):
        """Save current FSM state."""
        self.state = state

    def run_loop(self):
        """Drive robot in arc when in state 1"""
        if self.state.data == 1:
            msg = Twist()

            # Set forward velocity
            msg.linear.x = self.linear_distance / self.time_per_turn

            # Set turning velocity
            msg.angular.z = self.angular / self.time_per_turn
            self.vel_pub.publish(msg) 


def main(args=None):
    """Start the drive arch node."""
    rclpy.init(args=args)
    node = DriveArchNode()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()
