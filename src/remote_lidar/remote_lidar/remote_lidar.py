import sys
import os
os.environ['NUMEXPR_MAX_THREADS'] = '12'

import rclpy 
from rclpy.node import Node
import sensor_msgs.msg as sensor_msgs


import numpy as np
import open3d as o3d

from rclpy.qos import QoSProfile
import rclpy.qos


flag = False

class PCDListener(Node):

    def __init__(self):
        super().__init__('pcd_subscriber')

        ## This is for visualization of the received point cloud.
        self.vis = o3d.visualization.Visualizer()
        self.vis.create_window(width=1623, height=855)
        self.o3d_pcd = o3d.geometry.PointCloud()
        self.render_option: o3d.visualization.RenderOption = self.vis.get_render_option()
        self.render_option.background_color = np.array([0.2, 0.2, 0.2])
        self.render_option.point_size = 1.5
        
        qos_profile = QoSProfile(
            reliability = rclpy.qos.ReliabilityPolicy.BEST_EFFORT,
            history = rclpy.qos.HistoryPolicy.KEEP_LAST,
            depth = 1
        )

        # Set up a subscription to the 'pcd' topic with a callback to the 
        # function `listener_callback`
        self.pcd_subscriber = self.create_subscription(
            sensor_msgs.PointCloud2,        # Msg type
            'sensing/lidar/concatenated/pointcloud',     # topic
            self.listener_callback,         # Function to call
            qos_profile                     # QoS
        )

                
    def listener_callback(self, msg):
        global flag
        # Here we convert the 'msg', which is of the type PointCloud2.
        # I ported the function read_points2 from 
        # the ROS1 package. 
        # https://github.com/ros/common_msgs/blob/noetic-devel/sensor_msgs/src/sensor_msgs/point_cloud2.py

        pcd_as_numpy_array = np.array(list(read_points(msg)))
        
        # Reshape dimension of point cloud
        pcd_as_numpy_array = np.delete(pcd_as_numpy_array, 3, axis=1)
        

        # The rest here is for visualization.
        self.vis.remove_geometry(self.o3d_pcd)
        
        try:
            vec = o3d.utility.Vector3dVector(pcd_as_numpy_array)
            self.o3d_pcd = o3d.geometry.PointCloud(vec)
        except:
            self.o3d_pcd = o3d.geometry.PointCloud()

        self.vis.add_geometry(self.o3d_pcd)
        
        ctr = self.vis.get_view_control()
        parameters = o3d.io.read_pinhole_camera_parameters("./config/ScreenCamera_position.json")
        ctr.convert_from_pinhole_camera_parameters(parameters)

        
        self.vis.poll_events()
        self.vis.update_renderer()

        # if not flag:
        #     while True:
        #         self.vis.poll_events()
        #         self.vis.update_renderer()
        # flag = True
        


## The code below is "ported" from 
# https://github.com/ros/common_msgs/tree/noetic-devel/sensor_msgs/src/sensor_msgs
import sys
from collections import namedtuple
import ctypes
import math
import struct
from sensor_msgs.msg import PointCloud2, PointField

_DATATYPES = {}
_DATATYPES[PointField.INT8]    = ('b', 1)
_DATATYPES[PointField.UINT8]   = ('B', 1)
_DATATYPES[PointField.INT16]   = ('h', 2)
_DATATYPES[PointField.UINT16]  = ('H', 2)
_DATATYPES[PointField.INT32]   = ('i', 4)
_DATATYPES[PointField.UINT32]  = ('I', 4)
_DATATYPES[PointField.FLOAT32] = ('f', 4)
_DATATYPES[PointField.FLOAT64] = ('d', 8)

def read_points(cloud, field_names=None, skip_nans=False, uvs=[]):
    """
    Read points from a L{sensor_msgs.PointCloud2} message.

    @param cloud: The point cloud to read from.
    @type  cloud: L{sensor_msgs.PointCloud2}
    @param field_names: The names of fields to read. If None, read all fields. [default: None]
    @type  field_names: iterable
    @param skip_nans: If True, then don't return any point with a NaN value.
    @type  skip_nans: bool [default: False]
    @param uvs: If specified, then only return the points at the given coordinates. [default: empty list]
    @type  uvs: iterable
    @return: Generator which yields a list of values for each point.
    @rtype:  generator
    """
    assert isinstance(cloud, PointCloud2), 'cloud is not a sensor_msgs.msg.PointCloud2'
    fmt = _get_struct_fmt(cloud.is_bigendian, cloud.fields, field_names)
    width, height, point_step, row_step, data, isnan = cloud.width, cloud.height, cloud.point_step, cloud.row_step, cloud.data, math.isnan
    unpack_from = struct.Struct(fmt).unpack_from

    if skip_nans:
        if uvs:
            for u, v in uvs:
                p = unpack_from(data, (row_step * v) + (point_step * u))
                has_nan = False
                for pv in p:
                    if isnan(pv):
                        has_nan = True
                        break
                if not has_nan:
                    yield p
        else:
            for v in range(height):
                offset = row_step * v
                for u in range(width):
                    p = unpack_from(data, offset)
                    has_nan = False
                    for pv in p:
                        if isnan(pv):
                            has_nan = True
                            break
                    if not has_nan:
                        yield p
                    offset += point_step
    else:
        if uvs:
            for u, v in uvs:
                yield unpack_from(data, (row_step * v) + (point_step * u))
        else:
            for v in range(height):
                offset = row_step * v
                for u in range(width):
                    yield unpack_from(data, offset)
                    offset += point_step

def _get_struct_fmt(is_bigendian, fields, field_names=None):
    fmt = '>' if is_bigendian else '<'

    offset = 0
    for field in (f for f in sorted(fields, key=lambda f: f.offset) if field_names is None or f.name in field_names):
        if offset < field.offset:
            fmt += 'x' * (field.offset - offset)
            offset = field.offset
        if field.datatype not in _DATATYPES:
            print('Skipping unknown PointField datatype [%d]' % field.datatype, file=sys.stderr)
        else:
            datatype_fmt, datatype_length = _DATATYPES[field.datatype]
            fmt    += field.count * datatype_fmt
            offset += field.count * datatype_length

    return fmt



def main(args=None):
    # Boilerplate code.
    rclpy.init(args=args)
    pcd_listener = PCDListener()
    rclpy.spin(pcd_listener)
    
    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    pcd_listener.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

