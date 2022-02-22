from simglucose.controller.base import Controller
from simglucose.controller.base import Action
from simglucose.simulation.scenario import Scenario

import numpy as np
import pandas as pd
import pkg_resources
import logging
import json
from collections import namedtuple
from datetime import timedelta 
import time as t
import datetime
from json.decoder import JSONDecodeError



Action = namedtuple('ctrller_action', ['basal', 'bolus'])
logger = logging.getLogger(__name__)
CONTROL_QUEST = pkg_resources.resource_filename(
    'simglucose', 'params/Quest.csv')
PATIENT_PARA_FILE = pkg_resources.resource_filename(
    'simglucose', 'params/vpatient_params.csv')
#OPEN_APS_PATH = "~/myopenaps/"


class MyApsController(Controller):

    def __init__(self, patient, start_time, noise,scen,delay):
        self.quest = pd.read_csv(CONTROL_QUEST)
        self.patient_params = pd.read_csv(
            PATIENT_PARA_FILE)
        self.noise = noise
        self.scenario=scen
        self.patient = patient
        self.start_time = start_time
        self.delay=delay
    def aps(self,CGM,time):
        self.time=time
        t0=time
        try:
            with open("/root/myopenaps/monitor/glucose.json") as data1_file:
                 data1=json.load(data1_file)
        except JSONDecodeError as e:
            print(e)
            t.sleep(0.5)
            with open("/root/myopenaps/monitor/glucose.json") as data1_file:
                 data1=json.load(data1_file)
        t1=data1[0].get("dateString")
        t2=t1[:-1]
        try:
            t3=datetime.datetime.strptime(t2,'%Y-%m-%dT%H:%M:%S.%f')
        except ValueError as v:
            print(v)
            t.sleep(0.5)
            t1=data1[0].get("dateString")
            t2=t1[:-1]
            t3=datetime.datetime.strptime(t2,'%Y-%m-%dT%H:%M:%S.%f')
            
            
       
        t4=datetime.datetime.now()
        t5=t4-t3
        t6=self.start_time
        t7=t6-t3
        t8=t5.total_seconds()
        t9=t7.total_seconds()
        

        while t9<0 and t8<300:
            print(t4)
            t.sleep(5)
            return self.aps(CGM,time)
            if t9>0 or t8==300 or t8>300:
                
                break
        
        print(t0.isoformat() + " is time from CGM")
        t10=datetime.datetime(2020,11,22,20,44,43,0, None)
        timedelta=t4-t10
        minutes=timedelta.total_seconds()/60
        a=minutes/5*300062+1606074283338-25*300062
        try:
            with open("/root/myopenaps/monitor/glucose.json") as data1_file:
                 data1=json.load(data1_file)
        except JSONDecodeError as e:
            print(e)
            t.sleep(0.5)
            with open("/root/myopenaps/monitor/glucose.json") as data1_file:
                 data1=json.load(data1_file)
        b= int(round(CGM,0))-data1[0].get("glucose")
       
        if -5 < b < 5:
            c= "Flat"
            d=4
        if 5 < b < 10 or b==5: 
            c="FortyFiveUp"
            d=3
        if -5 > b > -10 or b==-5:
            c="FortyFiveDown"
            d=5
        if 10 < b < 15 or b==10:
            c="SingleUp"
            d=2
        if -10 > b > -15 or b==-10:
            c="SingleDown"
            d=6
        if b > 15 or b==15:
            c="DoubleUp"
            d=1
        if b < -15 or b==-15:
            c="DoubleDown"
            d=7
            
        if (t0-t6).total_seconds()<300:
            entry1= {
            "direction":c,
            "noise": self.noise,
            "dateString":t4.isoformat() + "Z" ,
            "sgv":int(round(CGM,0)) ,
            "device": "8GGD7E",
            "filtered": 0,
            "date":a, 
            "unfiltered": 0,
            "rssi": -80,
            "type": "sgv",
            "glucose": int(round(CGM,0))}
        
            json_object=json.dumps([entry1], indent=11)
            
            try:
                with open("/root/myopenaps/nightscout/recent-missing-entries.json","w") as outfile7:
                     outfile7.write(json_object)
            except JSONDecodeError as e:
                print(e)
                t.sleep(0.5)
                with open("/root/myopenaps/nightscout/recent-missing-entries.json","w") as outfile7:
                     outfile7.write(json_object)
            
    
            try:
                
            
                with open("/root/myopenaps/monitor/glucose.json","w") as outfile6:
                     outfile6.write(json_object)
            except JSONDecodeError as e:
                print(e)
                t.sleep(0.5)
                with open("/root/myopenaps/monitor/glucose.json","w") as outfile6:
                     outfile6.write(json_object)
            try:
            
                with open("/root/Desktop/xdrip.glucose.json","w") as outfile5:
                     outfile5.write(json_object)
            except JSONDecodeError as e:
                print(e)
                t.sleep(0.5)
                with open("/root/Desktop/xdrip.glucose.json","w") as outfile5:
                     outfile5.write(json_object)
        else:
            
            entry1= {
            "direction":c,
            "noise": self.noise,
            "dateString":t4.isoformat() + "Z" ,
            "sgv":int(round(CGM,0)) ,
            "device": "8GGD7E",
            "filtered": 0,
            "date":a, 
            "unfiltered": 0,
            "rssi": -80,
            "type": "sgv",
            "glucose": int(round(CGM,0))}
        
            json_object=json.dumps(entry1, indent=11)
            json_object1=json.dumps([entry1], indent=11)
            
            try:
                with open("/root/myopenaps/nightscout/recent-missing-entries.json","w") as outfile7:
                     outfile7.write(json_object)
            except JSONDecodeError as e:
                print(e)
                t.sleep(0.5)
                with open("/root/myopenaps/nightscout/recent-missing-entries.json","w") as outfile7:
                     outfile7.write(json_object)

            try:
            
               with open("/root/Desktop/glucose.json","w") as outfile2:
                    outfile2.write(json_object)
            except JSONDecodeError as e:
               print(e)
               t.sleep(0.5)
               with open("/root/Desktop/glucose.json","w") as outfile2:
                    outfile2.write(json_object)
        
            try:
            
                with open("/root/Desktop/xdrip.glucose.json","r") as data3_file:
                
                    old_data3= json.load(data3_file)
            except JSONDecodeError as e:
               print(e)
               t.sleep(0.5)
               with open("/root/Desktop/xdrip.glucose.json","r") as data3_file:
                    old_data3= json.load(data3_file)
            try:
               with open("/root/Desktop/glucose.json","r") as data4_file:
                    new_data4= json.load(data4_file)
                    old_data3.insert(0, new_data4)
            except JSONDecodeError as e:
                    print(e)
                    t.sleep(0.5)
                    with open("/root/Desktop/glucose.json","r") as data4_file:
                         new_data4= json.load(data4_file)
                         old_data3.insert(0, new_data4)
            try:
                    with open("/root/Desktop/xdrip.glucose.json","w") as outfile5:
                         json.dump (old_data3, outfile5)
            except JSONDecodeError as e:
                   print(e)
                   t.sleep(0.5)
                   with open("/root/Desktop/xdrip.glucose.json","w") as outfile5:
                        json.dump (old_data3, outfile5)
    
            try:
                   with open("/root/myopenaps/monitor/glucose.json","r") as data6_file:
                        old_data6=json.load(data6_file)
                        old_data6.insert(0, new_data4)
            except JSONDecodeError as e:
                   print(e)
                   t.sleep(0.5)
                   with open("/root/myopenaps/monitor/glucose.json","r") as data6_file:
                        old_data6=json.load(data6_file)
                        old_data6.insert(0, new_data4)
            try:
                   with open("/root/myopenaps/monitor/glucose.json","w") as outfile7:  
                        json.dump (old_data6, outfile7)
            except JSONDecodeError as e:
                   print(e)
                   t.sleep(0.5)
                   with open("/root/myopenaps/monitor/glucose.json","w") as outfile7:  
                        json.dump (old_data6, outfile7)

        entry2= {
        "device": "8GGD7E",
        "date":a,
        "dateString":t4.isoformat() + "Z" ,
        "sgv":int(round(CGM,0)) ,
        "direction":c,
        "type": "sgv",
        "filtered": 0,
        "unfiltered": 0,
        "rssi": -80,
        "noise": self.noise,
        "trend": d,
        "state": "OK",
        "status": "OK",
        "glucose": int(round(CGM,0))}
        entry= [entry2]
        
        
        json_object=json.dumps(entry, indent=14)
        try:
            with open("/root/myopenaps/monitor/xdripjs/entry-xdrip.json","w") as outfile8:
                 outfile8.write(json_object)
        except JSONDecodeError as e:
            print(e)
            t.sleep(0.5)
            with open("/root/myopenaps/monitor/xdripjs/entry-xdrip.json","w") as outfile8:
                 outfile8.write(json_object)
        
        try:
            with open("/root/myopenaps/monitor/xdripjs/last-entry.json","w") as outfile9:
                 outfile9.write(json_object)
        except JSONDecodeError as e:
            print(e)
            t.sleep(0.5)
            with open("/root/myopenaps/monitor/xdripjs/last-entry.json","w") as outfile9:
                 outfile9.write(json_object)
        try:
            with open("/root/myopenaps/monitor/xdripjs/entry-xdrip.json","r") as data10_file:
                 new_data10= json.load(data10_file)
                 new_data10a=new_data10[0]
        except JSONDecodeError as e:
            print(e)
            t.sleep(0.5)
            with open("/root/myopenaps/monitor/xdripjs/entry-xdrip.json","r") as data10_file:
                 new_data10= json.load(data10_file)
                 new_data10a=new_data10[0]
                 
        if (t0-t6).total_seconds()<300:
            entry=[]
            json_object=json.dumps(entry, indent=0)
            try:
                 with open("/root/Desktop/entry1.json","w") as outfile12:
                      outfile12.write(json_object)
            except JSONDecodeError as e:
                 print(e)
                 t.sleep(0.5)
                 with open("/root/Desktop/entry1.json","w") as outfile12:
                      joutfile12.write(json_object)
            
            try:
                 with open("/root/Desktop/entry1.json","r") as data11_file:
                      old_data11= json.load(data11_file)
                      old_data11.insert(0, new_data10a)
            except JSONDecodeError as e:
                 print(e)
                 t.sleep(0.5)
                 with open("/root/Desktop/entry1.json","r") as data11_file:
                      old_data11= json.load(data11_file)
                      old_data11.insert(0, new_data10a)
            try:
                 with open("/root/Desktop/entry1.json","w") as outfile13:
                      json.dump (old_data11, outfile13)
            except JSONDecodeError as e:
                print(e)
                t.sleep(0.5)
                with open("/root/Desktop/entry1.json","w") as outfile13:
                     json.dump (old_data11, outfile13)
        else:
            try:
                 with open("/root/Desktop/entry1.json","r") as data11_file:
                      old_data11= json.load(data11_file)
                      old_data11.insert(0, new_data10a)
            except JSONDecodeError as e:
                 print(e)
                 t.sleep(0.5)
                 with open("/root/Desktop/entry1.json","r") as data11_file:
                      old_data11= json.load(data11_file)
                      old_data11.insert(0, new_data10a)
            try:
                 with open("/root/Desktop/entry1.json","w") as outfile13:
                      json.dump (old_data11, outfile13)
            except JSONDecodeError as e:
                print(e)
                t.sleep(0.5)
                with open("/root/Desktop/entry1.json","w") as outfile13:
                     json.dump (old_data11, outfile13)
            
        try:
             with open("/root/Desktop/entry1.json","r") as data13_file:
                  data13=json.load(data13_file)
                  data13a=data13[1:4]
                  data13b=data13[5:9]
        except JSONDecodeError as e:
            print(e)
            t.sleep(0.5)
            with open("/root/Desktop/entry1.json","r") as data13_file:
                  data13=json.load(data13_file)
                  data13a=data13[1:4]
                  data13b=data13[5:9]
        if len(data13)<4:
            try:
                  with open("/root/myopenaps/monitor/xdripjs/last15minutes.json","w") as outfile14:
                       outfile14.write(json_object)
            except JSONDecodeError as e:
                  print(e)
                  t.sleep(0.5)
                  with open("/root/myopenaps/monitor/xdripjs/last15minutes.json","w") as outfile14:
                        outfile14.write(json_object)
        else:  
        

            try:
                  with open("/root/myopenaps/monitor/xdripjs/last15minutes.json","w") as outfile14:
                       json.dump(data13a, outfile14)
            except JSONDecodeError as e:
                  print(e)
                  t.sleep(0.5)
                  with open("/root/myopenaps/monitor/xdripjs/last15minutes.json","w") as outfile14:
                       json.dump(data13a, outfile14)
        if len(data13)<8:
            try:
                  with open("/root/myopenaps/monitor/xdripjs/last41minutes.json","w") as outfile15:
                       outfile15.write(json_object)
            except JSONDecodeError as e:
                  print(e)
                  t.sleep(0.5)
                  with open("/root/myopenaps/monitor/xdripjs/last41minutes.json","w") as outfile15:
                       outfile15.write(json_object)
        
        else:
        
        
              try:
                  with open("/root/myopenaps/monitor/xdripjs/last41minutes.json","w") as outfile15:
                       json.dump(data13b, outfile15)
              except JSONDecodeError as e:
                  print(e)
                  t.sleep(0.5)
                  with open("/root/myopenaps/monitor/xdripjs/last41minutes.json","w") as outfile15:
                       json.dump(data13b, outfile15)

    def policy(self, observation, reward, done, **kwargs):
        
        sample_time = kwargs.get('sample_time', 1)
        pname = kwargs.get('patient_name')
        meal = kwargs.get('meal')
        self.aps(observation.CGM,self.start_time + timedelta(minutes=self.patient.t))
        
       
        action = self._bb_policy(
            pname,
            meal,
            observation.CGM,
            sample_time)
        return action
        

   
    def _bb_policy(self,name, meal, CGM, env_sample_time):
        
        t0=self.time
        print(t0)
        t1=self.start_time
        timedelta=t0-t1
        T=timedelta.total_seconds()
        print(T)
        scenario=dict(self.scenario)
        print(scenario)
        scenario_keys=list(scenario.keys())
        scenario_values=list(scenario.values())
        scenario_time=self.time+datetime.timedelta(minutes=self.delay)
        print(scenario_time)
        print(int(round(CGM,0)))     
        
        if T<1 and int(round(CGM,0))>140:
            bolus= 2.2 #Correction
         
        elif int(round(CGM,0))>70 and any ((scenario_time-x).total_seconds()==0 or 0<(scenario_time-x).total_seconds()<5 for x in scenario_keys):
            index=scenario_keys.index([x for x in scenario_keys if (scenario_time-x).total_seconds()==0 or 0<(scenario_time-x).total_seconds()<5][0])
            print(index)
            meal=scenario_values[index]
            print(meal)
            target=80
            quest = self.quest[self.quest.Name.str.match(name)]
            logger.info('Calculating bolus ...')
            bolus1= (meal / quest.CR.values+(int(round(CGM,0)) - target) / quest.CF.values).item()
            if int(round(CGM,0))>150:
                bolus2=bolus1/2
            else:
                bolus2=bolus1#+1
                
            #print(bolus1)
            #bolus2=bolus1#+1
            print(bolus2)
            bolus=bolus2/env_sample_time
            print(env_sample_time)
        else:
            bolus=0
        print(bolus)
        
        try:
            
            with open('/root/myopenaps/monitor/temp_basal.json') as data22_file:
                
                data22=json.load(data22_file)
        except JSONDecodeError as e:
            print(e)
            t.sleep(0.5)
            with open('/root/myopenaps/monitor/temp_basal.json') as data22_file:
                
                data22=json.load(data22_file)
        try:
            
            with open("/root/myopenaps/monitor/status.json") as data23_file:
                 data23=json.load(data23_file)
        except JSONDecodeError as e:
            print(e)
            t.sleep(0.5)
            with open("/root/myopenaps/monitor/status.json") as data23_file:
                 data23=json.load(data23_file)

           
        if  bolus==0 and data22.get("duration")> 0 and data22.get("temp")== "absolute" and data23.get("suspended")== False and 900<T:
            x=data22.get("rate")
            basal= x/60. # rate in minutes instead of hours
        else:
           basal=0
        print(basal)
        #try:  
         #   with open('/root/myopenaps/settings/basal_profile.json') as data24_file:
          #      
           #   data24=json.load(data24_file)
        #except JSONDecodeError as e:
         #     print(e)
          #    t.sleep(0.5)
           #   with open('/root/myopenaps/settings/basal_profile.json') as data24file:
            #    
             #       data24=json.load(data24_file)
        #for i in data24:
         #   if ((datetime.datetime.strptime(i.get('start'), '%H:%M:%S').strftime('%H'))
          #  ==t0.strftime('%H')):
           #       basal1=i.get('rate')
        #if bolus==0:
         #  basal=basal1/60
        #else:
         #   basal=0

        #print(basal)
        action = Action(basal=basal, bolus=bolus)
        
        
        return action
        

    def reset(self):
        pass

if __name__ == '__main__':
    ctrller = MyApsController()