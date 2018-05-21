#!/usr/bin/env python

# Import modules
from pcl_helper import *
import ipdb

# TODO: Define functions as required

def segment_objects(cloud_objects):

    white_cloud = XYZRGB_to_XYZ(cloud_objects)
    tree = white_cloud.make_kdtree()

    # Create a cluster extraction object
    ec = white_cloud.make_EuclideanClusterExtraction()
    # Set tolerances for distance threshold
    # as well as minimum and maximum cluster sizes (in points)
    ec.set_ClusterTolerance(0.02)
    ec.set_MinClusterSize(10)
    ec.set_MaxClusterSize(2000)
    ec.set_SearchMethod(tree)
    cluster_indices = ec.Extract()


    # TODO: Create Cluster-Mask Point Cloud to visualize each cluster separately

    cluster_color = get_color_list(len(cluster_indices))
    color_cluster_point_list = []

    for j, indices in enumerate(cluster_indices):
        for i, indice in enumerate(indices):
            point_item = white_cloud[indice]
            color_cluster_point_list.append([ point_item[0],
                                              point_item[1],
                                              point_item[2],
                                              rgb_to_float(cluster_color[j])
                                            ]
                                           )
    cluster_cloud = pcl.PointCloud_PointXYZRGB()
    cluster_cloud.from_list(color_cluster_point_list)
    ros_cluster_cloud = pcl_to_ros(cluster_cloud)
    return ros_cluster_cloud


# Callback function for your Point Cloud Subscriber
def pcl_callback(pcl_msg):

    # TODO: Convert ROS msg to PCL data
    cloud = ros_to_pcl(pcl_msg)

    # TODO: Voxel Grid Downsampling
    vox = cloud.make_voxel_grid_filter()
    LEAF_SIZE = 0.01
    vox.set_leaf_size(LEAF_SIZE, LEAF_SIZE, LEAF_SIZE)
    cloud_filtered = vox.filter()


    # TODO: PassThrough Filter
    passthrough = cloud_filtered.make_passthrough_filter()
    filter_axis = 'z'
    passthrough.set_filter_field_name(filter_axis)
    axis_min = 0.76; axis_max=2
    passthrough.set_filter_limits(axis_min, axis_max)

    cloud_filtered = passthrough.filter()

    #ros_cloud_passthrough = pcl_to_ros(cloud_filtered)
    #pcl_table_pub.publish(ros_cloud_passthrough)

    if 1:
        # TODO: RANSAC Plane Segmentation
        seg = cloud_filtered.make_segmenter()
        seg.set_model_type(pcl.SACMODEL_PLANE)
        seg.set_method_type(pcl.SAC_RANSAC)

        # TODO: Extract inliers and outliers
        max_distance = 0.01
        seg.set_distance_threshold(max_distance)
        inliers, coefficients = seg.segment()
        cloud_table = cloud_filtered.extract(inliers, negative=False)
        cloud_objects = cloud_filtered.extract(inliers, negative=True)

        # TODO: Euclidean Clustering
        ros_cluster_cloud = segment_objects(cloud_objects)

        # TODO: Convert PCL data to ROS messages
        ros_cloud_table = pcl_to_ros(cloud_table)
        if 0:
            pcl.save(cloud_objects, 'cloud_objects.pcd')

        ros_cloud_objects = pcl_to_ros(cloud_objects)

        # TODO: Publish ROS messages
        pcl_objects_pub.publish(ros_cloud_objects)
        pcl_table_pub.publish(ros_cloud_table)
        pcl_cluster_pub.publish(ros_cluster_cloud)


def debug():
    cloud_objects = pcl.load('cloud_objects.pcd')
    ros_cloud_objects = pcl_to_ros(cloud_objects)
    ros_cluster_cloud = segment_objects(ros_cloud_objects)

if __name__ == '__main__':

  if 0:
    debug()

  if 1:
    # TODO: ROS node initialization
    rospy.init_node('clustering', anonymous=True)

    # TODO: Create Subscribers
    pcl_sub = rospy.Subscriber("/sensor_stick/point_cloud",
                               pc2.PointCloud2, pcl_callback, queue_size =1)

    # TODO: Create Publishers
    pcl_objects_pub = rospy.Publisher("/pcl_objects", PointCloud2, queue_size=1)
    pcl_table_pub = rospy.Publisher("/pcl_table", PointCloud2, queue_size=1)
    pcl_cluster_pub = rospy.Publisher("/pcl_cluster", PointCloud2, queue_size=1)
    # Initialize color_list
    get_color_list.color_list = []

    # TODO: Spin while node is not shutdown
    while not rospy.is_shutdown():
        rospy.spin()
