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

        self.vel_pub = self.create_publisher(
            Twist, "/cmd_vel", 10
        )
        self.follower = self.create_publisher(
            Bool, "/found_following_state", 10
        )

        self.target_index = None # Where was the closest target in the last scan

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

        if self.target_index is None:
            min_index = min(range(len(ranges)), key=ranges.__getitem__)
            self.target_index = min_index

        search_range = 10  # Area to search for target

        min_index = self.target_index
        closest_distance = ranges[self.target_index]

        for offset in range(-search_range, search_range + 1):
            index = (self.target_index + offset) % len(ranges)
            if ranges[index] < closest_distance:
                closest_distance = ranges[index]
                min_index = index

        self.target_index = min_index  # Update the target index for the next scan

        # min_index = min(range(len(ranges)), key=ranges.__getitem__)
        print(f"The closest object is {closest_distance} m away")

        if closest_distance < 2:
            print(f"Found a target / following target")
            self.found_following_target.data = True
        else:
            self.found_following_target.data = False
            self.target_index = None  # Reset target index if no target is found

        if self.target_index is not None:
            min_index = self.target_index

            if min_index < abs(min_index - 360):
                min_index = min_index
            else:
                min_index = min_index - 360

            print(f"angle direction is: {min_index}")

            if self.state == 3:
                msg.angular.z = ((min_index * (pi / 180)) / 10) / self.time_per_turn
                msg.linear.x = 0.1

                if closest_distance < 0.8:
                    msg.linear.x = 0.2
                else:
                    msg.linear.x = 0.0

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

        print(f"I'm following a target: {self.found_following_target.data}")
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
