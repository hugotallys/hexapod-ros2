import numpy as np

from controller import Supervisor  # type: ignore


class Hexapod:

    def __init__(self) -> None:
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
        
        # self.sensors = [
        #     self.robot.getDevice(jname + "_sensor") for jname in self.joints_names
        # ]

        # for s in self.sensors:
        #     s.enable(self.timestep)

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
        return self.robot.step(self.timestep)

    def getTimeStep(self):
        return int(self.timestep) * 1e-3

    def delay(self, ms):
        counter = ms / self.timestep
        while (counter > 0) and (self.step() != -1):
            counter -= 1
