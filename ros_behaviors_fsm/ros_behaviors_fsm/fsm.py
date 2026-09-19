import numpy as np
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import Int8, Int32, Bool
from math import pi
from enum import Enum


class STATE(Enum):
    DRIVE_ARCH = 1
    BUMP_DETECTED = 2
    FOLLOW_PERSON = 3


class FSMNode(Node):
    def __init__(self):
        super().__init__("fsm")
        self.state = Int8()
        self.state.data = 1
        self.time_per_turn = 0.1
        self.found_following_state = Bool()
        self.bumped_reversing_state = Bool()
        self.create_timer(self.time_per_turn, self.run_loop)
        self.fsm_state_pub = self.create_publisher(Int8, "/fsm_state", 10)
        self.create_subscription(Bool, "/found_following_state", self.follower_sub, 10)
        self.create_subscription(Bool, "/bumped_reversing", self.bumped_sub, 10)

    # subscription created for follower
    def follower_sub(self, msg: Bool):
        self.found_following_state = msg

    # subscription created for bumped msg
    def bumped_sub(self, msg: Bool):
        self.bumped_reversing_state = msg

    def run_loop(self):

        # state selector logic
        if (
            self.bumped_reversing_state.data == True
            and self.found_following_state.data == True
        ):
            print("Choice 1")
            self.state.data = 2
        elif self.found_following_state.data == True:
            self.state.data = 3
            print("Choice 2")
        elif self.bumped_reversing_state.data == True:
            self.state.data = 2
            print("Choice 3")
        else:
            self.state.data = 1
            print("Choice 4")

        self.fsm_state_pub.publish(self.state)
        print(f"The current state is: {self.state.data}")


def main(args=None):
    rclpy.init(args=args)
    node = FSMNode()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()
