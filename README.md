# Indra Navia ROS concept

This is a minimum viable product for the Indra Navia summer project

Consists of plotter_node that logs the drones global position and heading, calculates instantaneus velocity of the drone from these 2 and pushes it to an sql database

another python class MapPlotter includes functionality to visualize the data using a scatter plot within a bounding box image


# Comments

This is only a simple example that I spent an hour playing around with. The data gathering node is lacking other data the the flight controller logs that could be extracted are:
- Trajectory
- instantaneus velocity (in local coordinates), this requires using transforms (trivial but painfull)

This data can be piped into a machine learning algorithm to predict the path of the drone. I beleive that the instantanues velocity combined with the gps location and trajectory will be more than enough data for a good estimate of the drones path


