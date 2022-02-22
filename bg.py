from simglucose.simulation.env import T1DSimEnv
from en import MyApsController
from simglucose.sensor.cgm import CGMSensor
from simglucose.actuator.pump import InsulinPump
#from RealTimet1dpatient import RealTimeT1DPatient
from simglucose.patient.t1dpatient import T1DPatient
from simglucose.simulation.scenario_gen import RandomScenario
from simglucose.simulation.scenario import CustomScenario
from simglucose.simulation.sim_engine import SimObj, sim, batch_sim
from datetime import timedelta
from datetime import datetime
import time as t




# specify start_time as the beginning of today
now = datetime.now()
start_time = datetime.combine(now.date(),now.time())
print(start_time.isoformat())
# --------- Create Random Scenario --------------
# Specify results saving path
path = '/home/pi/Desktop/results'

#Create a simulation environment
#patient = T1DPatient.withName('adolescent#002')
#sensor = CGMSensor.withName('GuardianRT', seed=1)
#pump = InsulinPump.withName('Insulet')
#scenario = RandomScenario(start_time=start_time, seed=1)
#env = T1DSimEnv(patient, sensor, pump, scenario)

# Create a controller
#controller = MyApsController(patient, start_time, sensor.seed,scenario)

# Put them together to create a simulation object
#s1 = SimObj(env, controller, timedelta(days=2), animate=True, path=path)
#results1 = sim(s1)
#print(results1)

# Create a simulation environment
patient = T1DPatient.withName('adult#001')
sensor = CGMSensor.withName('GuardianRT', seed=1)
pump = InsulinPump.withName('Insulet')
scen = [(now+timedelta(hours=3), 60), (now+timedelta(hours=6), 15), (now+timedelta(hours=8), 20), (now+timedelta(hours=17), 25), (now+timedelta(hours=20), 80)]
scenario = CustomScenario(start_time=start_time, scenario=scen)
env = T1DSimEnv(patient, sensor, pump, scenario)
delay=0
controller = MyApsController(patient, start_time, sensor.seed,scen,delay)

#Put them together to create a simulation object
s2 = SimObj(env, controller, timedelta(days=1), animate=True, path=path)
results2 = sim(s2)
print(results2)