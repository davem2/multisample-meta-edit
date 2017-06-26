#!/usr/bin/env python3

VERSION="0.1.0" # MAJOR.MINOR.PATCH | http://semver.org

import zipfile
import xml.etree.ElementTree as etree
import tempfile
import shutil
import os
import argparse

#TODO: allow individual fields to be set through command line arguments, --xml= arg for current method

def parse_commandline():
    parser = argparse.ArgumentParser(prog='sfz2bitwig', description='Edit Bitwig multisample instrument metadata.')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s v{0}'.format(VERSION))
    parser.add_argument('file', nargs='+', help='multisample file(s) to modify')
    parser.add_argument('-x', '--xml', help='xml data to write')
    parser.add_argument('-m', '--merge', action='store_true', help='merge xml with existing')
    parser.add_argument('--noloop', default=False, action='store_true', help='disable wav loop point extraction')

    return parser.parse_args()


def main():
    args = parse_commandline()

    # Parse new metadata to be written
    with open(args.xml) as f:
        data = f.read()
    xml = etree.fromstring("<root>\n{}</root>".format(data))
    #etree.dump(xml)

    newdata = {}
    newdata['category'] = gettagvalue('category')
    newdata['creator'] = gettagvalue('creator')
    newdata['description'] = gettagvalue('description')
    newdata['keywords'] = []
    for k in xml.findall('keywords/keyword'):
        newdata['keywords'].append(k.text)
    #print(newdata)


    # Write new metadata to multisample file(s)
    for fn in args.file:
        xml = readmultisamplexml(fn)

        if newdata['category']:
            xml.find('category').text = newdata['category']
        if newdata['creator']:
            xml.find('creator').text = newdata['creator']
        if newdata['description']:
            xml.find('description').text = newdata['description']

        if len(newdata['keywords']) > 0:
            #TODO: add other combination rules instead of just overwrite for keywords
            #if overwrite:
            parent = xml.find('keywords')
            for keyword in parent.findall('keyword'):
                if args.merge:
                    if keyword.text in newdata['keywords']:
                        print("removing {}".format(keyword))
                        parent.remove(keyword)
                else:
                    parent.remove(keyword)

            for word in newdata['keywords']:
                child = etree.SubElement(parent,'keyword')
                child.text = word

        delete_from_zip(fn,'multisample.xml')
        writemultisamplexml(fn,xml)

    return


def gettagvalue(tag=None):
    try:
        value = xml.find(tag).text
    except:
        value = ''

    return value


def readmultisamplexml(fn=None):
    zf = zipfile.ZipFile(fn,mode='r',compression=zipfile.ZIP_DEFLATED)
    try:
        xml = zf.read('multisample.xml')
        tree = etree.fromstring(xml)
    finally:
        zf.close()

    return tree


def writemultisamplexml(fn=None,xml=None):
    zf = zipfile.ZipFile(fn,mode='a',compression=zipfile.ZIP_DEFLATED)
    try:
        zf.writestr('multisample.xml',etree.tostring(xml))
    finally:
        zf.close()


def delete_from_zip(zipfn=None, *filenames):
    tempdir = tempfile.mkdtemp()
    try:
        tempname = os.path.join(tempdir, 'new.zip')
        with zipfile.ZipFile(zipfn, 'r') as zipread:
            with zipfile.ZipFile(tempname, 'w') as zipwrite:
                for item in zipread.infolist():
                    if item.filename not in filenames:
                        data = zipread.read(item.filename)
                        zipwrite.writestr(item, data)
        shutil.move(tempname, zipfn)
    finally:
        shutil.rmtree(tempdir)


if __name__ == "__main__":
    main()


