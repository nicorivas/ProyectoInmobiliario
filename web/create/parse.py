from region.models import Region
from commune.models import Commune
from building.models import Building
from dbase.globals import *
from appraisal.models import Appraisal
import datetime
import re
import unidecode
import requests
from lxml import html
import dateutil.parser

def get_value(ws,cell):
    if ws[cell].value == None:
        return None
    if type(ws[cell].value) == type(""):
        if ws[cell].value == "":
            return None
        else:
            return ws[cell].value

def parse_date(string):
    print(string)
    return dateutil.parser.parse(string)

def parse_email(string):
    if '<' in string:
        iii = string.index('<')+1
        iif = string.index('>')
        return string[iii:iif].strip().lower()
    else:
        return string.strip().lower()

def parse_telephone(string):
    if re.search('[a-zA-Z]', string):
        return None
    else:
        return string.strip().replace(' ','')

def parse_address(address,commune=None):
    addressNumber2 = None
    addressNumber = None

    address = address.lower().strip()

    if commune:
        commune = commune.lower()
        if address.endswith(commune):
            address = address[:address.find(commune)].strip()
        commune = unidecode.unidecode(commune)
        if address.endswith(commune):
            address = address[:address.find(commune)].strip()

    dpto_strings = ["dpto.","dpto","depto.","depto","departamento","oficina"]
    for dpto_string in dpto_strings:
        if dpto_string in address:
            match = re.search(dpto_string+' ?(\d+)', address)
            if match:
                addressNumber2 = match.group(1)
                address = address[:address.index(dpto_string)]
                break

    casa_strings = ["casa.","casa "]
    for casa_string in casa_strings:
        if casa_string in address:
            match = re.search(casa_string+' ?[a-zA-Z0-9]', address)
            if match:
                addressNumber2 = match.group(0).title()
                address = address[:address.index(casa_string)]
                break

    address = address.strip()
    if address[-1] == ',' or address[-1] == '.' or address[-1] == '-':
        address = address[:-1].strip()

    match = re.search('(\d+)$', address) 
    if match:
        addressNumber = match.group(0)
        address = address[:address.index(addressNumber)]
    address = address.strip()
    address = address.replace("avenida","av.")
    address = address.replace('aven','av.')
    address = address.replace('avnda','av.')

    addressStreet = address

    no_strings = ["no.","nº"]
    for no_string in no_strings:
        if address.endswith(no_string):
            addressStreet = address[:address.find(no_string)]
            break

    if addressStreet.startswith('calle'):
        addressStreet = addressStreet[5:].strip()

    addressStreet = addressStreet.title()

    return [addressStreet,addressNumber,addressNumber2]

def parse_rut(rut):
    rut = rut.replace('.','').replace(',','').replace('-','').lower()
    return rut[:-1].strip()+'-'+rut[-1].strip()

def parse_commune(string):
    commune = string.strip().title()
    if '(' in commune:
        commune = commune[:commune.index('(')].strip()
    if commune in COMMUNE_NAME_ASCII__UTF.keys():
        commune = COMMUNE_NAME_ASCII__UTF[commune]
    commune = Commune.objects.get(name=commune)
    region = commune.region
    commune = commune
    return [commune, region]

def parse_solicitante_ejecutivo(string):
    return string.strip().title()

def parse_solicitante_sucursal(string):
    return string.strip().title()

