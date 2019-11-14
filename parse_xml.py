import xml.etree.ElementTree as ET
import re
import json

labels = []
mark = []
for i in range(13002):
    labels.append([])
    mark.append(0)
for xi in range(1):
    name = "26_poliseg0.xml"
    tree = ET.parse(name)
    root = tree.getroot()
    offset = xi*1800
    print(offset)
  
    for neighbor in root.iter('track'):
        print (neighbor.attrib)
        print (neighbor.get('label'))
        for child in neighbor:
            if child.get('occluded')=='0':
                
                entry = {}
              #  box2d = {}
              #  box2d['x1'] = child.get('xtl')
              #  box2d['x2'] = child.get('xbr')
               # box2d['y1'] = child.get('ytl')
               # box2d['y2'] = child.get('ybr')
              #  entry['box2d']=box2d
                mark[int(child.get('frame'))] = 1
for i in range(755):
	if mark[i]==0:
		print(i)



