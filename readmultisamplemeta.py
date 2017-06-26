#!/usr/bin/env python3

VERSION="0.1.0" # MAJOR.MINOR.PATCH | http://semver.org

import zipfile
import xml.etree.ElementTree as etree
import argparse

def parse_commandline():
    parser = argparse.ArgumentParser(prog='readmultisamplemeta', description='Extracts metadata from a Bitwig multisample instrument.')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s v{0}'.format(VERSION))
    parser.add_argument('file', nargs='+', help='multisample file(s) to read')
    #TODO.. more formats? json,csv? allow user to extract one field?

    return parser.parse_args()


def main():
    args = parse_commandline()

    for fn in args.file:
        xml = readmultisamplexml(fn)
        #etree.dump(xml)
        if len(args.file) > 1:
            print("\n{}:\n-------------------------------".format(fn))

        dumpelement(xml,'category')
        dumpelement(xml,'creator')
        dumpelement(xml,'description')
        dumpelement(xml,'keywords')

    return


def dumpelement(xml=None,xpath=None):
    elem = xml.findall(xpath)
    for e in elem:
        #empty
        if not e.text and len(list(e)) == 0:
            print("<{}/>".format(e.tag))
        #children
        elif len(list(e)) > 0:
            print("<{}>".format(e.tag))
            for c in list(e):
                print("  <{}>{}</{}>".format(c.tag,c.text,c.tag))
            print("</{}>".format(e.tag))
        #normal
        else:
            print("<{}>{}</{}>".format(e.tag,e.text,e.tag))


def readmultisamplexml(fn=None):
    zf = zipfile.ZipFile(fn,mode='r',compression=zipfile.ZIP_DEFLATED)
    try:
        xml = zf.read('multisample.xml')
        tree = etree.fromstring(xml)
    finally:
        zf.close()

    return tree

#def writexml(fn=None,xml=None):
#    zf = zipfile.ZipFile(fn,mode='w',compression=zipfile.ZIP_DEFLATED)
#    try:
#        zf.writestr('multisample.xml',xml.tostring())
#    finally:
#        zf.close()

if __name__ == "__main__":
    main()

#multisample metadata format
#
#   <category>Mallets</category>
#   <creator>Genys</creator>
#   <description><description/>
#   <keywords>
#      <keyword>acoustic</keyword>
#      <keyword>clean</keyword>
#   </keywords>
#
#    ... other stuff?
#
#multisample metadata format
#
#   <category>Mallets</category>
#   <creator>Genys</creator>
#   <description><description/>
#   <keywords>
#      <keyword>acoustic</keyword>
#      <keyword>clean</keyword>
#   </keywords>
#
#    ... other stuff?
#
#
#
#tree = etree.parse('input.xml')
#for elem in tree.findall('//tag-Name'):
#    if elem.text == 'oldName':
#        elem.text = 'newName'
## some output options for example
#tree.write('output.xml', encoding='utf-8', xml_declaration=True)
