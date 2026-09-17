import numpy as np
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from neato2_interfaces.msg import Bump
from time import sleep
from rclpy.duration import Duration


class BumpDetectNode(Node):
    def __init__(self):
        super().__init__("bump_detect_node")
        self.time_per_turn = 0.1
        self.timer = self.create_timer(self.time_per_turn, self.run_loop)
        # subscriber to get bump message
        self.bump_sub = self.create_subscription(Bump, "/bump", self.bump_callback, 10)

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

    def run_loop(self):
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
            msg.linear.x = 0.1  # m/s
            msg.angular.z = 0.0

        self.vel_pub.publish(msg)

    def bump_callback(self, msg: Bump):
        # if eys then change self.bumped to True

        if (
            msg.left_front == 1
            or msg.left_side == 1
            or msg.right_side == 1
            or msg.right_front == 1
        ):
            self.bumped = True
            print("bumped!")
        else:
            self.bumped = False


# REVISIT BELOW _ IDK HOW TO WRITE MAIN Functions
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