def parseItau(ws):
    '''
    Devuelve datos de solicitud ITAU
    '''
    data = {}

    for c in Appraisal.petitioner_choices:
        if c[1] == 'Itaú':
            data['solicitante'] = c[0]

    d = {
            'appraisalTimeRequest':["M3",parse_date],
            'solicitanteEjecutivo':["C7",parse_solicitante_ejecutivo],
            'solicitanteEjecutivoEmail':["J7",parse_email],
            'solicitanteSucursal':["C9",parse_solicitante_sucursal],
            'solicitanteEjecutivoEmail':[["J7","K7"],parse_email],
            'solicitanteEjecutivoTelefono':[["O7","P7"],parse_telephone],
            'solicitanteEjecutivoTelefono':[["O7","P7"],parse_telephone],
        }
    for variable, info in d.items():
        function = info[1]
        coords = info[0]
        if type(coords) == type([]):
            for coord in coords:
                value = get_value(ws,coord)
                if value != None:
                    data[variable] = function(value)
                    if data[variable] != None:
                        break

    tipoTasacion = ws['G9'].value
    if tipoTasacion == "Operación:":
        tipoTasacion = ws['H9'].value
    if tipoTasacion:
        tipoTasacion = tipoTasacion.strip()
        if tipoTasacion == 'CRÉDITO HIPOTECARIO':
            data['tipoTasacion'] = Appraisal.HIPOTECARIA
            data['finalidad'] = Appraisal.CREDITO
        if tipoTasacion == 'CRÉDITO COMERCIAL':
            data['tipoTasacion'] = Appraisal.COMERCIAL
            data['finalidad'] = Appraisal.CREDITO

    finalidad = ws['J9'].value
    if finalidad:
        finalidad = finalidad.strip()
        if finalidad == 'ACTUALIZAR GARANTÍA':
            data['finalidad'] = Appraisal.GARANTIA
        elif finalidad == 'COMPRA INMUEBLE':
            data['finalidad'] = Appraisal.CREDITO
        elif finalidad == 'LIQUIDACIÓN FORZADA':
            data['finalidad'] = Appraisal.LIQUIDACION
        elif finalidad == 'DACIÓN EN PAGO':
            data['finalidad'] = Appraisal.DACION_EN_PAGO

    appraisalTimeRequest = ws['M3'].value
    if isinstance(appraisalTimeRequest,type('')):
        data['appraisalTimeRequest'] = parse_date(appraisalTimeRequest).strftime('%d/%m/%Y %H:%M')

    cliente = ws['C14'].value
    if isinstance(cliente,type('')):
        if cliente != '':
            data['cliente'] = ws['C14'].value.strip().title()

    if ws['C16'].value != None:
        if '-' in ws['C16'].value:
            # Rut viene todo en la celda
            data['clienteRut'] = parse_rut(ws['C16'].value)
        else:
            if ws['F16'].value != None:
                data['clienteRut'] = parse_rut(ws['C16'].value+ws['F16'].value)
            if ws['G16'].value != None:
                data['clienteRut'] = parse_rut(ws['C16'].value+ws['G16'].value)
            else:
                data['clienteRut'] = parse_rut(ws['C16'].value)
            
    clienteEmail = ws['C22'].value
    if isinstance(clienteEmail,type('')):
        if clienteEmail != '':
            data['clienteEmail'] = parse_email(clienteEmail)
    
    clienteTelefono = ws['C24'].value
    if isinstance(clienteTelefono,type('')):
        if clienteTelefono != '':
            data['clienteTelefono'] = ws['C24'].value.strip().replace(' ','')
    
    contacto = ws['C26'].value
    if isinstance(contacto,type('')):
        if contacto != '':
            data['contacto'] = ws['C26'].value.strip().title()

    contactoEmail = ws['C28'].value
    if isinstance(contactoEmail,type('')):
        if contactoEmail != '':
            data['contactoEmail'] = parse_email(contactoEmail)

    contactoTelefono = ws['C30'].value
    if isinstance(contactoTelefono,type('')):
        if contactoTelefono != '':
            data['contactoTelefono'] = ws['C30'].value.strip().replace(' ','')

    tipo = ws['C37'].value
    if tipo != None:
        if isinstance(tipo,type('')):
            tipo = tipo.strip()
        if tipo == 'CASAS':
            data['propertyType'] = Building.TYPE_CASA
        elif tipo == 'DEPARTAMENTOS':
            data['propertyType'] = Building.TYPE_DEPARTAMENTO
        elif tipo == 'OFICINAS':
            data['propertyType'] = Building.TYPE_OFICINA
        elif tipo == 'TERRENO PROYECTO INMOBILIARIO':
            data['propertyType'] = Building.TYPE_TERRENO
        elif tipo == 'SITIOS Y TERRENOS URBANOS':
            data['propertyType'] = Building.TYPE_TERRENO
        elif tipo == 'LOCALES COMERCIALES':
            data['propertyType'] = Building.TYPE_LOCAL_COMERCIAL
        elif tipo == 'CONSTRUCCIONES INDUSTRIALES':
            data['propertyType'] = Building.TYPE_INDUSTRIA
        elif 'BODEGAS' in tipo:
            data['propertyType'] = Building.TYPE_BODEGA
        elif 'ESTACIONAMIENTOS' in tipo:
            data['propertyType'] = Building.TYPE_ESTACIONAMIENTO
        elif 'BIENES RAICES RURALES' in tipo:
            data['propertyType'] = Building.TYPE_PARCELA
        else:
            data['propertyType'] = Building.TYPE_OTRO

    if ws['C45'].value != None:
        try :
            commune, region = parse_commune(ws['C45'].value)
            data['addressCommune'] = commune.id
            data['addressRegion'] = region.id
        except Commune.DoesNotExist:
            pass

    addressStreet = ws['C41'].value
    if isinstance(addressStreet,type('')):
        if addressStreet != '':
            if 'addressCommune' in data.keys():
                addressStreet, addressNumber, addressNumber2 = parse_address(addressStreet,
                    commune=Commune.objects.get(id=data.get('addressCommune')).name.lower())
                data['addressStreet'] = addressStreet
                if addressNumber:
                    data['addressNumber'] = addressNumber
                if addressNumber2:
                    data['addressNumber2'] = addressNumber2

    rol = ws['C43'].value
    if isinstance(rol,type('')):
        if rol != '':
            data['rol'] = ws['C43'].value.strip()

    comments = ws['B54'].value
    if isinstance(comments,type('')):
        if comments != '':
            data['comments'] = comments.strip()

    return data

