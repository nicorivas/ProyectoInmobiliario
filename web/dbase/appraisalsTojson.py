import pandas as pd #To manage dataframes and excel files


'''Functions that takes a bank's appraisal of a property in a Excel form and returns a json'''

#file = '/Volumes/GoogleDrive/Mi unidad/ProyectoInmobiliario/Informes/N-1762594 (9910373-6) Bartolome Coleone 8248 Las Condes.xlsx'
file = 'G:/Mi unidad/ProyectoInmobiliario/Informes/N-1762594 (9910373-6) Bartolome Coleone 8248 Las Condes.xlsx'
df = pd.read_excel(file, sheet_name='INFORME TASACION')
file2 = 'G:/Mi unidad/ProyectoInmobiliario/Informes/N-1761814 (96986670-6) Lincoyan 9930 Loteo Industrial Buenaventura Quilicura.xls'
df2 = pd.read_excel(file2, sheet_name='TASACION')
pd.read_

df.to_excel('G:/Mi unidad/ProyectoInmobiliario/Informes/test.xlsx', encoding='utf8')

def santander_app1(file):

    '''Takes a property appraisal for Santander in a specific excel file
    and returns a dictionary with the property data'''

    df = pd.read_excel(file, sheet_name='INFORME TASACION')
    appraisal_data = {}
    property_data = {} #Dictionary to save property data
    appraisal_info = {} #Dictionary with information about the appraisal itself (client, bank, executive, etc.)

    appraisal_info['solicitante'] = df.iat[8, 13]
    appraisal_info['ejecutivo'] = df.iat[9, 13]
    appraisal_info['cliente'] = df.iat[10, 13]
    appraisal_info['rut_cliente'] = df.iat[11, 13]
    appraisal_info['propietario'] = df.iat[12, 13]
    appraisal_info['rut_propietario'] = df.iat[13, 13]
    appraisal_info['rol_avaluo'] = df.iat[16, 13]
    appraisal_info['tasador'] = df.iat[20, 13]
    appraisal_info['rut_tasador'] = df.iat[21, 13]
    appraisal_info['empresa'] = df.iat[22, 13]
    appraisal_info['rut_empresa'] = df.iat[23, 13]
    appraisal_info['visador_blanco'] = df.iat[25, 13]

    property_data['direccion'] =df.iat[14,13]
    property_data['comuna'] = df.iat[17, 13]
    property_data['ciudad'] = df.iat[18, 13]
    property_data['region'] = df.iat[19, 13]
    property_data['coordenadas'] = {'latitud': df.iat[24, 14], 'longitud':df.iat[24, 35]}
    property_data['descripcion_general'] = df.iat[28, 33]
    property_data['nota'] = df.iat[47, 33]
    property_data['mercad_objetivo'] = df.iat[8, 53]
    property_data['antiguedad'] = df.iat[9, 53]
    property_data['vida_util_remanente'] = df.iat[10, 53]
    property_data['avaluo_fiscal'] = df.iat[11, 53]
    property_data['acogida_a'] = df.iat[12, 53]
    property_data['dfl2'] = df.iat[13, 53]
    property_data['sello_verde'] = df.iat[14, 53]
    property_data['coprop_inmobiliaria'] = df.iat[15, 53]
    property_data['ocupante'] = df.iat[16, 53]
    property_data['tipo'] = df.iat[17, 53]
    property_data['destino_segun_sii'] = df.iat[18, 53]
    property_data['uso_actual'] = df.iat[19, 53]
    property_data['uso_futuro'] = df.iat[20, 53]
    property_data['perm_edificacion'] = df.iat[21, 53]
    property_data['recepcion_final'] = df.iat[22, 53]
    property_data['expropiacion'] = df.iat[23, 53]
    property_data['vivienda_social'] = df.iat[24, 53]
    property_data['adobe'] = df.iat[25, 53]
    property_data['cont_desmontable'] = df.iat[26, 53]
    property_data['valor_comercial_pesos'] = df.iat[81, 45]
    property_data['valor_comercial_uf'] = df.iat[81, 53]
    property_data['liquidez_porcentaje'] = df.iat[83, 41]
    property_data['valor_liquidez_pesos'] = df.iat[83, 45]
    property_data['valor_liquidez_uf'] = df.iat[83, 53]
    property_data['monto_seguro_pesos'] = df.iat[84, 45]
    property_data['monto_seguro_uf'] = df.iat[84, 53]

    appraisal_data['property_data'] = property_data
    appraisal_data['appraisal_info'] = appraisal_info
    return appraisal_data
