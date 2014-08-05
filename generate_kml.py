#!/usr/bin/python

from xml.dom.minidom import parse, Document
from yaml import load
from os.path import split, splitext
import sys, urllib2
dom = Document()

STYLES = {'school': '44AF62', 'company': 'F08641', 'other': '5EDDFF', None: 'FFFFFF', 'research institute': '3644DB'}

REGIONS = ['america', 'asia', 'australia', 'europe']
PATTERN = 'https://raw.githubusercontent.com/DLu/ros_map/master/data/%s.yaml'


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
        tipo = place.get('type', None)
        if tipo == 'null' or tipo not in STYLES:
            tipo = None

        p.appendChild( text_element('styleUrl', '#%s'%str(tipo)))
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
            d.appendChild( dom.createCDATASection(place['description'].encode('utf-8')) )
            p.appendChild(d)
        
        point = dom.createElement('Point')
        p.appendChild(point)
        if 'lat' in place:
            coordinates = '%f,%f,0.0'%( place['long'], place['lat'])
            point.appendChild( text_element('coordinates', coordinates))

        f.appendChild(p)
    
    return f

def create_style(name, color, url='http://www.gstatic.com/mapspro/images/stock/959-wht-circle-blank.png'):
    f = dom.createElement('Style')
    f.setAttribute('id', str(name))
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

files = [arg for arg in sys.argv[1:] if 'yaml' in arg]
kml = [arg for arg in sys.argv[1:] if 'kml' in arg]

if len(files)==0:
    for region in REGIONS:
        key = region.capitalize()
        url = PATTERN % region
        stream = urllib2.urlopen(url)
        document.appendChild( create_folder('ROS Users (%s)'%key, load(stream)) )
else:
    for fn in files:
        document.appendChild( create_folder(fn, load(open(fn))))

for style, color in STYLES.iteritems():
    document.appendChild( create_style(style, color) )

if len(kml)>0:
    f = open(kml[0], 'w')
    f.write(dom.toprettyxml())
    f.close()
else:
    print "Content-type: text/xml"
    print 
    print dom.toprettyxml() 

