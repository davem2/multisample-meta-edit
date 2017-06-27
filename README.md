
## Description
Edit Bitwig Studio multisample instrument metadata

## Usage
### readmultisamplemeta
python readmultisamplemeta.py file.multisample
python readmultisamplemeta.py *.multisample
### writemultisamplemeta
python writemultisamplemeta.py --xml=data.xml file.multisample

data.xml:
```
<category>Note3</category>
<creator>Sfz2bitwig2</creator>
<description>test2</description>
<keywords>
    <keyword>dirty2</keyword>
    <keyword>noisy2</keyword>
</keywords>
```

