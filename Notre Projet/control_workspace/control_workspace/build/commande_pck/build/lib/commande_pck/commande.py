import numpy as np
import matplotlib.pyplot as plt
import rclpy
import time
from rclpy.node import Node
# from pylimo import limo
import time
# limo=limo.LIMO()
# limo.EnableCommand()
from std_msgs.msg import String
from interfaces.msg import *
from geometry_msgs.msg import Twist
class MinimalSubscriber(Node):

    def __init__(self):
        super().__init__('commande')
        ##sub
        self.subscription1 = self.create_subscription(
            Position,
            'Positionxy',
            self.listener_callback,
            10)
        self.subscription2 = self.create_subscription(Entree,
            'topic',
            self.listener_callback2,
            10)
        ##pub
        self.publisher_ = self.create_publisher(Twist,'cmd_vel', 10)
        self.publisher2_ = self.create_publisher(Position, 'Positionxy', 10)
        timer_period = 0.5
        timer_period2 = 0.5
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.timer2 = self.create_timer(timer_period2, self.timer_callback2)
        self.i=0
        ##initialisation des variables
        self.position_calculer=0.0
        self.position_recup=None
        self.entree_recup=None
        self.x=-1.0
        self.y=-1.0
        self.theta=0.4
        self.x_star=1.0
        self.y_star=0.0
        self.theta_star=1.5
        self.v=0
        self.gamma=0.0



        # self.subscription  # prevent unused variable wacolcon build --packages-select my_packagerning

    def listener_callback(self, posixy):
        self.position_recup=posixy
        self.get_logger().info(': x "%s"' % posixy.positionx)
        self.get_logger().info(': y  "%s"' % posixy.positiony)
        # self.get_logger().info(': odomr  "%s"' % posixy.positionfx)
        # self.get_logger().info(': odomr  "%s"' % posixy.positionfy)
        if (self.position_recup!=None):
            self.x=posixy.positionx
            self.y=posixy.positiony


    def listener_callback2(self, entree):
        self.entree_recup=entree
        self.get_logger().info(': vitessereel "%s"' % entree.vitess_l)
        self.get_logger().info(': vitesseangulairereel  "%s"' % entree.omega)

    def timer_callback(self):
        msg = Twist()
        #Description de la position
        # float32 positionx
        # float32 positiony
        # float32 positionfx
        # float32 positionfy
        time.sleep(0.1)
        self.positioncalculator()
        self.controleuropt()
        epsilon = 10**(-3)

        if(abs(self.x-self.x_star) > epsilon or abs(self.y-self.y_star) > epsilon or abs(self.theta - self.theta_star) > epsilon):
            if(self.position_calculer!=None):
                msg.linear.x=self.v/10+0.0
                msg.angular.z=self.gamma+0.0
            else:
                msg.linear.x=0.0
                msg.angular.z=0.0
        else:
                msg.linear.x=0.0
                msg.angular.z=0.0
                print('fin')

        self.publisher_.publish(msg)
        self.get_logger().info('vitessedemander: "%s"' % msg.linear.x)
        self.get_logger().info('vitessaangulairedemander: "%s"' % msg.angular.z)
        self.i += 1


    def listener_callback2(self,msg):
        self.get_logger().positionxpub "%s"' % msg.positionx)
            msg.positiony=self.position_recup.positiony
            print("self.publisher2_.publish(msg)")
        else:
            msg.positionx=self.x
            msg.positiony=self.y
        self.publisher2_.publish(msg)

    def positioncalculator(self):

        #Description de la position
        # float32 positionx
        # float32 positiony
        # float32 positionfx
        # float32 positionf
        if (self.entree_recup!=None and self.position_recup!=None):
            mesures(self.position_recup.positionx,self.position_recup.positiony,0,self.entree_recup.vitess_l,self.entree_recup.omega)
            print("posxmesure",self.position_recup.positionx)
        else:
            print("attente")

    def controleuropt(self):
        if (self.entree_recup!=None):
            (self.x,self.y,self.theta,self.v,self.gamma)=controleur(self.x, self.y, self.theta, self.x_star,self.y_star, self.theta_star, self.entree_recup.vitess_l, self.entree_recup.omega)
        else:
                print("pas de vitesse d'entrée")
        return None


k_rho = 1
k_alpha = 20
k_beta = -10
L = 322 * 10**(-3)
T = 0.01

k_rho = 1
k_alpha = 20
k_beta = -10
L = 322 * 10**(-3)
T = 0.01

def mesures(x, y, theta, v, gamma) : #calcule x, y et theta à l'instant T pour faire un observateur

    thetap = v/L * np.tan(gamma)
    theta = theta + T*thetapcommande1

    xp = v * np.cos(theta)
    x = x + T*xp

    yp = v * np.sin(theta)
    y = y + T*yp

    return x, y, theta


def controleur(x, y, theta, x_star, y_star, theta_star, v=k_rho, gamma=k_beta+k_alpha) :#calcule rho, alpha et beta pour renvoyer gamma et v
    (x,y,theta) = mesures(x, y, theta, v, gamma)
    x1 = -x+x_star
    y1 = -y+y_star

    rho = np.sqrt(x1**2 + y1**2)
    beta = - theta_star - np.arctan2(y1,x1) # beta_tilde selon les calcules
    alpha = np.arctan2(y1,x1) - theta # -beta - theta avec le beta sans prendre en compte theta_star


    if (-1.57 <= alpha <= 1.57) :
        sens = 1
    else :
        sens = -1

    v = rho * k_rho *sens
    omega = k_alpha*alpha + k_beta*beta
    gamma = np.arctan2(L * omega, abs(v)) * sens

    return x,y,theta,v, gamma

def boucle(x0, y0, theta0, x_star, y_star, theta_star) :
    X=[x0]
    Y=[y0]
    THETA=[theta0]
    (x,y,theta,v,gamma)=controleur(x0, y0, theta0, x_star, y_star, theta_star)
    epsilon = 10**(-3)
    while (abs(x - x_star) > epsilon or abs(y - y_star) > epsilon or abs(theta - theta_star) > epsilon) :
        (x,y,theta, v,gamma) = controleur(x, y, theta, x_star, y_star, theta_star,v,gamma)
        X.append(x)
        Y.append(y)
        THETA.append(theta)
        time.sleep(T)
    return X,Y,THETA

# (X,Y,THETA) = boucle(-3, -3, 0.4, 0, 0, 1.5)
#
# t=np.linspace(0, 1000, len(X))
# #plt.plot(t, X, label='simulation de la trajectoire selon x')
# #plt.plot(t, Y, label='simulation de la trajectoire selon y')
# #plt.plot(t, THETA, label='simulation de la trajectoire selon theta')
# plt.plot(X,Y, label='simulation de la trajectoire selon xy')
#
# plt.show()
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
