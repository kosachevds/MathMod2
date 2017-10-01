import math
import numpy
from matplotlib import pyplot

U = 3000.0
M0 = 100.0
LAMBDA = 0.1
MP = 10.0
FUEL_CONST = 0.4
MS = LAMBDA * (M0 - MP)
MT = (1 - LAMBDA) * (M0 - MP)
MAX_VELOCITY = U * math.log(M0 / (MP + MS))
print "ms = {} mt = {}".format(MS, MT)


def fuel(t):
    mass = MT - FUEL_CONST * t
    return mass if mass > 0.0 else 0.0


def velocity(t):
    return U * math.log(M0 / (MP + MS + fuel(t)))


def max_velocity(mp, lambda_):
    ms = lambda_ * (M0 - mp)
    return U * math.log(M0 / (mp + ms))


MAX_TIME = 3 * 60
t_list = numpy.arange(0, MAX_TIME).tolist()
v_list = [velocity(t) for t in t_list]
pyplot.figure(1)
pyplot.title("v(t), max = {:.3f} km/s".format(MAX_VELOCITY / 1000.0))
pyplot.plot(t_list, v_list)
pyplot.xlabel("time")
pyplot.ylabel("velocity")

mp_list = numpy.arange(0, 10, 0.3)
pyplot.figure(2)
legend_handles = []
for lambda_ in numpy.arange(0.01, 0.12, 0.02):
    v_list = [max_velocity(m, lambda_) for m in mp_list]
    label = "Lambda = {}, max = {:.3f}".format(lambda_, max(v_list) / 1000)
    handle, = pyplot.plot(mp_list, v_list, label=label)
    legend_handles.append(handle)
pyplot.legend(handles=legend_handles)
pyplot.xlabel("mp")
pyplot.ylabel("max velocity")
pyplot.show()
