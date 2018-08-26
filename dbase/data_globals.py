region_name_to_iso_code = {
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

region_name_to_code = {
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

code_to_region_name = {v: k for k, v in region_name_to_code.items()}
