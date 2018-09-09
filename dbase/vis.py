#!/usr/bin/env python
import geojson # write geojson
import glob
import json
import matplotlib.pyplot as plt
from descartes import PolygonPatch

path_data = '/Users/nico/Code/ProyectoInmobiliario/data/geo/chile/'

def vis_polygon(ax,type,region,commune):

    path = path_data+'{}/json/{}/'.format(type,region)

    if not isinstance(commune,list):
        communes = [commune]

    filenames = []
    for commune in communes:
        filenames += glob.glob(path+'{}*'.format(commune))

    for filename in filenames:
        print(filename[-20:])
        file = open(filename,'r')
        json_data = json.load(file)

        poly = json_data['geometry']
        BLUE = '#cccccc'

        ax.add_patch(PolygonPatch(poly, fc=BLUE, ec='#000000', lw=0.2, zorder=2))
        ax.axis('scaled')


def vis_manzana(ax,commune=""):
    vis_polygon(ax,'manzanas','metropolitana-de-santiago',commune)

def vis_areasverde(ax,commune=""):
    vis_polygon(ax,'areasverde','metropolitana-de-santiago',commune)

fig = plt.figure()
ax = fig.gca()

#vis_manzana(ax,commune="providencia")
vis_areasverde(ax,commune="providencia")

plt.show()