def parseBancoDeChileAvance(wb):
    '''
    Sacar información de solicitu de Banco de Chile, para tasaciones
    de avance de obras. Recibe un archivo excel.
    '''

    ws = wb.worksheets[0]

    data = {}

    for c in Appraisal.petitioner_choices:
        if c[1] == 'Banco de Chile':
            data['solicitante'] = c[0]

    solicitanteEjecutivo = ws['E61'].value
    if isinstance(solicitanteEjecutivo,type('')):
        if solicitanteEjecutivo != '':
            data['solicitanteEjecutivo'] = solicitanteEjecutivo.strip().title()

    solicitanteSucursal = ws['E62'].value
    if isinstance(solicitanteSucursal,type('')):
        if solicitanteSucursal != '':
            data['solicitanteSucursal'] = solicitanteSucursal.strip().title()

    solicitanteEjecutivoEmail = ws['E63'].value
    if isinstance(solicitanteEjecutivoEmail,type('')):
        if solicitanteEjecutivoEmail != '':
            data['solicitanteEjecutivoEmail'] = solicitanteEjecutivoEmail.strip().lower()

    solicitanteEjecutivoTelefono = ws['M62'].value
    if solicitanteEjecutivoTelefono != '':
        data['solicitanteEjecutivoTelefono'] = str(solicitanteEjecutivoTelefono)

    solicitanteEjecutivoRut = str(ws['M61'].value)+str(ws['N61'].value)
    if isinstance(solicitanteEjecutivoRut,type('')):
        if solicitanteEjecutivoRut != '':
            data['solicitanteEjecutivoRut'] = parse_rut(solicitanteEjecutivoRut)

    cliente = ws['H9'].value
    if isinstance(cliente,type('')):
        if cliente != '':
            data['cliente'] = cliente.strip().title()

    clienteRut = ws['H10'].value
    clienteRutDF = ws['J10'].value
    if clienteRut != '' and clienteRutDF != '':
        data['clienteRut'] = parse_rut(str(clienteRut)+''+clienteRutDF)

    contacto = ws['E56'].value
    if isinstance(contacto,type('')):
        if contacto != '':
            data['contacto'] = contacto.strip().title()

    contactoEmail = ws['E58'].value
    if isinstance(contactoEmail,type('')):
        if contactoEmail != '':
            data['contactoEmail'] = contactoEmail.strip().lower()

    contactoTelefono = ws['M56'].value
    if contactoTelefono != '':
        data['contactoTelefono'] = str(contactoTelefono)

    tipoTasacion = ws['I12'].value.strip()
    if 'ESTADO de AVANCE' in tipoTasacion:
        data['tipoTasacion'] = Appraisal.AVANCE_DE_OBRA
        data['finalidad'] = Appraisal.OTRO
        data['visita'] = Appraisal.COMPLETA


    tipo = ws['H17'].value
    if isinstance(tipo,type('')):
        tipo = tipo.strip()
        if tipo == 'Casas':
            data['propertyType'] = Building.TYPE_CONDOMINIO
        if tipo == 'CASA':
            data['propertyType'] = Building.TYPE_CASA
        elif tipo == 'DEPARTAMENTO':
            data['propertyType'] = Building.TYPE_DEPARTAMENTO

    address = ws['K17'].value
    if isinstance(address,type('')):
        if address != '':
            addressStreet, addressNumber, addressNumber2 = parse_address(address)
            data['addressStreet'] = addressStreet
            if addressNumber:
                data['addressNumber'] = addressNumber
            if addressNumber2:
                data['addressNumber2'] = addressNumber2

    try :
        commune = ws['M17'].value
        if commune == 'EST. CENTRAL':
            commune = "Estación Central"
        commune = Commune.objects.get(name=commune.strip().title())
        data['addressCommune'] = commune.id
        data['addressRegion'] = commune.region.code
    except Commune.DoesNotExist:
        pass

    if ws['N6'].value:
        data['appraisalTimeRequest'] = ws['N6'].value.strftime('%d/%m/%Y %H:%M')

    ws = wb.worksheets[1]

    data['appraisalTimeDue'] = ws['J41'].value.strftime('%d/%m/%Y %H:%M')

    data['solicitanteCodigo'] = ws['E37'].value

    return data

