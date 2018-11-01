from django.shortcuts import render

from region.models import Region
from commune.models import Commune
from collections import OrderedDict
from realestate.models import RealEstate
from apartment.models import Apartment

from bokeh.models import CustomJS, TapTool, HoverTool
from bokeh.plotting import figure, output_file, show, ColumnDataSource
from bokeh.embed import components

import numpy as np

def vis(request):

    apts = Apartment.objects.only('lat','lng','name','addressStreet','addressNumber').all()
    lat = np.array(apts.values_list('lat',flat=True))
    lng = np.array(apts.values_list('lng',flat=True))
    name = list(apts.values_list('name',flat=True))
    street = list(apts.values_list('addressStreet',flat=True))
    number = list(apts.values_list('addressNumber',flat=True))

    callback = CustomJS(args={
            'name':name,
            'lat':lat,
            'lng':lng,
            'street':street,
            'number':number
            },
            code="""
                console.log(cb_data.source.selected.indices)
                var i = cb_data.source.selected.indices[0];
                $("#name").val(name[i]);
                $("#lat").val(lat[i]);
                $("#lng").val(lng[i]);
                $("#street").val(street[i]);
                $("#number").val(number[i]);
            """
            )
    """
    $("#id_valorUF").change(function () {
        var valor = $(this).val();
        $.ajax({
            url: 'test',
            data: {'id': id},
        success: function (data) {
          data = JSON.parse(data)
          $("#id_valor").val(parseFloat(data.valorComercialPesos));
          $("#id_valor_liquidez").val(parseFloat(data.valorLiquidezPesos));
          $("#id_valor_liquidez_uf").val(parseFloat(data.valorLiquidezUF));
          $("#id_valor_monto_seguro").val(parseFloat(data.montoSeguroPesos));
          $("#id_valor_monto_seguro_uf").val(parseFloat(data.montoSeguroUF));
        }
      });
    });
    """

    source = ColumnDataSource(data=dict(
        x=lat,
        y=lng,
        name=name)
    )

    TOOLTIPS = [
        ("Nombre:", "@name"),
    ]
    p = figure(title= 'Santiago',
        x_axis_label= 'X-Axis',
        y_axis_label= 'Y-Axis',
        plot_width =600,
        plot_height =600,
        tooltips=TOOLTIPS,
        tags=name)

    p.circle('x', 'y', size=5, color="navy", source=source)    
    p.add_tools(TapTool(callback=callback))

    
    script, div = components(p)
    return render(request, 'viz/test.html',{'script' : script , 'div' : div})
