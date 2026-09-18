import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Int8, Bool
from geometry_msgs.msg import Twist


class PeopleFollowNode(Node):
    def __init__(self):
        super().__init__("people_follow_node")

        self.found_following_target = Bool()
        self.state = 0
        self.scan_sub = self.create_subscription(
            LaserScan, "/scan", self.scan_callback, 10
        )
        self.state_sub = self.create_subscription(
            Int8, "/fsm_state", self.state_tracker, 10
        )
        self.vel_pub = self.create_publisher(Twist, "/cmd_vel", 10)
        self.follower = self.create_publisher(Bool, "/found_following_target_", 10)

    def state_tracker(self, state: Int8):
        self.state = state.data

    # current issue --> need to subscribe to multiple states in one node
    def scan_callback(self, scan):
        msg = Twist()

        ranges = scan.ranges

        # Check front, left, and right
        front = ranges[0]
        left = ranges[30]
        right = ranges[-30]

        # checks if
        if any(front, left, right != 0):
            self.found_following_target.data = True
        else:
            self.found_following_target.data = False

        if self.state == 3:
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

        self.follower.publish(self.found_following_target)
        self.vel_pub.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = PeopleFollowNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
