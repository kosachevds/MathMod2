import math
import numpy
from matplotlib import pyplot

U = 3000.0
LAMBDA = 0.1
MP = 42.0
V = 9000.0


def velocity(start_velocity, stage, masses, fuel_mass):
    start_mass = MP + sum(masses[stage - 1:])
    current_mass = start_mass - masses[stage - 1] * (1 - LAMBDA) + fuel_mass
    return start_velocity + U * math.log(start_mass / current_mass)


def get_alpha(v, stages_count):
    p = math.exp(-v / (stages_count * U))
    return (1 - LAMBDA) / (p - LAMBDA)


def get_stages_masses(mp, v, stages_count):
    alpha = get_alpha(v, stages_count)
    m0 = mp * alpha ** stages_count
    m1 = m0 * (1 - 1 / alpha)
    m2 = m0 / alpha - mp * alpha
    m3 = (alpha - 1) * mp
    return [m1, m2, m3]


m0_list = [MP * get_alpha(V, x) ** x for x in range(2, 10)]
pyplot.figure(1)
pyplot.plot(range(2, 10), m0_list, "bo", linestyle="dashed")
pyplot.xlabel("stages")
pyplot.ylabel("start mass")
pyplot.title("mp = {}, v = {}km/s".format(MP, V / 1000))

STAGES_COUNT = 3
stages = get_stages_masses(MP, V, STAGES_COUNT)
fuel_masses = [(1 - LAMBDA) * mass for mass in stages]
stage = 1
f_list = numpy.arange(sum(fuel_masses), 0, -1)
v_list = []
previous_v = 0
for f in f_list:
    stage_fuel = f - sum(fuel_masses[stage:])
    if stage_fuel > 0.0:
        v_list.append(velocity(previous_v, stage, stages, stage_fuel))
    else:
        v_list.append(velocity(previous_v, stage, stages, 0.0))
        stage += 1
        previous_v = max(v_list)
pyplot.figure(2)
pyplot.plot(list(reversed(f_list)), v_list)
for f in [fuel_masses[0], sum(fuel_masses[:2])]:
    pyplot.plot([f, f], [min(v_list), max(v_list)], "r--")
pyplot.xlabel("fuel mass")
pyplot.ylabel("velocity")
pyplot.title("v_max = {:.2f}km/s, ".format(max(v_list) / 1000))
pyplot.show()
