"""
People Follower

Uses LiDAR data to locate and follow a target

THe neato chooses the closest object, remembers where it was,
and then searches around that location for future scans.

This node tells the FSM where the target is and controls it
in state 3.
"""

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Int8, Bool
from geometry_msgs.msg import Twist
from math import pi


class PeopleFollowNode(Node):
    """Find and follow target with LiDAR scans"""
    def __init__(self):
        """Set up LiDAR, subscribers, publishers, timers, and variables"""
        super().__init__("people_follow_node")

        self.time_per_turn = 0.1 # Run  every .1 seconds
        self.timer = self.create_timer(self.time_per_turn, self.run_loop)
        self.found_following_target = Bool() # Has target been found
        self.state = 0 # FSM state
        self.scan_ranges = LaserScan() # Store scan

        # Listen to LiDAR data
        self.scan_sub = self.create_subscription(
            LaserScan, "/scan", self.scan_tracker, 10
        )
        # Listen to current FSM state
        self.state_sub = self.create_subscription(
            Int8, "/fsm_state", self.state_tracker, 10
        )
        # Publish movement commands
        self.vel_pub = self.create_publisher(
            Twist, "/cmd_vel", 10
        )
        # Tell FSM if target found
        self.follower = self.create_publisher(
            Bool, "/found_following_state", 10
        )

        self.target_index = None # Where was the closest target in the last scan

    def scan_tracker(self, scan):
        """Save newest LiDAR scan"""
        self.scan_ranges = scan

    def state_tracker(self, state: Int8):
        """Save current FSM state"""
        self.state = state.data

    def run_loop(self):
        """Find and follwo target while in state 3"""
        msg = Twist()

        ranges = self.scan_ranges.ranges # Get LiDAR measurements

        # Do nothing until LiDAR scan recieved 
        if not ranges:
            return

        # Find the closest object 
        if self.target_index is None:
            min_index = min(range(len(ranges)), key=ranges.__getitem__)
            self.target_index = min_index # Save location

        search_range = 10  # Area to search for target

        # Search for item at previous location
        min_index = self.target_index
        closest_distance = ranges[self.target_index]

        # Look near where target last seen
        for offset in range(-search_range, search_range + 1):
            index = (self.target_index + offset) % len(ranges)
            # Update target if closer point found nearby
            if ranges[index] < closest_distance:
                closest_distance = ranges[index]
                min_index = index

        self.target_index = min_index  # Update the target index for the next scan

        print(f"The closest object is {closest_distance} m away")

        if closest_distance < 2: # Target must be within 2m
            print(f"Found a target / following target")
            self.found_following_target.data = True
        else:
            self.found_following_target.data = False
            self.target_index = None  # Reset target index if no target is found

        # Only calculate direction if a target exists
        if self.target_index is not None:
            min_index = self.target_index

            # Convert indices near 360 into negative values 
            # One side of robot is pos, one is neg
            if min_index < abs(min_index - 360):
                min_index = min_index
            else:
                min_index = min_index - 360

            print(f"angle direction is: {min_index}")

            if self.state == 3: # Control robot while FSM is in follow state
                # Turn towards target
                msg.angular.z = ((min_index * (pi / 180)) / 10) / self.time_per_turn
                msg.linear.x = 0.1

                # Change speed based on distance
                if closest_distance < 0.8:
                    msg.linear.x = 0.2
                else:
                    msg.linear.x = 0.0

        print(f"I'm following a target: {self.found_following_target.data}")
        self.follower.publish(self.found_following_target) # Tell FSM if target was found
        self.vel_pub.publish(msg) # Send movement command


def main(args=None):
    """Start the follower node"""
    rclpy.init(args=args)
    node = PeopleFollowNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
