from flask import Flask, render_template, request
app = Flask(__name__)
import numpy as np
import math
import pandas as pd
import requests
import json
from math import sin, cos, sqrt, atan2, radians

d = pd.read_csv('stops.txt')
y=d.values.tolist()
lat=[]
long=[]
name=[]
for i in range(len(y)):
    lat.append(y[i][3])
    long.append(y[i][4])
    name.append(y[i][2])
print(name)
stoplat=lat
stoplong=long
@app.route("/")
def index():
    
    return render_template("map.html",lat=lat,long=long)
@app.route('/map2',methods = ['POST', 'GET'])
def result():
   if request.method == 'POST':
      result = request.form
      la=[]
      validlat=[]
      validlong=[]
      validname=[]
      originlat=[]
      originlong=[]
      lo=[]
      latt =  request.form.getlist('Origin lat')
      la.append((latt[0]))
      latt =  request.form.getlist('Origin long')
      lo.append((latt[0]))
      latt =  request.form.getlist('Dest lat')
      la.append((latt[0]))
      latt =  request.form.getlist('Dest long')
      lo.append((latt[0]))
      print(la)
      print(lo)
      d=''
      R=6373.0
      lat=[0,0,0]
      lon=[0,0,0]
      dlon=[0,0,0]
      dlat=[0,0,0]
      a=[0,0,0]
      c=[0,0,0]
      distance=[0,0,0,0]
      response=requests.get("http://dev.virtualearth.net/REST/V1/Routes/Driving?wp.0="+str(la[0])+","+str(lo[0])+"&wp.1="+str(la[1])+","+str(lo[1])+"&optmz=time&ra=routePath&key=AkzkWEB4iMLDt8PfVNewJ4FEYlPf_FSJzf0MICjIm_qWp7BOSbVE-wnA6_qZHR3e")
      data = json.loads(response.text)
      #print(data)
 #     print(data["resourceSets"][0]["resources"][0]["routePath"]["line"]["coordinates"])
      j=len(data["resourceSets"][0]["resources"][0]["routePath"]["line"]["coordinates"]);
      for i in range(j):
            originlat.append(data["resourceSets"][0]["resources"][0]["routePath"]["line"]["coordinates"][i][0])
            originlong.append(data["resourceSets"][0]["resources"][0]["routePath"]["line"]["coordinates"][i][1])
      print(originlat)
      for i in range(len(originlat)-1): 
        for q in range(len(stoplat)):
            lat[0]=radians(originlat[i])
            lat[1]=radians(originlat[i+1])
            lon[0]=radians(originlong[i])
            lon[1]=radians(originlong[i+1])
            lat[2]=radians(stoplat[q])
            lon[2]=radians(stoplong[q])
            dlon[0]=lon[1]-lon[0]
            dlat[0]=lat[1]-lat[0]
            a[0] = sin(dlat[0] / 2)**2 + cos(lat[0]) * cos(lat[1]) * sin(dlon[0] / 2)**2
            c[0] = 2 * atan2(sqrt(a[0]), sqrt(1 - a[0]))
            distance[0] = R * c[0]
            
            
            
            dlon[1]=lon[2]-lon[0]
            dlat[1]=lat[2]-lat[0]
            a[1] = sin(dlat[1] / 2)**2 + cos(lat[0]) * cos(lat[2]) * sin(dlon[1] / 2)**2
            c[1] = 2 * atan2(sqrt(a[1]), sqrt(1 - a[1]))
            distance[1] = R * c[1]
    
        
            dlon[2]=lon[2]-lon[1]
            dlat[2]=lat[2]-lat[1]
            a[2] = sin(dlat[2] / 2)**2 + cos(lat[1]) * cos(lat[2]) * sin(dlon[0] / 2)**2
            c[2] = 2 * atan2(sqrt(a[2]), sqrt(1 - a[0]))
            distance[2] = R * c[2]
      
            distance[3]=distance[1]+distance[2]
            #print(distance[3]-distance[0])
            if(abs(distance[3]-distance[0]<=0.17)):
                validlat.append(stoplat[q])
                validlong.append(stoplong[q])
                validname.append(name[q])
      print(validlat)  
      return render_template("map2.html",originlat=originlat,originlong=originlong,validlat=validlat,validlong=validlong,validname=validname)
if __name__ == '__main__':
   app.run(debug = True)
''' from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("speech.html")

if __name__ == '__main__':
   app.run(debug = True)'''
 
 