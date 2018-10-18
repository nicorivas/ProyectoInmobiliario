from slugify import slugify # for nice filenames

from sqlalchemy import create_engine # for pandas dataframes to postgre
from sqlalchemy import MetaData
#from sqlalchemy.sql import and_
#from sqlalchemy import update


DATA_PATH = '/Users/nico/Code/ProyectoInmobiliario/data'
GEO_DATA_PATH = '/Users/nico/Code/ProyectoInmobiliario/data/geo/chile'
REALSTATE_DATA_PATH = '/Users/nico/Code/ProyectoInmobiliario/data/realestate'

'''
Regions of Chile
'''

REGION_NAME__ISO_CODE = {
    u'Arica y Parinacota':'CL-AP',
    u'Tarapacá':'CL-TA',
    u'Antofagasta':'CL-AN',
    u'Atacama':'CL-AT',
    u'Coquimbo':'CL-CO',
    u'Valparaíso':'CL-VS',
    u"Libertador General Bernardo O'Higgins":'CL-LI',
    u'Maule':'CL-ML',
    u'Biobío':'CL-BI',
    u'La Araucanía':'CL-AR',
    u'Los Ríos':'CL-LR',
    u'Los Lagos':'CL-LL',
    u'Aysén del General Carlos Ibáñez del Campo':'CL-AI',
    u'Magallanes y Antártica Chilena':'CL-MA',
    u'Metropolitana de Santiago':'CL-RM'
}

REGION_NAME__SHORT_NAME = {
    u'Arica y Parinacota':'Arica',
    u'Tarapacá':'Tarapacá',
    u'Antofagasta':'Antofagasta',
    u'Atacama':'Atacama',
    u'Coquimbo':'Coquimbo',
    u'Valparaíso':'Valparaíso',
    u"Libertador General Bernardo O'Higgins":"O'Higgins",
    u'Maule':'Maule',
    u'Biobío':'Biobío',
    u'La Araucanía':'La Araucanía',
    u'Los Ríos':'Los Ríos',
    u'Los Lagos':'Los Lagos',
    u'Aysén del General Carlos Ibáñez del Campo':'Aysén',
    u'Magallanes y Antártica Chilena':'Magallanes',
    u'Metropolitana de Santiago':'Metropolitana'
}

REGION_NAME__CODE = {
    u'Arica y Parinacota':15,
    u'Tarapacá':1,
    u'Antofagasta':2,
    u'Atacama':3,
    u'Coquimbo':4,
    u'Valparaíso':5,
    u"Libertador General Bernardo O'Higgins":6,
    u'Maule':7,
    u'Biobío':8,
    u'La Araucanía':9,
    u'Los Ríos':14,
    u'Los Lagos':10,
    u'Aysén del General Carlos Ibáñez del Campo':11,
    u'Magallanes y Antártica Chilena':12,
    u'Metropolitana de Santiago':13
}

REGION_CODE__NAME = {v: k for k, v in REGION_NAME__CODE.items()}

REGION_CODE__NAME_SLUG = {v: slugify(k) for k, v in REGION_NAME__CODE.items()}

REGION_NAME = REGION_NAME__CODE.keys()

REGION_NAME_SLUG = [slugify(k) for k, v in REGION_NAME__CODE.items()]

