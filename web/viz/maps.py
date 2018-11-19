from bokeh.models import GMapOptions
from bokeh.plotting import figure, show, ColumnDataSource, gmap
from bokeh.embed import components

import numpy as np

def mapReferences(references,realestate):
    map_options = GMapOptions(lat=realestate.lat, lng=realestate.lng, map_type="roadmap", zoom=13, scale_control=True)
    p = gmap("AIzaSyAKZ-wutxLGtqlojKj00BwHKFlH5dkr47c", map_options,plot_width=1000,plot_height=400)
    lat = np.array(references.values_list('lat',flat=True))
    lng = np.array(references.values_list('lng',flat=True))
    source = ColumnDataSource(data=dict(
        lat=lat,
        lon=lng)
    )
    p.circle(x='lon', y='lat', size=10, color="navy", source=source)
    source = ColumnDataSource(data=dict(
        lat=[realestate.lat],
        lon=[realestate.lng])
    )
    p.circle(x='lon', y='lat', size=10, color="red", source=source)
    script, div = components(p)
    return {'script':script,'div':div}