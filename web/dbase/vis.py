#!/usr/bin/env python
import glob
import json
import matplotlib.pyplot as plt
import matplotlib
from descartes import PolygonPatch
from matplotlib.patches import Circle

from tools import *

path_data = '/Users/nico/Code/ProyectoInmobiliario/data/geo/chile/'

def vis_polygon(ax,type,region,commune,color_type=''):

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
        if color_type == 'greenspace':
            greens = json_data['properties']['greenspace']
            factor = 0.0
            for green in greens:
                if green[1] != 0:
                    factor += green[0]/(green[1]*green[1])
            cmap = matplotlib.cm.get_cmap('viridis')
            color = cmap(factor/1.0)
        elif color_type == 'area':
            cmap = matplotlib.cm.get_cmap('viridis')
            area = json_data['properties']['area']
            if area > 0.00001:
                color = '#ff0000'
            else:
                color = '#00ff00'
        else:
            color = '#ffffff'

        poly = json_data['geometry']

        ax.add_patch(PolygonPatch(poly, fc=color, ec='#000000', lw=0.2, zorder=2))
        ax.add_patch(Circle(json_data['properties']['center'], radius=0.00005, fc='#000000', ec='#000000', lw=0.2, zorder=2))
        ax.axis('scaled')
        ax.set_xlabel('lng')
        ax.set_ylabel('lat')


def vis_manzana(ax,commune=""):
    vis_polygon(ax,'manzanas','metropolitana-de-santiago',commune,
        color_type='greenspace')

def vis_areasverde(ax,commune=""):
    vis_polygon(ax,'areasverde','metropolitana-de-santiago',commune,
        color_type='')

def vis_areasverde_distribution(ax,commune=""):
    greenspaces = loadGreenspaces(commune)
    areas = np.zeros(len(greenspaces))
    cap = 0.00001
    for i, gs in enumerate(greenspaces):
        if gs['properties']['area'] > cap:
                areas[i] = cap
        else:
            areas[i] = gs['properties']['area']
    plt.hist(areas)
    plt.yscale('log')

#fig = plt.figure()
#ax = fig.gca()

#vis_manzana(ax,commune="providencia")
#vis_areasverde(ax,commune="providencia")
#vis_areasverde_distribution(ax)
#vis_areasverde(ax,commune="providencia")

#plt.show()
