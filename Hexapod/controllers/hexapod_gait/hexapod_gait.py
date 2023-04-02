import numpy as np

from hexapod import Hexapod



if __name__ == "__main__":

    # Tripod robot
    # A=.3, B=.15, q_init=[0., -1., 2.5], leg_phase=[0., np.pi, np.pi, 0., 0., np.pi]
    
    robot = Hexapod(
       A=.3, B=.2, leg_phase=[0., np.pi, np.pi, 0., 0., np.pi]
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

      if gait[g] == 0:
        robot.straight()
      elif gait[g] == 1:
        robot.rotate(clockwise=True)
      elif gait[g] == 2:
        robot.rotate(clockwise=False)
      
      robot.delay(2000)

      g = (g + 1) % len(gait)
