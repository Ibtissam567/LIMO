import rclpy
from rclpy.node import Node
from pylimo import limo
#from tutorial_interfaces.msg import Num
import time
limo=limo.LIMO()
limo.EnableCommand()
from std_msgs.msg import String
from interfaces.msg import Entree
from geometry_msgs.msg import Twist



class MinimalSubscriber(Node):

    def __init__(self):
        super().__init__('acceleration_des_roues')
        # self.subscription1 = self.create_subscription(
        #     Entree,
        #     'topic',
        #     self.listener_callback,
        #     10)
        self.subscription2 = self.create_subscription(Twist,
            'cmd_vel',
            self.listener_callback,
            10)
        # self.subscription  # prevent unused variable warning

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
