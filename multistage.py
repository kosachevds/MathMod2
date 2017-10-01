import math
import numpy
from matplotlib import pyplot

STAGES_COUNT = 3
U = 3000.0
LAMBDA = 0.1
FUEL_CONST = 0.4
MP = 42.0
V = 9000.0
M0 = MP * math.pow((1 - LAMBDA) / (math.exp(-V / (STAGES_COUNT * U)) - LAMBDA),
                   STAGES_COUNT)
STAGE_MASS = (M0 - MP) / STAGES_COUNT


def fuel(mt, time):
    mass = mt - FUEL_CONST * time
    return mass if mass > 0.0 else 0.0


def velocity(fuel_mass, stage, v0):
    const_mass = MP + (STAGES_COUNT - stage + LAMBDA) * STAGE_MASS
    m0 = const_mass + (1 - LAMBDA) * STAGE_MASS
    return v0 + U * math.log(m0 / (fuel_mass + const_mass))


MT = (1 - LAMBDA) * STAGE_MASS
STAGE_TIME = int(MT / FUEL_CONST)
t_list = numpy.arange(0, STAGES_COUNT * STAGE_TIME)
v_list = []
changes = []
stage = 1
v0 = 0
time_shift = 0
i = 0
while i < len(t_list):
    fuel_mass = fuel(MT, t_list[i] - time_shift)
    if fuel_mass != 0:
        v_list.append(velocity(fuel_mass, stage, v0))
        i += 1
        continue
    time_shift = stage * STAGE_TIME
    stage += 1
    v0 = max(v_list)
    changes.append(t_list[i])

pyplot.plot(t_list, v_list)
for t in changes:
    pyplot.plot([t, t], [min(v_list), max(v_list)], "r--")
pyplot.xlabel("Time")
pyplot.ylabel("Velocity")
pyplot.title("m0 = {:.2f} kg, v_max = {:.2f} km/s"
             .format(M0, max(v_list) / 1000))
pyplot.show()
