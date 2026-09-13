import numpy as np
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import Header
from math import pi


class DriveArchNode(Node):
    def __init__(self):
        super().__init__("drive_arch_node")
        self.time_per_turn = 1
        self.timer = self.create_timer(self.time_per_turn, self.run_loop)
        self.linear_distance = 0.1
        self.angular = pi / 30
        self.vel_pub = self.create_publisher(Twist, "cmd_vel", 10)

    def run_loop(self):
        msg = Twist()
        msg.linear.x = self.linear_distance / self.time_per_turn
        msg.angular.z = self.angular / self.time_per_turn
        self.vel_pub.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = DriveArchNode()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()
