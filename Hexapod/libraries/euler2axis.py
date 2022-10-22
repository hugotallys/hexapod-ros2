import math

def euler_yzx_to_axis_angle(z_e, x_e, y_e, normalize=True):
    # Assuming the angles are in radians.
    c1 = math.cos(z_e/2)
    s1 = math.sin(z_e/2)
    c2 = math.cos(x_e/2)
    s2 = math.sin(x_e/2)
    c3 = math.cos(y_e/2)
    s3 = math.sin(y_e/2)
    c1c2 = c1*c2
    s1s2 = s1*s2
    w = c1c2*c3 - s1s2*s3
    x = c1c2*s3 + s1s2*c3
    y = s1*c2*c3 + c1*s2*s3
    z = c1*s2*c3 - s1*c2*s3
    angle = 2 * math.acos(w)
    if normalize:
        norm = x*x+y*y+z*z
        if norm < 0.001:
            # when all euler angles are zero angle =0 so
            # we can set axis to anything to avoid divide by zero
            x = 1
            y = 0
            z = 0
        else:
            norm = math.sqrt(norm)
            x /= norm
            y /= norm
            z /= norm
    return z, x, y, angle

print(euler_yzx_to_axis_angle(0.5*math.pi, 0., 0.5*math.pi))