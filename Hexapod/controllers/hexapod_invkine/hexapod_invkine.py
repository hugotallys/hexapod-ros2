"""hexapod_invkine controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor

from cmath import sin
import numpy as np

np.set_printoptions(precision=4, suppress=True)

from controller import Supervisor

A1 = 0.0295
A2 = 0.0800
A3 = 0.1142

# create the Robot instance.
robot = Supervisor()

# get the time step of the current world.
timestep = int(robot.getBasicTimeStep())

# You should insert a getDevice-like function in order to get the
# instance of a device of the robot. Something like:
#  motor = robot.getDevice('motorname')
#  ds = robot.getDevice('dsname')
#  ds.enable(timestep)
joints = [robot.getDevice(f"joint1{i}") for i in range(1, 4)]

def delay(ms):
    iter = ms // timestep
    while iter > 0:
        iter -= 1
        robot.step(timestep)

def setJoints(thetas):
    for i in range(3):
        joints[i].setPosition(thetas[i])
    delay(50)

target = robot.getFromDef("TARGET")

dy1 = -0.0505
dx1 = 0.0875

T01B = np.array(
    [
        1.,  0.,  0., -dx1,
        0., -1.,  0., dy1,
        0.,  0., -1.,  0.,
        0.,  0.,  0.,  1.
    ]
).reshape(4, 4)

def c(x): return np.cos( x )
def s(x): return np.sin( x )

def dh_transform(theta, d, a, alpha): return np.array([
    c(theta), -s(theta)*c(alpha), s(theta)*s(alpha), a*c(theta),
    s(theta), c(theta)*c(alpha), -c(theta)*s(alpha), a*s(theta),
    0., s(alpha), c(alpha), d,
    0, 0, 0, 1
]).reshape(4, 4)

TB0 = np.array(
    [
        1.,  0.,  0., dx1,
        0., -1.,  0., dy1,
        0.,  0., -1.,  0.,
        0.,  0.,  0.,  1.
    ]
).reshape(4, 4)

def fkine(q):
    T01 = dh_transform( q[0], 0., A1, 0.5*np.pi )
    T12 = dh_transform( q[1], 0., A2, 0. )
    T23 = dh_transform( q[2], 0., A3, 0. )
    return TB0 @ T01 #  @ T12 @ T23

def invkine(x):
    x = (T01B @ x)[:,-1]
    theta1 = np.arctan2( -x[0], x[1] )
    
    c1 = np.cos( theta1 + 0.5*np.pi )
    s1 = np.sin( theta1 + 0.5*np.pi )
    
    T10 = np.array(
        [
           c1, s1, 0., -A1,
           0., 0., 1., 0.,
           s1, -c1, 0., 0.,
           0., 0., 0., 1.
        ]
    ).reshape(4, 4)
    
    x = (T10 @ x.reshape(4, 1))[:,-1]
    x, y = x[0], x[1]
    
    theta3 = np.arccos( (x**2 + y**2 - A2**2 - A3**2) / (2*A2*A3) )    
    theta2 = np.arctan2(y, x) - np.arctan2(A3*np.sin(theta3), A2 + A3*np.cos(theta3))
        
    return np.array( [theta1, theta2, theta3] )
    
# Main loop:
# - perform simulation steps until Webots is stopping the controller
while robot.step(timestep) != -1:
    # Gets the ball position relative to frame 01
    ball_pos = np.array( target.getPose() ).reshape(4, 4)
    ball_pos = ball_pos[:,-1].reshape(4, 1)
    # q = np.array([0. + 0.5*np.pi, 0., 0.])
    # print(fkine(q))
    
    # Sets the joints positions
    setJoints(invkine(ball_pos))

# Enter here exit cleanup code.
