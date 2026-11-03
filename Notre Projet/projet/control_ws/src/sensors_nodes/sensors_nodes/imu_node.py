import rclpy
from rclpy.node import Node
from pylimo import limo
#from tutorial_interfaces.msg import Num
import time
limo=limo.LIMO()
limo.EnableCommand()
from std_msgs.msg import String
from interfaces.msg import *

class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('imu_node')
        self.publisher_ = self.create_publisher(Entree, 'topic', 10)
        timer_period = 0.5
        timer_period2 = 1# seconds
        self.publisher1_ = self.create_publisher(Odom, 'odometrie', 10)
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.timer2 = self.create_timer(timer_period2, self.timer_callback2)
        self.i = 0
        self.j = 0


    def timer_callback(self):
        msg = Entree()
        a=limo.GetIMUAccelData()
        # float32 vitess_l
        # float32 omega
        print(limo.GetLinearVelocity())
        msg.vitess_l =limo.GetLinearVelocity()
        # msg.omega =limo.GetAngularVelocity()[2]
        msg.omega =limo.GetAngularVelocity()
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

    minimal_publisher = MinimalPublisher()

    rclpy.spin(minimal_publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

