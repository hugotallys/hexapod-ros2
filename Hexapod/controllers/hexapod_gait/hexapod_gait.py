import numpy as np

from hexapod import Hexapod

w = np.pi

def q1(t):
  A = .3
  return A * np.sin(w * t)

def q2(t):
  B = .15
  return B * np.clip(np.cos(w * t), -1., 0.)

def q3(t):
  C = .05
  return C * np.clip(np.cos(w * t), -1., 0.)

def turn_clockwise():
  q0[0] = q1t[i]
  q0[1] = q2t[i]
  q0[2] = q3t[i]

  q0[3] = _q1t[j]
  q0[4] = _q2t[j]
  q0[5] = _q3t[j]

  q0[6] = q1t[k]
  q0[7] = q2t[k]
  q0[8] = q3t[k]

  q0[9] = _q1t[l]
  q0[10] = _q2t[l]
  q0[11] = _q3t[l]

  q0[12] = q1t[m]
  q0[13] = q2t[m]
  q0[14] = q3t[m]

  q0[15] = _q1t[n]
  q0[16] = _q2t[n]
  q0[17] = _q3t[n]

def turn_anticlockwise():
  q0[0] = _q1t[i]
  q0[1] = _q2t[i]
  q0[2] = _q3t[i]

  q0[3] = q1t[j]
  q0[4] = q2t[j]
  q0[5] = q3t[j]

  q0[6] = _q1t[k]
  q0[7] = _q2t[k]
  q0[8] = _q3t[k]

  q0[9] = q1t[l]
  q0[10] = q2t[l]
  q0[11] = q3t[l]

  q0[12] = _q1t[m]
  q0[13] = _q2t[m]
  q0[14] = _q3t[m]

  q0[15] = q1t[n]
  q0[16] = q2t[n]
  q0[17] = q3t[n]

def forward():
  q0[0] = q1t[i]
  q0[1] = q2t[i]
  q0[2] = q3t[i]

  q0[3] = q1t[j]
  q0[4] = q2t[j]
  q0[5] = q3t[j]

  q0[6] = q1t[k]
  q0[7] = q2t[k]
  q0[8] = q3t[k]

  q0[9] = q1t[l]
  q0[10] = q2t[l]
  q0[11] = q3t[l]

  q0[12] = q1t[m]
  q0[13] = q2t[m]
  q0[14] = q3t[m]

  q0[15] = q1t[n]
  q0[16] = q2t[n]
  q0[17] = q3t[n]

if __name__ == "__main__":

    robot = Hexapod()

    t = np.arange(0., 2*np.pi/w, 0.01)
    q1t, q2t, q3t = q1(t), q2(t), q3(t)
    _q1t, _q2t, _q3t = np.flip(q1(t)), np.flip(q2(t)), np.flip(q3(t))

    # Initial joint configuration
    q0 = np.zeros(shape=18)
    
    for i in range(1, 18, 3):
        q0[i] = -1.5
        q0[i+1] = 2.5
        robot.setJointPositions(q0)
    
    robot.delay(500)

    for i in range(1, 18, 3):
        q0[i] = -1.
        q0[i+1] = 2.5
        robot.setJointPositions(q0)

    robot.delay(500)

    q2t = q2t - 1.
    q3t = q3t + 2.5

    _q2t = _q2t - 1.
    _q3t = _q3t + 2.5

    # trpod gait
    i = 0 
    j = -100
    k = -100
    l = 0
    m = 0
    n = -100

    s = 5

    count = 0
    clock_wise = False

    while robot.step() != -1:
        '''if count < 100:
          forward()
        elif count < 200:
          if clock_wise:
            turn_clockwise()
          else:
            turn_anticlockwise()
        else:
          count = 0
          clock_wise = not clock_wise'''

        forward()

        robot.delay(5)

        i = (i + s) % len(t)
        j = (j + s) % len(t)
        k = (k + s) % len(t)
        l = (l + s) % len(t)
        m = (m + s) % len(t)
        n = (n + s) % len(t)

        count += 1

        robot.setJointPositions(q0)
