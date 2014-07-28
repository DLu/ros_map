#!/usr/bin/python

from xml.dom.minidom import parse, Document
from yaml import load
from os.path import split, splitext
import sys
dom = Document()

STYLES = {'school': '#icon-959-62AF44', 'company': '#icon-959-4186F0', 'other': '#icon-959-FFDD5E'}
DEFAULT_STYLE = '#icon-959-FFFFFF'

def text_element(name, text, cdata=False):
    if text is None:
        text = ''
    d = dom.createElement(name)
    if cdata:
        d.appendChild( dom.createCDATASection(text) )
    else:
        d.appendChild( dom.createTextNode(text.encode('utf-8')) )
    return d

def data_element(name, value):
    data = dom.createElement('Data')
    data.setAttribute('name', name)
    data.appendChild( text_element('value', value) )
    return data

def create_folder(name, data):
    f = dom.createElement('Folder')
    f.appendChild( text_element('name', name))
    for place in data:
        p = dom.createElement('Placemark')
        style = STYLES.get(place['type'], DEFAULT_STYLE)
        p.appendChild( text_element('styleUrl', style))
        p.appendChild( text_element('name', place['name']))
        
        edata = dom.createElement('ExtendedData')
        edata.appendChild( data_element('type', place['type']) )
        if 'link' in place:
            edata.appendChild( data_element('gx_media_links', place['link']) )

        p.appendChild(edata)

        if 'address' in place:
            p.appendChild( text_element('address', place['address']) )

        if 'description' in place:
            d = dom.createElement('description')
            d.appendChild( dom.createCDATASection(place['description']) )
            p.appendChild(d)
        
        point = dom.createElement('Point')
        p.appendChild(point)
        point.appendChild( text_element('coordinates', place.get('latlong', '')))
        
        f.appendChild(p)
    
    return f

def create_style(name, color, url='http://www.gstatic.com/mapspro/images/stock/959-wht-circle-blank.png'):
    f = dom.createElement('Style')
    f.setAttribute('id', name)
    p = dom.createElement('IconStyle')
    f.appendChild(p)
    p.appendChild( text_element('color', 'ff' + color) )
    p.appendChild( text_element('scale', '1.1') )
    i = dom.createElement('Icon')
    p.appendChild( i )
    i.appendChild( text_element('href', url) )
    return f

root = dom.createElement("kml")
root.setAttribute('xmlns', 'http://www.opengis.net/kml/2.2')
dom.appendChild(root)
document = dom.createElement("Document")
root.appendChild(document)
document.appendChild( text_element('name', 'ROS Users of the World') )
document.appendChild( text_element('description', 'ROS Users of the World', True) )
for arg in sys.argv[1:]:
    key = splitext( split(arg)[-1] )[0].capitalize()
    document.appendChild( create_folder('ROS Users (%s)'%key, load(open(arg))) )

document.appendChild( create_style('icon-959-4186F0', 'F08641') )
document.appendChild( create_style('icon-959-62AF44', '44AF62') )
document.appendChild( create_style('icon-959-FFDD5E', '5EDDFF') )
document.appendChild( create_style('icon-959-FFFFFF', 'FFFFFF') )

print dom.toprettyxml()

