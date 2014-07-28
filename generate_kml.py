#!/usr/bin/python

from xml.dom.minidom import parse, Document
from yaml import load
import sys
dom = Document()

def text_element(name, text, cdata=False):
    if text is None:
        text = ''
    d = dom.createElement(name)
    if cdata:
        d.appendChild( dom.createCDATASection(text) )
    else:
        d.appendChild( dom.createTextNode(text.encode('utf-8')) )
    return d

def create_folder(name, data):
    f = dom.createElement('Folder')
    f.appendChild( text_element('name', name))
    for place in data:
        p = dom.createElement('Placemark')
        p.appendChild( text_element('name', place['name']))
        
        edata = dom.createElement('ExtendedData')
        data = dom.createElement('Data')
        data.setAttribute('name', 'type')
        data.appendChild( text_element('value', place['type']) )
        edata.appendChild(data)
        p.appendChild(edata)
        
        point = dom.createElement('Point')
        p.appendChild(point)
        point.appendChild( text_element('coordinates', place.get('latlong', '')))
        
        f.appendChild(p)
    
    return f

root = dom.createElement("kml")
root.setAttribute('xmlns', 'http://www.opengis.net/kml/2.2')
dom.appendChild(root)
document = dom.createElement("Document")
root.appendChild(document)
document.appendChild( text_element('name', 'ROS Users of the World') )
document.appendChild( text_element('description', 'ROS Users of the World', True) )
document.appendChild( create_folder('ROS Users', load(open(sys.argv[1]))) )



print dom.toprettyxml()
