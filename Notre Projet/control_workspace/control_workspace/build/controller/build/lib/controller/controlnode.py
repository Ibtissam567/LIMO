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



class MinimalSubscriber(Node):

    def __init__(self):
        super().__init__('acceleration_des_roues')
        self.subscription = self.create_subscription(Entree,
            'topic',
            self.listener_callback2,
            10)
        self.subscription2 = self.create_subscription(Twist,
            'cmd_vel',
            self.listener_callback,
            10)
        self.publisher_ = self.create_publisher(Entree, 'topic', 10)
        timer_period = 0.5
        timer_period2 = 1# seconds
        self.publisher1_ = self.create_publisher(Odom, 'odometrie', 10)
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.timer2 = self.create_timer(timer_period2, self.timer_callback2)
        self.i = 0
        self.j = 0

    def listener_callback(self,twist):
        # self.get_logger().info(': "%s"' % msg.vitess_l)
        # self.get_logger().info(': "%s"' % msg.omega)
        self.get_logger().info('x: "%s"' % twist.linear.x)
        self.get_logger().info('y: "%s"' % twist.linear.y)
        self.get_logger().info('z: "%s"' % twist.linear.z)
        self.get_logger().info('ax: "%s"' % twist.angular.x)
        self.get_logger().info('ay: "%s"' % twist.angular.y)
        self.get_logger().info('az: "%s"' % twist.angular.z)
        limo.SetMotionCommand(linear_vel=twist.linear.x,steering_angle =twist.angular.z)
        # a=msg.vitess_l+1
        # limo.SetMotionCommand(linear_vel= a,angular_vel = 0)
    def listener_callback2(self,msg):
        self.get_logger().info('vitesselll: "%s"' % msg.vitess_l)
        self.get_logger().info('omegaaa: "%s"' % msg.omega)

    def timer_callback(self):
        msg = Entree()
        a=limo.GetIMUAccelData()
        # float32 vitess_l
        # float32 omega

        msg.vitess_l =limo.GetLinearVelocity()
        # msg.omega =limo.GetAngularVelocity()[2]
        msg.omega =limo.GetSteeringAngle()
        self.publisher_.publish(msg)
        self.get_logger().info('LinearSpeed: "%s"' % msg.vitess_l)
        self.get_logger().info('Thetapoint: "%s"' % msg.omega)
        self.i += 1

    def timer_callback2(self):
        msg2 = Odom()
        msg2.rightwheelodom =limo.GetRightWheelOdom()
        msg2.steeringangle=limo.GetSteeringAngle()    #msg.omega =limo.GetAngularVelocity()[2]
        msg2.leftwheelodom =limo.GetLeftWheelOdeom()
        self.publisher1_.publish(msg2)
        self.get_logger().info('odomd: "%s"' %  msg2.rightwheelodom)
        self.get_logger().info('angle: "%s"' % msg2.steeringangle)
        self.get_logger().info('odoml: "%s"' % msg2.leftwheelodom)
        self.j += 1
def main(args=None):
    rclpy.init(args=args)

    minimal_subscriber = MinimalSubscriber()

    rclpy.spin(minimal_subscriber)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main();
