import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Int8, Bool
from geometry_msgs.msg import Twist
from math import pi


class PeopleFollowNode(Node):
    def __init__(self):
        super().__init__("people_follow_node")

        self.time_per_turn = 0.1
        self.timer = self.create_timer(self.time_per_turn, self.run_loop)
        self.found_following_target = Bool()
        self.state = 0
        self.scan_ranges = LaserScan()
        self.scan_sub = self.create_subscription(
            LaserScan, "/scan", self.scan_tracker, 10
        )
        self.state_sub = self.create_subscription(
            Int8, "/fsm_state", self.state_tracker, 10
        )
        self.vel_pub = self.create_publisher(Twist, "/cmd_vel", 10)
        self.follower = self.create_publisher(Bool, "/found_following_state", 10)

    def scan_tracker(self, scan):
        self.scan_ranges = scan

    def state_tracker(self, state: Int8):
        self.state = state.data

    # current issue --> need to subscribe to multiple states in one node
    def run_loop(self):
        msg = Twist()

        ranges = self.scan_ranges.ranges

        if not ranges:
            return
        # Check front, left, and right
        # print(f"The ranges are {ranges}")

        min_index = min(range(len(ranges)), key=ranges.__getitem__)
        print(f"The closest object is {ranges[min_index]} m away")

        if ranges[min_index] < 1:
            print(f"Found a target / following target")
            self.found_following_target.data = True
        else:
            self.found_following_target.data = False

        if min_index < abs(min_index - 360):
            min_index = min_index
        else:
            min_index = min_index - 360

        print(f"angle direction is: {min_index}")
        if self.state == 3:
            msg.angular.z = ((min_index * (pi / 180)) / 10) / self.time_per_turn
            msg.linear.x = 0.1
        # front = ranges[0]
        # left = ranges[30]
        # right = ranges[-30]

        # min(ranges)

        # self.get_logger().info(f"The left data is {left}")
        # print(f"The left data is {left}")

        # # checks if
        # if front < 2 or left < 2 or right < 2:
        #     self.found_following_target.data = True
        # else:
        #     self.found_following_target.data = False

        # if self.state == 3:
        #     # Turn toward the closest side
        #     if left < front and left < right:
        #         msg.angular.z = 0.3
        #     elif right < front and right < left:
        #         msg.angular.z = -0.3
        #     else:
        #         msg.angular.z = 0.0

        #     if front > 0.8:
        #         msg.linear.x = 0.1
        #     else:
        #         msg.linear.x = 0.0

        print(f"I'm following a target: {self.found_following_target}")
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
