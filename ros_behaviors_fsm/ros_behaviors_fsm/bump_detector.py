import numpy as np
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import Header
from nav_msgs.msg import Odometry
from neato2_interfaces.msg import Bump
from math import pi


class BumpDetectNode(Node):
    def __init__(self):
        super().__init__("bump_detect_node")

        # #speed
        # self.speed = 0.1 #m/s
        # self.turn = 0.4 #rad/s

        # #default
        # self.cmd = Twist()
        # self.cmd.linear.x = self.speed
        # self.cmd.angular.z = 0.0
        self.time_per_turn = 0.1
        self.timer = self.create_timer(self.time_per_turn, self.run_loop)
        # subscriber to get bump message
        self.bump_sub = self.create_subscription(Bump, "/bump", self.bump_callback, 10)
        # subscriber to odom message
        # self.odom_sub = self.create_subscription(Odometry, "/odom", self.odom_callback, 10)

        # publisher to wheel velocity
        self.vel_pub = self.create_publisher(
            Twist, "/cmd_vel", 10
        )  # /cmd_vel is velocity

        self.bumped = False
        self.current_pose = None

    def run_loop(self):
        # message received from Bump
        # twist for linear and angular velocity
        cmd = Twist()

        if not self.bumped:
            cmd.linear.x = 0.1  # m/s
            cmd.angular.z = 0.0
            self.vel_pub.publish(cmd)

        else:
            # stop the neato
            cmd.linear.x = 0.0
            cmd.angular.z = 0.0
            self.vel_pub.publish(cmd)
            # want 5 sec of -0.1 m/s for it to back up 0.5m to then

            # #Move backwards 0.5m (5 seconds)
            # rclpy.spin_once(self, timeout_sec=0.05) #times out

            # set self.bumped = False

    def bump_callback(self, msg: Bump):
        # if eys then change self.bumped to True

        if (
            msg.left_front == 1
            or msg.left_side == 1
            or msg.right_side == 1
            or msg.right_front == 1
        ):
            self.bumped = True
        else:
            self.bumped = False

    # def odom_callback(self, msg):
    #     #want the position
    #     self.current_pose = msg.pose.pose


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
