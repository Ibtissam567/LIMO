import launch
import launch.actions
import launch.substitutions
import launch_ros.actions
from launch import LaunchDescription
from launch_ros.actions import Node
import subprocess
import rclpy
from rclpy.node import Node
from pylimo import limo
#from tutorial_interfaces.msg import Num
import time
limo=limo.LIMO()
limo.EnableCommand()
from std_msgs.msg import String
from interfaces.msg import *
from geometry_msgs.msg import Twist

def generate_launch_description():
    # return launch.LaunchDescription([
    #     launch.actions.DeclareLaunchArgument(
    #         'node_prefix',
    #         default_value=[launch.substitutions.EnvironmentVariable('USER'), '_'],
    #         description='Prefix for node names'),
    #     launch_ros.actions.Node(
    #         package='demo_nodes_cpp', node_executable='talker', output='screen',
    #         node_name=[launch.substitutions.LaunchConfiguration('node_prefix'), 'talker']),
    # ])
    # commande1 = "cd ~/control_ws && source install/setup.bash && ros2 run teleop_twist_keyboard teleop_twist_keyboard '"
    # subprocess.run(["python", "/home/agilex/control_ws/src/teleop_twist_keyboard/teleop_twist_keyboard.py"])
    # subprocess.run(['gnome-terminal', '--', 'bash', '-c', commande1], check=True)
    return LaunchDescription([
    # subprocess.run(['gnome-terminal', '--', 'bash', '-c', commande1], check=True)
        Node(
            package='sensors_nodes',
            node_namespace='teleop_keyboard',
            node_executable='imu_node',
            node_name='imu_node'
        ),
        Node(
            package='teleop_twist_keyboard',
            node_namespace='teleop_keyboard',
            node_executable='teleop_twist_keyboard',
            node_name='teleop_twist_keyboard'
        ),
        Node(
            package='controller',
            node_namespace='teleop_keyboard',
            node_executable='controlnode',
            node_name='controlnode'
        ),

        Node(
            package='calcul_position',
            node_namespace='teleop_keyboard',
            node_executable='odom_node',
            node_name='odom_node'
        ),


     ])