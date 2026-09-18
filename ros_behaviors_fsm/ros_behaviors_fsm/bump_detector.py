"""
Bump Detector
    This node encorporates a simple bump node where if the neato is
    bumped, the signal is activated and then the neato will drive
    backwards for 5 seconds, before driving forwards again.
    The coordinator file allows the robot to turn 90* before continuing.
"""

import numpy as np
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from neato2_interfaces.msg import Bump
from std_msgs.msg import Int8, Bool
from time import sleep
from rclpy.duration import Duration


class BumpDetectNode(Node):
    """A class that implements a node to to stop a robot and redirect when bumped."""

    def __init__(self):
        super().__init__("bump_detect_node")
        self.time_per_turn = 0.1
        self.timer = self.create_timer(self.time_per_turn, self.run_loop)
        # subscriber to get bump message
        self.bump_sub = self.create_subscription(Bump, "/bump", self.bump_callback, 10)

        # subscriber to fsm state
        self.state_sub = self.create_subscription(Int8, "/fsm_state", self.run_loop, 10)

        # publisher to bumped reversing flag as feedback for fsm state
        self.bump_pub = self.create_publisher(Bool, "/bumped_reversing", 10)

        # publisher to wheel velocity
        self.vel_pub = self.create_publisher(
            Twist, "/cmd_vel", 10
        )  # /cmd_vel is velocity

        self.backup_time = Duration(
            seconds=5.0
        )  # length of backup (approximately half meter)
        self.bumped = False
        self.current_pose = None
        self.backing_up = False
        self.start_time = None
        self.backup_start_time = None

    def run_loop(self, state: Int8):
        """Handles the execution of the neato driving forward, or stopping.

        Args:

            Linear (_type_) = the linear velocity in m/s
            angular (_type_) = the angular velocity in rad/s
            time (_type_) = the time it is backing up

        """

        # if fsm is in bump detector state
        if state == 2:
            msg = Twist()

            # redirect after bump
            if self.bumped and not self.backing_up:
                self.backing_up = True
                self.backup_start_time = self.get_clock().now()

            if self.backing_up:
                # time dependent backup
                if (self.get_clock().now() - self.backup_start_time) < self.backup_time:
                    msg.linear.x = -0.1  # m/s backup
                    msg.angular.z = 0.0  # no turn, implemented in coordinator
                else:  # back to forward
                    self.backing_up = False
                    self.bumped = False
                    msg.linear.x = 0.1
                    msg.angular.z = 0.0
            else:  # drive forward
                self.bump_pub.publish(
                    False
                )  # will toggle bump state off once bump behavior is done

            self.vel_pub.publish(msg)

    def bump_callback(self, msg: Bump):
        """Handles bump input data.

        Args:
            msg (Bump): message that takes value true if robot bumped.
        """
        # if bumped then change self.bumped to True
        if (
            self.backing_up == False
        ):  ## ensures that fsm doesn't change while backing up
            if (
                msg.left_front == 1
                or msg.left_side == 1
                or msg.right_side == 1
                or msg.right_front == 1
            ):
                # will publish true if the bump detector hits
                self.bumped = True
                self.bump_pub.publish(self.bumped)
                print("bumped!")
            else:
                self.bumped = False


def main(args=None):
    rclpy.init(args=args)
    node = BumpDetectNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
