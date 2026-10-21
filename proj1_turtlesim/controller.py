
import sys
import select
import termios
import tty

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


def main():
    turtle = sys.argv[1] if len(sys.argv) > 1 else "turtle1"

    rclpy.init()
    node = Node("controller_" + turtle)

    topic = "/" + turtle + "/cmd_vel"
    pub = node.create_publisher(Twist, topic, 10)

    print(turtle)
    print("WASD")

    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    tty.setcbreak(fd)

    try:
        while rclpy.ok():
            msg = Twist()

            if select.select([sys.stdin], [], [], 0.1)[0]:
                key = sys.stdin.read(1).lower()

                if key == 'w':
                    msg.linear.x = 2.0
                elif key == 's':
                    msg.linear.x = -2.0
                elif key == 'a':
                    msg.angular.z = 2.0
                elif key == 'd':
                    msg.angular.z = -2.0

            pub.publish(msg)

    except KeyboardInterrupt:
        pass

    finally:
        pub.publish(Twist())
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