def parseBancoDeChile(text):
    '''
    Devuelve datos de solicitud de Banco de Chile (general)
    Recibe un arreglo de strings que es el .pdf cortado.
    '''
    data = {}
    
    for c in Appraisal.petitioner_choices:
        if c[1] == 'Banco de Chile':
            data['solicitante'] = c[0]
    for i, line in enumerate(text):
        if 'ID' == line.strip():
            data['solicitanteCodigo'] = text[i+6].strip()
        if 'TIPO OPERACION' in line.strip():
            if text[i+6].strip() == "Crédito Hipotecario":
                data['tipoTasacion'] = Appraisal.HIPOTECARIA
                data['finalidad'] = Appraisal.CREDITO
        if 'TIPO DE BIEN' in line.strip():
            if text[i+6].strip() == "DEPARTAMENTO":
                data['propertyType'] = Building.TYPE_DEPARTAMENTO
            if text[i+6].strip() == "CASA":
                data['propertyType'] = Building.TYPE_CASA
        if 'COMUNA' in line.strip():
            comuna = text[i+6].strip().title()
            print(comuna)
            try:
                commune = Commune.objects.get(name_simple=unidecode.unidecode(comuna))
                data['addressCommune'] = commune.id
                data['addressRegion'] = commune.region.code
            except Commune.DoesNotExist:
                data['addressCommune'] = ""
                data['addressRegion'] = ""
        if 'ROL' in line.strip():
            data['rol'] = text[i+6+c-1].strip()
        if 'DIRECCION' in line.strip():
            address = ''
            c = 0
            while not 'De propiedad de' in text[i+6+c+1].strip():
                address += text[i+6+c].strip().title()
                c += 1
            addressStreet, addressNumber, addressNumber2 = parse_address(address)
            data['addressStreet'] = addressStreet
            if addressNumber:
                data['addressNumber'] = addressNumber
            if addressNumber2:
                data['addressNumber2'] = addressNumber2
        if 'Cliente' in line.strip():
            data['cliente'] = text[i+2].strip().title()
        if 'Rut' == line.strip():
            data['clienteRut'] = parse_rut(text[i+2])
        if 'Nombre' == line.strip():
            data['solicitanteEjecutivo'] = text[i+2].strip().title()
        if 'Teléfono' == line.strip():
            data['solicitanteEjecutivoTelefono'] = text[i+2].strip().replace(' ','')
        if 'E - Mail' == line.strip():
            data['solicitanteEjecutivoEmail'] = text[i+2].strip().lower()
        if 'Unidad' in line.strip():
            data['solicitanteSucursal'] = text[i+2].strip().title()
        if 'INFORMACION ADICIONAL' in line.strip():
            data['comments'] = ''
            c = 1
            while not 'Antecedentes' in text[i+c].strip() or 'Información de Contacto' in text[i+c].strip():
                data['comments'] += text[i+c].strip()
                c += 1
        if 'Información de Contacto' in line.strip():
            line = text[i+1]
            if '@' in text[i+2]:
                line += text[i+2]
                data['appraisalTimeRequest'] = text[i+3]+' '+text[i+4]
            else:
                data['appraisalTimeRequest'] = text[i+2]+' '+text[i+3]
            c = line.split('/')
            data['contacto'] = c[0]
            for cc in c[1:]:
                if 'Fono' in cc:    
                    data['contactoTelefono'] = cc.split(':')[1].strip().replace(' ','')
                elif 'E-Mail' in cc:
                    data['contactoEmail'] = cc.split(':')[1].strip()

    return data