COMMUNE_NAME__CODE = {'Arica': 15101, 'Camarones': 15102, 'Putre': 15201,
'General Lagos': 15202, 'Iquique': 1101, 'Alto Hospicio': 1102,
'Pozo Almonte': 1201, 'Camiña': 1402, 'Colchane': 1403, 'Huara': 1404,
'Pica': 1405, 'Antofagasta': 2101, 'Mejillones': 2102, 'Sierra Gorda': 2103,
'Taltal': 2104, 'Calama': 2201, 'Ollagüe': 2202, 'San Pedro de Atacama': 2203,
'Tocopilla': 2301, 'María Elena': 2302, 'Copiapó': 3101, 'Caldera': 3102,
'Tierra Amarilla': 3103, 'Chañaral': 3201, 'Diego de Almagro': 3202,
'Vallenar': 3301, 'Alto del Carmen': 3302, 'Freirina': 3303, 'Huasco': 3304,
'La Serena': 4101, 'Coquimbo': 4102, 'Andacollo': 4103, 'La Higuera': 4104,
'Paiguano': 4105, 'Vicuña': 4106, 'Illapel': 4201, 'Canela': 4202,
'Los Vilos': 4203, 'Salamanca': 4204, 'Ovalle': 4301, 'Combarbalá': 4302,
'Monte Patria': 4303, 'Punitaqui': 4304, 'Río Hurtado': 4305, 'Valparaíso': 5101,
'Casablanca': 5102, 'Concón': 5103, 'Juan Fernández': 5104, 'Puchuncaví': 5105,
'Quintero': 5107, 'Viña del Mar': 5109, 'Isla de Pascua': 5201, 'Los Andes': 5301,
'Calle Larga': 5302, 'Rinconada': 5303, 'San Esteban': 5304, 'La Ligua': 5401,
'Cabildo': 5402, 'Papudo': 5403, 'Petorca': 5404, 'Zapallar': 5405,
'Quillota': 5501, 'Calera': 5502, 'Hijuelas': 5503, 'La Cruz': 5504,
'Nogales': 5506, 'San Antonio': 5601, 'Algarrobo': 5602, 'Cartagena': 5603,
'El Quisco': 5604, 'El Tabo': 5605, 'Santo Domingo': 5606, 'San Felipe': 5701,
'Catemu': 5702, 'Llaillay': 5703, 'Panquehue': 5704, 'Putaendo': 5705,
'Santa María': 5706, 'Quilpué': 5801, 'Limache': 5802, 'Olmué': 5803,
'Villa Alemana': 5804, 'Rancagua': 6101, 'Codegua': 6102, 'Coinco': 6103,
'Coltauco': 6104, 'Doñihue': 6105, 'Graneros': 6106, 'Las Cabras': 6107,
'Machalí': 6108, 'Malloa': 6109, 'Mostazal': 6110, 'Olivar': 6111,
'Peumo': 6112, 'Pichidegua': 6113, 'Quinta de Tilcoco': 6114, 'Rengo': 6115,
'Requínoa': 6116, 'San Vicente': 6117, 'Pichilemu': 6201, 'La Estrella': 6202,
'Litueche': 6203, 'Marchihue': 6204, 'Navidad': 6205, 'Paredones': 6206,
'San Fernando': 6301, 'Chépica': 6302, 'Chimbarongo': 6303, 'Lolol': 6304,
'Nancagua': 6305, 'Palmilla': 6306, 'Peralillo': 6307, 'Placilla': 6308,
'Pumanque': 6309, 'Santa Cruz': 6310, 'Talca': 7101, 'Constitución': 7102,
'Curepto': 7103, 'Empedrado': 7104, 'Maule': 7105, 'Pelarco': 7106,
'Pencahue': 7107, 'Río Claro': 7108, 'San Clemente': 7109, 'San Rafael': 7110,
'Cauquenes': 7201, 'Chanco': 7202, 'Pelluhue': 7203, 'Curicó': 7301,
'Hualañé': 7302, 'Licantén': 7303, 'Molina': 7304, 'Rauco': 7305,
'Romeral': 7306, 'Sagrada Familia': 7307, 'Teno': 7308, 'Vichuquén': 7309,
'Linares': 7401, 'Colbún': 7402, 'Longaví': 7403, 'Parral': 7404,
'Retiro': 7405, 'San Javier': 7406, 'Villa Alegre': 7407, 'Yerbas Buenas': 7408,
'Concepción': 8101, 'Coronel': 8102, 'Chiguayante': 8103, 'Florida': 8104,
'Hualqui': 8105, 'Lota': 8106, 'Penco': 8107, 'San Pedro de la Paz': 8108,
'Santa Juana': 8109, 'Talcahuano': 8110, 'Tomé': 8111, 'Hualpén': 8112,
'Lebu': 8201, 'Arauco': 8202, 'Cañete': 8203, 'Contulmo': 8204,
'Curanilahue': 8205, 'Los Álamos': 8206, 'Tirúa': 8207, 'Los Ángeles': 8301,
'Antuco': 8302, 'Cabrero': 8303, 'Laja': 8304, 'Mulchén': 8305,
'Nacimiento': 8306, 'Negrete': 8307, 'Quilaco': 8308, 'Quilleco': 8309,
'San Rosendo': 8310, 'Santa Bárbara': 8311, 'Tucapel': 8312, 'Yumbel': 8313,
'Alto Biobío': 8314, 'Chillán': 8401, 'Bulnes': 8402, 'Cobquecura': 8403,
'Coelemu': 8404, 'Coihueco': 8405, 'Chillán Viejo': 8406, 'El Carmen': 8407,
'Ninhue': 8408, 'Ñiquén': 8409, 'Pemuco': 8410, 'Pinto': 8411,
'Portezuelo': 8412, 'Quillón': 8413, 'Quirihue': 8414, 'Ránquil': 8415,
'San Carlos': 8416, 'San Fabián': 8417, 'San Ignacio': 8418,
'San Nicolás': 8419, 'Treguaco': 8420, 'Yungay': 8421, 'Temuco': 9101,
'Carahue': 9102, 'Cunco': 9103, 'Curarrehue': 9104, 'Freire': 9105,
'Galvarino': 9106, 'Gorbea': 9107, 'Lautaro': 9108, 'Loncoche': 9109,
'Melipeuco': 9110, 'Nueva Imperial': 9111, 'Padre las Casas': 9112,
'Perquenco': 9113, 'Pitrufquén': 9114, 'Pucón': 9115, 'Saavedra': 9116,
'Teodoro Schmidt': 9117, 'Toltén': 9118, 'Vilcún': 9119, 'Villarrica': 9120,
'Cholchol': 9121, 'Angol': 9201, 'Collipulli': 9202, 'Curacautín': 9203,
'Ercilla': 9204, 'Lonquimay': 9205, 'Los Sauces': 9206, 'Lumaco': 9207,
'Purén': 9208, 'Renaico': 9209, 'Traiguén': 9210, 'Victoria': 9211,
'Valdivia': 14101, 'Corral': 14102, 'Lanco': 14103, 'Los Lagos': 14104,
'Máfil': 14105, 'Mariquina': 14106, 'Paillaco': 14107, 'Panguipulli': 14108,
'La Unión': 14201, 'Futrono': 14202, 'Lago Ranco': 14203, 'Río Bueno': 14204,
'Puerto Montt': 10101, 'Calbuco': 10102, 'Cochamó': 10103, 'Fresia': 10104,
'Frutillar': 10105, 'Los Muermos': 10106, 'Llanquihue': 10107, 'Maullín': 10108,
'Puerto Varas': 10109, 'Castro': 10201, 'Ancud': 10202, 'Chonchi': 10203,
'Curaco de Vélez': 10204, 'Dalcahue': 10205, 'Puqueldón': 10206,
'Queilén': 10207, 'Quellón': 10208, 'Quemchi': 10209, 'Quinchao': 10210,
'Osorno': 10301, 'Puerto Octay': 10302, 'Purranque': 10303, 'Puyehue': 10304,
'Río Negro': 10305, 'San Juan de la Costa': 10306, 'San Pablo': 10307,
'Chaitén': 10401, 'Futaleufú': 10402, 'Hualaihué': 10403, 'Palena': 10404,
'Coyhaique': 11101, 'Lago Verde': 11102, 'Aysén': 11201, 'Cisnes': 11202,
'Guaitecas': 11203, 'Cochrane': 11301, "O'Higgins": 11302, 'Tortel': 11303,
'Chile Chico': 11401, 'Río Ibáñez': 11402, 'Punta Arenas': 12101,
'Laguna Blanca': 12102, 'Río Verde': 12103, 'San Gregorio': 12104,
'Cabo de Hornos': 12201, 'Porvenir': 12301, 'Primavera': 12302,
'Timaukel': 12303, 'Natales': 12401, 'Torres del Paine': 12402,
'Santiago': 13101, 'Cerrillos': 13102, 'Cerro Navia': 13103, 'Conchalí': 13104,
'El Bosque': 13105, 'Estación Central': 13106, 'Huechuraba': 13107,
'Independencia': 13108, 'La Cisterna': 13109, 'La Florida': 13110,
'La Granja': 13111, 'La Pintana': 13112, 'La Reina': 13113, 'Las Condes': 13114,
'Lo Barnechea': 13115, 'Lo Espejo': 13116, 'Lo Prado': 13117, 'Macul': 13118,
'Maipú': 13119, 'Ñuñoa': 13120, 'Pedro Aguirre Cerda': 13121, 'Peñalolén': 13122,
'Providencia': 13123, 'Pudahuel': 13124, 'Quilicura': 13125,
'Quinta Normal': 13126, 'Recoleta': 13127, 'Renca': 13128, 'San Joaquín': 13129,
'San Miguel': 13130, 'San Ramón': 13131, 'Vitacura': 13132, 'Puente Alto': 13201,
'Pirque': 13202, 'San José de Maipo': 13203, 'Colina': 13301, 'Lampa': 13302,
'Tiltil': 13303, 'San Bernardo': 13401, 'Buin': 13402, 'Calera de Tango': 13403,
'Paine': 13404, 'Melipilla': 13501, 'Alhué': 13502, 'Curacaví': 13503,
'María Pinto': 13504, 'San Pedro': 13505, 'Talagante': 13601, 'El Monte': 13602,
'Isla de Maipo': 13603, 'Padre Hurtado': 13604, 'Peñaflor': 13605}

COMMUNE_NAME = COMMUNE_NAME__CODE.keys()

COMMUNE_NAME_SLUG = [slugify(c) for c in COMMUNE_NAME]

COMMUNE_CODE__NAME = {v: k for k, v in COMMUNE_NAME__CODE.items()}

COMMUNE_NAME_SLUG__CODE = {slugify(k): v for k, v in COMMUNE_NAME__CODE.items()}

COMMUNE_CODE__NAME_SLUG = {v: k for k, v in COMMUNE_NAME_SLUG__CODE.items()}

COMMUNES_NAME_SLUG = [slugify(a) for a in COMMUNE_NAME__CODE.keys()]

def get_regions():
    sql_engine = create_engine('postgresql://postgres:iCga1kmX@localhost:5432/data')
    sql_metadata = MetaData(sql_engine,reflect=True)
    sql_connection = sql_engine.connect()
    sql_buildings_table = sql_metadata.tables['region_region']

    sql_select = sql_buildings_table.select()
    result = sql_connection.execute(sql_select)
    for row in result:
        print(row)

    sql_connection.close()
