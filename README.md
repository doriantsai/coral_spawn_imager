# Coral Spawn Imager

As part of the Reef Restoration and Adaptation Program (RRAP), the Coral Spawn and Larvae Imaging Camera System (CSLICS) is a camera system aimed at capturing images of coral spawn for research and analysis. This coral_spawn_imager repo is specifically the code for camera control, image capture and scheduling.


## Hardware

- Raspberry Pi Model 4B (<2 GB)
- Raspberry Pi High Quality Camera
- Microscope lens (TODO: get specifications)

## Installation Requirements

- Raspberry Pi OS version 10 (Buster)
- Enable legacy camera stack
- Python 3.7.3
- pip3 install picamera (v1.13)
- cv-bridge (1.16.2)
- numpy (1.21.6)
- Pillow (9.2.0)

## Installation Instructions

- Use raspberry Pi Imager for Raspbian OS Buster (legacy), because this has documented ROS Noetic support, while Bullseye does not. Consider migrating to Ubuntu 20.04 with picamera2, which is soon to be supported.
- `sudo raspi-config` to enable ssh and legacy camera stack
- Increase swap RAM to 1GB for faster compiles:

      sudo dphys-swapfile swapoff
	    sudo vim /etc/dphys-swapfile
      
- Change 100 MB to 1024 MB

      sudo dphys-swapfile setup
      sudo dphys-swapfile swapon
      
- Install ROS Noetic directly (from Github Repos) because a number of ROS packages like RVIZ are not available for Debian Buster, and fail to compile from source. Most relevant packages do however still compile. We roughly follow the instructions from this tutorial (https://varhowto.com/install-ros-noetic-raspberry-pi-4/)  with the addition of relevant ROS image packages.

      sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu buster main" > /etc/apt/sources.list.d/ros-noetic.list' 
      sudo apt-key adv --keyserver 'hkp://keyserver.ubuntu.com:80' --recv-key C1CF6E31E6BADE8868B172B4F42ED6FBAB17C654
      sudo apt update
      sudo apt-get install -y python3-rosdep python3-rosinstall-generator python3-wstool python3-rosinstall build-essential cmake
      sudo rosdep init && rosdep update
      mkdir ~/ros_catkin_ws && cd ~/ros_catkin_ws
      rosinstall_generator ros_comm common_msgs image_common image_pipeline vision_opencv vision_msgs --rosdistro noetic --deps --wet-only --tar > noetic-ros_comm-vision-wet.rosinstall
      wstool init src noetic-ros_comm-vision-wet.rosinstall
      rosdep install -y --from-paths src --ignore-src --rosdistro noetic -r --os=debian:buster
      
- Compile ROS Noetic (this step can take several hours):

      sudo src/catkin/bin/catkin_make_isolated --install -DCMAKE_BUILD_TYPE=Release --install-space /opt/ros/noetic -j1 -DPYTHON_EXECUTABLE=/usr/bin/python3
      
- Create a ROS workspace:

      mkdir ~/cslics_ws/src
      cd ~/cslics_ws/src
 
- Clone this repo in the src directory. Note: might have to use the HTTPS if you don't have SSH access to the repo.

      git clone git@github.com:doriantsai/coral_spawn_imager.git

- Compile the catkin workspace

      cd ~/cslics_ws
      catkin_make

- Source the workspace and packages within

      source ~/cslics_ws/devel/setup.bash

- coral_spawn_imager should be operational. Whenver changes to the packages are made, you need to recompile with catkin_make and source. 

## Usage Instructions

Running the camera publisher:

      rosrun coral_spawn_imager camera_publisher.py

Running the camera subscriber:

      rosrun coral_spawn_imager camera_subscriber.py

## ROS Multple Computer Setup

- We refer to http://wiki.ros.org/ROS/NetworkSetup for the ROS network setup
- In each computer, use `ifconfig` to get the ip addresses. Let's say we got 192.168.1.100 for the main `cslics` computer and 192.168.1.200 for `pi` imaging device. On both computers, set the hostnames:

      sudo vim /etc/hosts

  And set `cslics 192.168.1.100` and on the next line, `pi 192.168.1.200`.

- Ensure each computer can ping each other
- On the main cslics computer: (note: unsure why ROS_IP has to be a valid IPv4/v6 address, can't it just use the alias from /etc/hosts? I got errors otherwise)

      export ROS_IP=192.168.1.100
      export ROS_MASTER_URI=http://cslics:11311/
      roscore

- On the imaging device:

      export ROS_IP=192.168.1.200
      export ROS_MASTER_URI=http://cslics:11311/

- Then we should be able to run the publisher on the `pi`, and see the topics and read the values of the topics on the `cslics` computer