def parseSantander(text):
    '''
    Devuelve datos de solicitud del Santander
    Recibe un arreglo de strings que es el .pdf cortado.
    '''
    
    data = {}
    
    address = ''

    for c in Appraisal.petitioner_choices:
        if c[1] == 'Santander':
            data['solicitante'] = c[0]
    for i, line in enumerate(text):
        if 'Nº Req' in line.strip():
            data['solicitanteCodigo'] = line.split(':')[1].strip()
        elif 'Fecha de asignación' in line.strip():
            data['appraisalTimeRequest'] = text[i+5].strip()
        elif 'Entregar informe de' in line.strip():
            data['appraisalTimeDue'] = text[i+5].strip()
        elif 'Nombre Cliente' in line.strip():
            data['cliente'] = line.split(':')[1].strip().title()
            c = 1
            while not 'RUT Cliente' in text[i+c].strip():
                if text[i+c].strip() == '':
                    c += 1
                    continue
                data['cliente'] += ' '+text[i+c].strip().title()
                c += 1
        elif 'RUT Cliente' in line.strip():
            data['clienteRut'] = parse_rut(line.split(':')[1])
        elif 'Nombre Propietario' in line.strip():
            data['propietario'] = line.split(':')[1].strip().title()
            c = 1
            while not 'RUT Propietario' in text[i+c].strip():
                if text[i+c].strip() == '':
                    c += 1
                    continue
                data['propietario'] += ' '+text[i+c].strip().title()
                c += 1
        elif 'RUT Propietario' in line.strip():
            data['propietarioRut'] = parse_rut(line.split(':')[1])
        elif 'Nombre Contacto' in line.strip():
            data['contacto'] = line.split(':')[1].strip().title()
        elif 'Telefono movil' in line.strip():
            data['contactoTelefono'] = text[i+1].split(':')[1].strip().replace(' ','')
        elif 'Direccion' in line.strip():
            address = line.split(':')[1].strip()            
        elif 'Rubro :' in line.strip():
            tipoTasacion = line.split(':')[1].strip()
            if tipoTasacion == "HIPOTECARIO":
                data['tipoTasacion'] = Appraisal.HIPOTECARIA
                data['finalidad'] = Appraisal.CREDITO
            elif tipoTasacion == "GARANTIAS GENERALES":
                data['finalidad'] = Appraisal.GARANTIA
        elif 'Grupo :' in line.strip():
            propertyType = line.split(':')[1].strip()
            if 'DEPARTAMENTO' in propertyType:
                data['propertyType'] = Building.TYPE_DEPARTAMENTO
            elif 'VIVIENDA' in propertyType:
                pass # Puede ser casa o departamento
            elif 'TERRENO' in propertyType:
                data['propertyType'] = Building.TYPE_TERRENO
            elif 'LOCAL COMERCIAL' in propertyType:
                data['propertyType'] = Building.TYPE_LOCAL_COMERCIAL
                data['tipoTasacion'] = Appraisal.COMERCIAL
            elif 'LOCALCOMERCIAL' in propertyType:
                data['propertyType'] = Building.TYPE_LOCAL_COMERCIAL
                data['tipoTasacion'] = Appraisal.COMERCIAL
            elif 'AVANCE' in propertyType:
                data['tipoTasacion'] = Appraisal.AVANCE_DE_OBRA
        elif 'Rol :' in line.strip():
            data['rol'] = line.split(':')[1].strip()
        elif 'Comuna' in line.strip():
            communes = line.split(':')[1].strip().title()
            commune, region = parse_commune(communes)
            data['addressCommune'] = commune.id
            data['addressRegion'] = region.code
            addressStreet, addressNumber, addressNumber2 = parse_address(address,commune=commune.name)
            data['addressStreet'] = addressStreet
            if addressNumber:
                data['addressNumber'] = addressNumber
            if addressNumber2:
                data['addressNumber2'] = addressNumber2
        elif 'Nombre Ejecutivo' in line.strip():
            data['solicitanteEjecutivo'] = line.split(':')[1].strip().title()
            c = 1
            while not 'E-Mail Ejecutivo' in text[i+c].strip():
                if text[i+c].strip() == '':
                    c += 1
                    continue
                data['solicitanteEjecutivo'] += ' '+text[i+c].strip().title()
                c += 1
        elif 'Telefono Ejecutivo' in line.strip():
            data['solicitanteEjecutivoTelefono'] = line.split(':')[1].strip().replace(' ','')
        elif 'E-Mail Ejecutivo' in line.strip():
            data['solicitanteEjecutivoEmail'] = line.split(':')[1].strip()
        elif 'Sucursal' in line.strip():
            data['solicitanteSucursal'] = line.split(':')[1].strip().title()
        elif 'Centro de Costo' in line.strip():
            c = 1
            data['comments'] = ''
            while i+c < len(text) and not 'Página 1 de 2' in text[i+c].strip() and not 'Incidencia' in text[i+c].strip():
                if len(text[i+c]) > 1 and text[i+c].strip()[1:-1] not in data['comments']:
                    data['comments'] += text[i+c].strip()
                c += 1

    return data

