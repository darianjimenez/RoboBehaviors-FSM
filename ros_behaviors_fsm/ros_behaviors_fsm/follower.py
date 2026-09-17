import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

class PeopleFollowNode(Node):
    def __init__(self):
        super().__init__("people_follow_node")
        self.scan_sub = self.create_subscription(LaserScan, "/scan", self.scan_callback, 10)
        self.vel_pub = self.create_publisher(Twist, "/cmd_vel", 10)

    def scan_callback(self, scan):
        msg = Twist()

        ranges = scan.ranges

        # Check front, left, and right
        front = ranges[0]
        left = ranges[30]
        right = ranges[-30]

        # Turn toward the closest side
        if left < front and left < right:
            msg.angular.z = 0.3
        elif right < front and right < left:
            msg.angular.z = -0.3
        else:
            msg.angular.z = 0.0

        if front > 0.8:
            msg.linear.x = 0.1
        else:
            msg.linear.x = 0.0

        self.vel_pub.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = PeopleFollowNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()