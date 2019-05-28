#!/usr/bin/python

from xml.dom.minidom import Document
import yaml
import argparse
import requests
dom = Document()

STYLES = {'school': '44AF62', 'company': 'F08641', 'other': '5EDDFF', None: 'FFFFFF', 'research institute': '3644DB'}

REGIONS = ['america', 'asia', 'australia', 'europe', 'africa']
PATTERN = 'https://raw.githubusercontent.com/DLu/ros_map/master/data/%s.yaml'


def text_element(name, text, cdata=False):
    if text is None:
        text = ''
    d = dom.createElement(name)
    if cdata:
        d.appendChild(dom.createCDATASection(text))
    else:
        d.appendChild(dom.createTextNode(text.encode('utf-8')))
    return d


def data_element(name, value):
    data = dom.createElement('Data')
    data.setAttribute('name', name)
    data.appendChild(text_element('value', value))
    return data


def create_folder(name, data, verbose=False):
    if verbose:
        print('===== %s =====' % name)
    f = dom.createElement('Folder')
    f.appendChild(text_element('name', name))
    for place in data:
        p = dom.createElement('Placemark')
        if verbose:
            if 'name' not in place:
                print('Field name not defined for the following entry:')
                print(yaml.dump(place))
            else:
                missing_keys = set(['lat', 'long', 'type']) - set(place.keys())
                if missing_keys:
                    print('Field(s) %s not defined for %s' % (', '.join(missing_keys), place['name']))
                elif not place['type'] or place['type'] not in STYLES:
                    print('Type %s not standard for %s' % (place['type'], place['name']))

                weird_keys = set(place.keys()) - set(['lat', 'long', 'name', 'type', 'link', 'description', 'address'])
                if weird_keys:
                    print('Weird key(s) %s for %s' % (', '.join(weird_keys), place['name']))


        tipo = place.get('type', None)
        if tipo == 'null' or tipo not in STYLES:
            tipo = None

        p.appendChild(text_element('styleUrl', '#%s' % str(tipo)))
        p.appendChild(text_element('name', place.get('name', '')))

        edata = dom.createElement('ExtendedData')
        edata.appendChild(data_element('type', tipo))
        if 'link' in place:
            edata.appendChild(data_element('gx_media_links', place['link']))

        p.appendChild(edata)

        if 'address' in place:
            p.appendChild(text_element('address', place['address']))

        if 'description' in place:
            d = dom.createElement('description')
            d.appendChild(dom.createCDATASection(place['description'].encode('utf-8')))
            p.appendChild(d)

        point = dom.createElement('Point')
        p.appendChild(point)
        if 'lat' in place:
            coordinates = '%f,%f,0.0' % (place['long'], place['lat'])
            point.appendChild(text_element('coordinates', coordinates))

        f.appendChild(p)

    return f


def create_style(name, color, url='http://maps.google.com/mapfiles/kml/pal2/icon18.png'):
    f = dom.createElement('Style')
    f.setAttribute('id', str(name))
    p = dom.createElement('IconStyle')
    f.appendChild(p)
    p.appendChild(text_element('color', 'ff' + color))
    p.appendChild(text_element('scale', '1.1'))
    i = dom.createElement('Icon')
    p.appendChild(i)
    i.appendChild(text_element('href', url))
    return f


root = dom.createElement("kml")
root.setAttribute('xmlns', 'http://www.opengis.net/kml/2.2')
dom.appendChild(root)
document = dom.createElement("Document")
root.appendChild(document)
document.appendChild(text_element('name', 'ROS Users of the World'))
document.appendChild(text_element('description', 'ROS Users of the World', True))

parser = argparse.ArgumentParser()
parser.add_argument('input_yaml', nargs='*')
parser.add_argument('-o', '--output')
parser.add_argument('-v', '--verbose', action='store_true')
args = parser.parse_args()

if len(args.input_yaml) == 0:
    for region in REGIONS:
        url = PATTERN % region
        resp = requests.get(url)
        document.appendChild(create_folder('ROS Users (%s)' % region.capitalize(), yaml.load(resp.text)))
else:
    for fn in args.input_yaml:
        document.appendChild(create_folder(fn, yaml.load(open(fn)), args.verbose))

for style, color in STYLES.iteritems():
    document.appendChild(create_style(style, color))

if args.output:
    with open(args.output, 'w') as f:
        f.write(dom.toprettyxml())
else:
    print("Content-type: text/xml")
    print()
    print(dom.toprettyxml())
