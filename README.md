# RoboBehaviors-FSM


## Quickstart Guide

Below, we have included a quickstart guide to get started with setup to run these nodes.
### 1. Download our Repo
```bash
cd ~/ros2_ws/src
git clone https://github.com/darianjimenez/RoboBehaviors-FSM.git
```

### 2. Build our Repo
```bash
cd ~/ros2_ws
colcon build --symlink-install
source install/setup.bash
```
Note: make sure to run `source ~/ros2_ws/install/setup.bash` in every new terminal.

### 3. Launch Neato in Simulation
**Or the Gazebo simulator:**
```bash
ros2 launch neato2_gazebo neato_gauntlet_world.py
```
Note: to test our FSM in simulation, we recommend launching the simulator and removing all objects in the Gazebo simulation (except one or two objects) from the simulated world. 

### 4. Run the behaviors
Or run each node in its own terminal:
```bash
ros2 run ros_behaviors_fsm drive_arch      
ros2 run ros_behaviors_fsm people_follow   
ros2 run ros_behaviors_fsm bump_detector   
ros2 run ros_behaviors_fsm fsm             
```
Here, we also recommend running the non-FSM behaviors first and then running the FSM node. 

### 5. Play back the bag files
Each recorded bag is in its own folder under `bags/`:
```bash
cd ~/ros2_ws/src/RoboBehaviors-FSM/bags
ros2 bag play fsm_controller/fsm_controller.bag 
ros2 bag play people_follow/people_follow.bag
ros2 bag play bump_detector/bump_detector.bag
```
Always make sure to run the corresponding ROS node before running the ROS bag. 
