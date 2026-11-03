
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
        super().__init__('odom_node')
        self.publisher_ = self.create_publisher(Position, 'Positionxy', 10)
        timer_period = 0.5
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i=0
        self.position_calculer=0.0
        self.odom_value=None
        self.subscription1 = self.create_subscription(
            Odom,
            'odometrie',
            self.listener_callback,
            10)
        # self.subscription2 = self.create_subscription(Twist,
        #     'cmd_vel',
        #     self.listener_callback,
        #     10)
        # self.subscription  # prevent unused variable warning

    def listener_callback(self, odom):
        # self.get_logger().info(': "%s"' % msg.vitess_l)
        # self.get_logger().info(': "%s"' % msg.omega)
        ##Description odom

        # int64 leftwheelodom
        # int64 rightwheelodom
        # float32 steeringangle
        self.odom_value=odom
        self.get_logger().info(': odoml "%s"' % odom.leftwheelodom)
        self.get_logger().info(': odomr  "%s"' % odom.rightwheelodom)
        self.get_logger().info(': odomr  "%s"' % odom.steeringangle)

        # a=msg.vitess_l+1
        # limo.SetMotionCommand(linear_vel= a,angular_vel = 0)
    def timer_callback(self):
        msg = Position()
        #Description de la position
        # float32 positionx
        # float32 positiony
        # float32 positionfx
        # float32 positionfy
        self.positioncalculator()
        if(self.odom_value!=None):
            msg.positionx=self.position_calculer
            msg.positiony=self.position_calculer
        else:
            msg.positionx=0.0
            msg.positiony=0.0

        msg.positionfx=0.0
        msg.positionfy=0.0
        self.publisher_.publish(msg)
        self.get_logger().info('positionx: "%s"' % msg.positionx)
        # self.get_logger().info('Thetapoint: "%s"' % msg.omega)
        self.i += 1
    def positioncalculator(self):
        if(self.odom_value!=None):
            # self.position_calculer=self.odom_value.leftwheelodom*5.1
            self.position_calculer=0.0
        else:
            self.position_calculer=0.0





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



