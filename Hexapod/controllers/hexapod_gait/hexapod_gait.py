import numpy as np

from hexapod import Hexapod

class Gait:

  w = 2 * np.pi
  dt = 0.01
  t = np.arange(0., 2*np.pi/w, dt)
  q = np.zeros(shape=18)

  def __init__(self, A, B, leg_phase) -> None:

    self.q1_init = 0.
    self.q2_init = -1.
    self.q3_init = 2.5

    self.A = A
    self.B = B
    self.C = 0.5 * self.B

    self.q1t = self.A * np.sin(self.w * self.t) + self.q1_init
    self.q2t = self.B * np.clip(np.cos(self.w * self.t), -1., 0.) + self.q2_init
    self.q3t = self.q3_init * np.ones_like(self.q2t) # self.C * np.clip(np.cos(self.w * self.t), -1., 0.) + self.q3_init

    self.inc = 0
    self.s = 1
    self.k = [int(p / (self.w * self.dt)) for p in leg_phase]

  def move(self):
    
    for i in range(0, 16, 3):
      j = (self.inc - self.k[int(i / 3)]) % len(self.t)
      self.q[i] = self.q1t[j]
      self.q[i+1] = self.q2t[j]
      self.q[i+2] = self.q3t[j]
      self.inc = (self.inc + self.s) % len(self.t)

if __name__ == "__main__":

    # Tripod gait
    # A=.3, B=.15, q_init=[0., -1., 2.5], leg_phase=[0., np.pi, np.pi, 0., 0., np.pi]
    
    robot = Hexapod()
    gait = Gait(
      A=.3, B=.15, leg_phase=[0., np.pi, np.pi, 0., 0., np.pi]
    )

    # Initial joint configuration
    q0 = np.zeros(shape=18)
    
    for i in range(1, 18, 3):
        q0[i] = 2*gait.q2_init
        q0[i+1] = gait.q3_init
        
    robot.setJointPositions(q0)
    robot.delay(500)

    for i in range(1, 18, 3):
        q0[i] = gait.q2_init
        q0[i+1] = gait.q3_init
    
    robot.setJointPositions(q0)
    robot.delay(500)

    while robot.step() != -1:
      gait.move()
      robot.setJointPositions(gait.q)
      robot.delay(5)
