import os
from pathlib import Path
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.conditions import IfCondition
from launch.conditions import UnlessCondition
from launch.actions import DeclareLaunchArgument
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import ThisLaunchFileDir
from launch.actions import ExecuteProcess
from launch.substitutions import LaunchConfiguration, PythonExpression
from launch_ros.actions import Node


def generate_launch_description():

    laser_topic_name = LaunchConfiguration('laser_topic_name')
    odom_topic_name  = LaunchConfiguration('odom_topic_name')
    
    laser_topic_name_launch_arg = DeclareLaunchArgument('topic_name',default_value ='/scan')
    odom_topic_name_launch_arg  = DeclareLaunchArgument('odom_topic_name',default_value ='/odom_rf2o')

    set_laser_topic_name = ExecuteProcess(cmd = [['ros2 param set',laser_topic_name]],shell=True)
    set_odom_topic_name  = ExecuteProcess(cmd = [['ros2 param set',odom_topic_name]],shell=True)
    
    return LaunchDescription([
        laser_topic_name_launch_arg,
        odom_topic_name_launch_arg,
        set_laser_topic_name,
        set_odom_topic_name,
        Node(
            package='rf2o_laser_odometry',
            executable='rf2o_laser_odometry_node',
            name='rf2o_laser_odometry',
            output='screen',
            parameters=[{
                'laser_scan_topic' : laser_topic_name,
                'odom_topic' : odom_topic_name,
                'publish_tf' : True,
                'base_frame_id' : 'base_link',
                'odom_frame_id' : 'odom',
                'init_pose_from_topic' : '',
                'freq' : 20.0}],
        ),
    ])
