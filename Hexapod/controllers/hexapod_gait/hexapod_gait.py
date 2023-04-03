import numpy as np

from hexapod import Hexapod



if __name__ == "__main__":

    tripod_gait = np.array([0., 1., 1., 0., 0., 1.]) * np.pi

    robot = Hexapod(
       A=.2, B=.1, leg_phase=tripod_gait
    )

    # Initial joint configuration
    q0 = np.zeros(shape=18)
    
    for i in range(1, 18, 3):
        q0[i] = 2*robot.q2_init
        q0[i+1] = robot.q3_init
        
    robot.setJointPositions(q0)
    robot.delay(500)

    for i in range(1, 18, 3):
        q0[i] = robot.q2_init
        q0[i+1] = robot.q3_init
    
    robot.setJointPositions(q0)
    robot.delay(500)

    g = 0
    gait = np.random.randint(0, 3, size=100)

    while robot.step() != -1:
        robot.straight()
        robot.delay(5, m=True)
        pass