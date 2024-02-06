#!/usr/bin/env python3

# import ROS for developing the node
import rospy
# import geometry_msgs/Twist for control commands
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from robotics_lab_1.msg import Turtlecontrol
#initializing pose and turtlecontrol
pose_msg = Pose() 
control_msg = Turtlecontrol()

def pos_callback(data):#position info, used pos_publisher.py from example code
	global pos_msg
	#convert linear position to degrees and store in pose obj
	pos_msg.xd = data.xd 
def control_gain(data):#control gain info., used pos_callback from example code as an outline
	global control_msg 
	#get control gain values and store them in turtlecontrol
	control_msg.kp = data.kp
	
if __name__ == '__main__':
	# declare a publisher to publish in the velocity command topic
	cmd_pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size = 10)
	# initialize the node
	rospy.init_node('ControlNode', anonymous = True)
	# set a 10Hz frequency for this loop
	rospy.Subscriber('/turtle1/pose',pos_msg, pose_callback)
	#subcriber to turtle1/pose topic, taking in pose
	rospy.Subscriber('/turtle1/control_params', control_msg, control_gain)
	#subcriber to turtle1/control_params topic, taking in turtlecontrol
	loop_rate = rospy.Rate(10)
	# declare a variable of type Twist for sending control commands
	vel_cmd = Twist()
	# run this control loop regularly
	while not rospy.is_shutdown():
		# set the linear (forward/backward) velocity command
		vel_cmd.linear.x = control_msg.kp * (control_msg.xd - control_msg.x) #formula from assignment page
		# publish the command to the defined topic
		cmd_pub.publish(vel_cmd)
		# wait for 0.1 seconds until the next loop and repeat
		loop_rate.sleep()
		
