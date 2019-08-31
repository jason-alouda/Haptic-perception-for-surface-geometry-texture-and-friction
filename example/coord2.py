from math import sqrt, sin, cos, atan2, radians, pi, acos, asin, degrees
from arm import arm
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import time
import matplotlib.animation as animation

j1 = 50.0
j2 = 291.5
j3 = 23.38
j4 = 235.0

def ang_to_xyz(alpha, beta, theta, stop=False):
    # convert raw into spherical
    gam = atan2(j2, j1)
    j5 = sqrt(j1**2 + j2**2)
    n3 = atan2(j3 * sin(gam), j5 - j3 * cos(gam))
    t1 = sqrt( (j3 * sin(gam)) ** 2 + (j5 - j3 * cos(gam)) ** 2)
    n4p = beta + gam + n3
    t2 = j4 * cos(n4p)
    t3 = j4 * sin(n4p)
    j13 = sqrt( (t1 + t2) ** 2 + (t3) ** 2 )
    # print(f"j13:  {j13/25.4} inches")
    zetta = alpha - gam - n3 - atan2(-t3, t1 + j4 * cos(n4p))
    x, y, z = j13 * sin(zetta), 0, j13 * cos(zetta)
    # rotate around z by theta
    # if not stop: print(xyz_to_ang(x, y, z, True))
    return x * cos(theta), x * sin(theta), z

def xyz_to_ang(x, y, z, stop=False):
    # find beta
    gam = atan2(j2, j1)
    j13 = sqrt(x**2 + y**2 + z**2)
    j5 = sqrt(j1**2 + j2**2)
    j9 = sqrt( (j3 * sin(gam)) ** 2 + (j5 - j3 * cos(gam)) ** 2 )
    n4p = acos( (j13 ** 2 - j9 ** 2 - j4 ** 2) / (2 * j9 * j4) )
    n3 = atan2(j3 * sin(gam), j5 - j3 * cos(gam))
    beta = -n4p + gam + n3 + pi + 0.18213632307686112
    # convert to spherical and find alpha and theta
    theta = -atan2(y, x)
    # rotate the vector back to standard position
    x_, y_, z_ = x * cos(theta) - y * sin(theta), x * sin(theta) + y * cos(theta), z
    # phi = acos(z / j13)
    # zetta = 0.5 * pi - phi
    zetta = atan2(z_, x_)
    # psi = asin(-j9 * sin(n4p) / j13)
    # alpha = zetta - beta - psi + pi
    n5 = -asin(-j4 * sin(n4p) / j13)
    alpha = zetta + gam + n3 + n5 - 0.5 * pi
    # if not stop: print(ang_to_xyz(alpha, beta, theta, True))
    return alpha, beta, theta
'''
fig = plt.figure()
ax1 = fig.add_subplot(111, projection='3d')
limit = 300
ax1.set_xlim(-limit, limit)
ax1.set_ylim(-limit, limit)
ax1.set_zlim(-limit, limit)
ax1.set_xlabel('X')
ax1.set_ylabel('Y')
ax1.set_zlabel('Z')
a = arm()
'''

def within_limits(m1, m2, m4):
    return (m1 > 120 and m1 < 2100) and (m2 > 1300 and m2 < 2430) and (m4 > 690 and m4 < 3360)

def animate(i):
    # if(i % 100 == 0): ax1.clear()
    state = a.read_state()
    m1, m2, m4 = -0.088 * (state['p1'] - 1024), -0.088 * (state['p2'] - 2048), -0.088 * (state['p4'] - 2048) + 120 + 90
    m1, m2, m4 = radians(m1), radians(m2), radians(m4)
    x, y, z = ang_to_xyz(m2, m4, m1)
    print(f"cor: {x},   {y},   {z}")
    print(f"ang: {m2}, {m4}, {m1}")
    alpha, beta, theta = xyz_to_ang(-x, y, z)
    ax1.scatter(x, y, z, marker='*')
    # x, y, z = ang_to_xyz(alpha, beta, theta)
    # ax1.scatter(x, y, z, marker='^')
    ax1.view_init(elev=10., azim=i*5)

def move_to(x, y, z, a):
    alpha, beta, theta = xyz_to_ang(x, y, z)
    alpha, beta, theta = degrees(alpha), degrees(beta), degrees(theta)
    # print([alpha, beta, theta])
    m1, m2, m4 = (theta / 0.088) + 1024, (alpha / -0.088) + 2048, ((beta - 120 - 90) / -0.088) + 2048
    # print(f"m1: {m1}   m2: {m2}    m4: {m4}")
    if not within_limits(m1, m2, m4): print("OUT OF LIMITS!!!")
    else: a.set_all_pos_slow(m1, m2, m4)
    
def get_coordinates(a):
    state = a.read_state()
    m1, m2, m4 = -0.088 * (state['p1'] - 1024), -0.088 * (state['p2'] - 2048), -0.088 * (state['p4'] - 2048) + 120 + 90
    m1, m2, m4 = radians(m1), radians(m2), radians(m4)
    x, y, z = ang_to_xyz(m2, m4, m1)
    return x, y, z
    
def get_distance(a):
    x, y, z = get_coordinates(a)
    return (sqrt(x*x + y*y))
    

if __name__=='__main__':
    pass

#ani = animation.FuncAnimation(fig, animate, interval=300)
#plt.show()