def parseSantanderUrl(url):

    data = {}
    
    with requests.Session() as s:

        login_url = "https://extranet.gruposantander.cl/autentica.aspx"
        login_data = {"user": "70149761", "clave": "protasa2018"}
        response = s.post(login_url, data=login_data, headers=dict(referer="https://extranet.gruposantander.cl/"))
        # These are to populate the session with the right cookies
        response = s.get("https://extranet.gruposantander.cl/gateW.aspx?dst_url=https://tasaciones.extranetsantander.cl/segesta/login_prov_adm.aspx?qry=ok&UrlToken=&Target=principal&UsaToken=SI")
        response = s.get("https://tasaciones.extranetsantander.cl/SEGESTA/VISTAS/PERFILES/INI_Generico.aspx",headers=dict(referer="https://extranet.gruposantander.cl/arriba2.aspx"))
        # Now that we have the right cookies, really get the appraisal
        response = s.get(url,headers=dict(referer=url))
        tree = html.fromstring(response.content)
        for c in Appraisal.petitioner_choices:
            if c[1] == 'Santander':
                data['solicitante'] = c[0]
        data['solicitanteCodigo'] = tree.xpath('//*[@id="lbl_requerimientoID"]/text()')
        data['solicitanteSucursal'] = tree.xpath('//*[@id="suc_ejecutivo"]/text()')

        ejecutivo = tree.xpath('//*[@id="lbl_nomEjecutivo"]/text()')
        if len(ejecutivo) > 0:
            data['solicitanteEjecutivo'] = ejecutivo[0]
        data['solicitanteEjecutivoEmail'] = tree.xpath('//*[@id="lbl_mailEjecutivo"]/text()')
        data['appraisalTimeRequest'] = tree.xpath('//table//td[contains(text(),"Fecha Ingreso")]/../following-sibling::tr[1]/td[1]/text()')[0].replace("-","/")
        data['appraisalTimeDue'] = tree.xpath('//table//td[contains(text(),"Entrega en Estándar Real")]/../following-sibling::tr[1]/td[6]/text()')[0].replace("-","/")

        rubro = tree.xpath('//*[@id="lbl_rubro"]/text()')
        if "Garantía General" in rubro:
            data['tipoTasacion'] = Appraisal.GARANTIA
            data['finalidad'] = Appraisal.GARANTIA

        data['cliente'] = tree.xpath('//*[@id="lbl_nomSolicitante"]/text()')
        data['clienteRut'] = tree.xpath('//*[@id="lbl_rutSolicitante"]/text()')

        propietario = tree.xpath('//*[@id="lbl_nomPropietario"]/text()')
        if len(propietario) > 0:
            data['propietario'] = propietario[0].title()
        propietarioRut = tree.xpath('//*[@id="lbl_rutPropietario"]/text()')
        if len(propietarioRut) > 0:
            data['propietarioRut'] = propietarioRut[0]

        data['contacto'] = tree.xpath('//*[@id="lbl_nomContacto"]/text()')
        data['contactoEmail'] = tree.xpath('//*[@id="lbl_emailContacto"]/text()')
        data['contactoTelefono'] = tree.xpath('//*[@id="lbl_fono1Contacto"]/text()')

        rubro = tree.xpath('//*[@id="lbl_rubro"]/text()')
        if len(rubro) > 0:
            rubro = rubro[0].strip()
            if "Local Comercial" in rubro:
                data['propertyType'] = Building.TYPE_LOCAL_COMERCIAL
                data['tipoTasacion'] = Appraisal.COMERCIAL
            if "Leasing" in rubro:
                data['tipoTasacion'] = Appraisal.LEASING
            if "Convenio Hipotecario" in rubro:
                data['tipoTasacion'] = Appraisal.CONVENIO_HIPOTECARIO

        grupo = tree.xpath('//*[@id="lbl_grupo"]/text()')
        if len(grupo) > 0:
            grupo = grupo[0].strip()
            if "Oficina" in grupo:
                data['propertyType'] = Building.TYPE_OFICINA

        commune, region = parse_commune(tree.xpath('//*[@id="lbl_comuna"]/text()')[0])
        data['addressCommune'] = commune.id
        data['addressRegion'] = region.id

        address = tree.xpath('//*[@id="lbl_direccion"]/text()')
        if len(address) > 0:
            street, number, number2 = parse_address(address[0])
            data['addressStreet'] = street
            data['addressNumber'] = number
            data['addressNumber2'] = number2

        roles = tree.xpath('//*[@id="lbl_roles"]/text()')
        if len(roles) > 0:
            if roles[0] != "":
                data["rol"] = roles[0].split(',')[0]

    return data