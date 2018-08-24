import json
json_data = open('data/chile/comunas_regiones.json','r')
data = json.load(json_data)
data = data['regiones']
regiones = []
regiones_comunas = {}
comunas = []
for i, region in enumerate(data):
    regiones.append(region['region'])
    regiones_comunas[region['region']] = region['comunas']
    for comuna in region['comunas']:
        comunas.append(comuna)