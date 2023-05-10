import random
from typing import Tuple
from geopy.distance import geodesic as geodesic_distance
import matplotlib.pyplot as plt

import rclpy
from rclpy.node import Node
from rclpy.time import Time
from rclpy.qos import DurabilityPolicy, QoSProfile, ReliabilityPolicy, qos_profile_sensor_data

from sensor_msgs.msg import NavSatFix
from std_msgs.msg import Float64

from plotter.utils import wgs84_to_ecef
from plotter.sql_controller import SQLController



class PlotterNode(Node):
    """
        A simple python node gathering basic data via mavlink and posting to a database
    """
    
    def __init__(self) -> None:
        super().__init__("plotter_node")
        
        self.current_global_pose_subscriber = self.create_subscription(
            NavSatFix,
            '/mavros/global_position/global',
            qos_profile=QoSProfile(depth=10, reliability=ReliabilityPolicy.BEST_EFFORT,
                                   durability=DurabilityPolicy.VOLATILE),
            callback=self.current_global_pose_cb,
        )
        
        self.current_compas_heading_subscriber = self.create_subscription(
            Float64,
            '/mavros/global_position/compass_hdg',
             qos_profile=QoSProfile(depth=10, reliability=ReliabilityPolicy.BEST_EFFORT,
                                   durability=DurabilityPolicy.VOLATILE),
            callback=self.current_compas_heading_cb,
        )
        
        self.pose_index = 0
        self.previous_global_pose: NavSatFix = None
        self.previous_sane_speed = 0.0
        
        self.compas_heading = 0.0
        self.flight_key = 6
        
        self.sql_controller = SQLController()
        
        
        
    def current_global_pose_cb(self, msg: NavSatFix) -> None:
        speed = self.calculate_speed(msg)
        
        query = f"""INSERT INTO wgs84 (id, flight_key, lat, lon, alt, stamp, speed, bearing)
                     VALUES ({self.pose_index}, {self.flight_key}, {msg.latitude}, {msg.longitude}, {msg.altitude}, {msg.header.stamp.sec}, {speed}, {self.compas_heading});"""
        
        self.sql_controller.push(query)
        self.previous_global_pose = msg
        self.pose_index += 1

    def current_compas_heading_cb(self, msg: Float64) -> None:
        self.compas_heading = msg.data
        
    
    def calculate_speed(self, msg: NavSatFix) -> float:
        """
            Calculate speed from previous and current position
        """
        if self.pose_index == 0:
            self.previous_global_pose = msg
            self.pose_index += 1
            return 0.0
        
        else:
            distance = geodesic_distance((self.previous_global_pose.latitude, self.previous_global_pose.longitude), (msg.latitude, msg.longitude)).meters
            time = Time.from_msg(msg.header.stamp)
            previous_time = Time.from_msg(self.previous_global_pose.header.stamp)
            
            delta_time = (time - previous_time).nanoseconds / 1e9
            
            self.get_logger().info(f"Distance: {distance} meters, delta_time: {delta_time} seconds, speeed: {distance / delta_time} m/s")
            
            estimated_speed = distance / delta_time
            
            # gps glitches cause some unreasonably high speeds (> 300 m/s), stupid simple filter to remove them
            if estimated_speed > 30:
                estimated_speed = self.previous_sane_speed
            else:
                self.previous_sane_speed = estimated_speed
            
            return estimated_speed
            
            
    
        
    
        
    def plot(self) -> None:
        img = plt.imread("src/plotter/plotter/maps/map.png")
        
        longitudes = [pose.longitude for pose in self.global_pose_list]
        latitudes = [pose.latitude for pose in self.global_pose_list]
        
        fig, ax = plt.subplots(figsize = (8,7))
        ax.scatter(longitudes, latitudes, zorder=1, alpha= 0.2, c='b', s=10)
        ax.set_title('Demo plot ')
        ax.set_xlim(self.BBox[0],self.BBox[1])
        ax.set_ylim(self.BBox[2],self.BBox[3])
        ax.imshow(img, zorder=0, extent = self.BBox, aspect= 'equal')
        
        
def main():
    rclpy.init()
    node = PlotterNode()
    rclpy.spin(node)
    rclpy.shutdown()
