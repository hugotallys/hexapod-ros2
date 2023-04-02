import numpy as np

from controller import Supervisor  # type: ignore
    

class Hexapod:

    w = np.pi
    dt = 0.01
    t = np.arange(0., 2*np.pi/w, dt)
    q = np.zeros(shape=18)

    def __init__(self, A, B, leg_phase) -> None:
        self.robot = Supervisor()
        self.timestep = int(self.robot.getBasicTimeStep())

        self.joints = [
            self.robot.getDevice(f"joint{i+1}{j+1}") for i in range(6) for j in range(3)
        ]

        self.joints_ranges = [
            (
                joint.getMinPosition(), joint.getMaxPosition()
            ) for joint in self.joints
        ]
        
        # self.camera = self.robot.getDevice("camera")
        # self.camera.enable(self.timestep)

        # self.sensors = [
        #     self.robot.getDevice(jname + "_sensor") for jname in self.joints_names
        # ]

        # for s in self.sensors:
        #     s.enable(self.timestep)
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

        self.amp = 1
        self.legset = None

    def move(self):
        _amp = self.amp

        for i in range(0, 16, 3):
            if self.legset is not None:
                _amp = -self.amp if i in self.legset else self.amp
            j = (self.inc - self.k[int(i / 3)]) % len(self.t)
            self.q[i] = _amp * self.q1t[j]
            self.q[i+1] = self.q2t[j]
            self.q[i+2] = self.q3t[j]
            self.inc = (self.inc + self.s) % len(self.t)

    def rotate(self, clockwise=True):
        self.legset = [0, 6, 12] if clockwise else [3, 9, 15]

    def straight(self):
        self.legset = None

    @staticmethod
    def cross_product(a: np.ndarray, b: np.ndarray) -> np.ndarray:
        return np.cross(a,b)

    @staticmethod
    def pose(r):
        return r[0:3, -1].reshape(3, 1)

    @staticmethod
    def dh_transform(theta, d, a, alpha):
        ct, st = np.cos(theta), np.sin(theta)
        ca, sa = np.cos(alpha), np.sin(alpha)
        return np.array([
            ct, -st*ca, st*sa, a*ct,
            st, ct*ca, -ct*sa, a*st,
            0., sa, ca, d,
            0., 0., 0., 1.
        ]).reshape(4, 4)
    
    def setJointPositions(self, q):
        for i, joint in enumerate( self.joints ):
            joint.setPosition(q[i])

    # def getJointPositions(self):
    #     return np.array(
    #         list(map(lambda s: s.getValue(), self.sensors))
    #     )

    def step(self):
        self.move()
        self.setJointPositions(self.q)
        return self.robot.step(self.timestep)

    def getTimeStep(self):
        return int(self.timestep) * 1e-3

    def delay(self, ms):
        counter = ms / self.timestep
        while (counter > 0) and (self.step() != -1):
            counter -= 1
