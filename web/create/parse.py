from region.models import Region
from commune.models import Commune
from building.models import Building
from dbase.globals import *
from appraisal.models import Appraisal
import datetime
import re

def parse_email(string):
    if '<' in string:
        iii = string.index('<')+1
        iif = string.index('>')
        return string[iii:iif].strip().lower()
    else:
        return string.strip().lower()

def parseAddress(address,commune=None):
    addressNumber2 = None
    addressNumber = None

    address = address.lower().strip()

    if commune:
        if address.endswith(commune.lower()):
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
    print(address)
    address = address.replace("avenida","av.")
    address = address.replace('aven','av.')
    address = address.replace('avnda','av.')
    print(address)

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

def parseRut(rut):
    rut = rut.replace('.','').replace(',','').replace('-','').lower()
    return rut[:-1].strip()+'-'+rut[-1].strip()

def parseCommune(string):
    commune = string.strip().title()
    if '(' in commune:
        commune = commune[:commune.index('(')].strip()
    if commune in COMMUNE_NAME_ASCII__UTF.keys():
        commune = COMMUNE_NAME_ASCII__UTF[commune]
    commune = Commune.objects.get(name=commune)
    region = commune.region.code
    commune = commune.id
    return [commune, region]

def parseItau(ws):
    '''
    Devuelve datos de solicitud ITAU
    '''
    data = {}

    for c in Appraisal.petitioner_choices:
        if c[1] == 'Itaú':
            data['solicitante'] = c[0]

    solicitanteEjecutivo = ws['C7'].value
    if isinstance(solicitanteEjecutivo,type('')):
        if solicitanteEjecutivo != '':
            data['solicitanteEjecutivo'] = ws['C7'].value.strip().title()

    solicitanteSucursal = ws['C9'].value
    if isinstance(solicitanteSucursal,type('')):
        if solicitanteSucursal != '':
            data['solicitanteSucursal'] = ws['C9'].value.strip().title()

    solicitanteEjecutivoEmail = ws['J7'].value
    if isinstance(solicitanteEjecutivoEmail,type('')):
        if solicitanteEjecutivoEmail != '':
            data['solicitanteEjecutivoEmail'] = parse_email(solicitanteEjecutivoEmail)

    solicitanteEjecutivoTelefono = ws['O7'].value
    if isinstance(solicitanteEjecutivoTelefono,type('')):
        if solicitanteEjecutivoTelefono != '':
            data['solicitanteEjecutivoTelefono'] = ws['O7'].value.strip().replace(' ','')

    tipoTasacion = ws['G9'].value
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
        if appraisalTimeRequest != '':
            if appraisalTimeRequest.endswith(',') or appraisalTimeRequest.endswith('.'):
                appraisalTimeRequest = appraisalTimeRequest[:-1]
            if '-' in appraisalTimeRequest:
                data['appraisalTimeRequest'] = appraisalTimeRequest.strip().replace('-','/')+' 00:00'
            elif '.' in appraisalTimeRequest:
                data['appraisalTimeRequest'] = appraisalTimeRequest.strip().replace('.','/')+' 00:00'
            elif '/' in appraisalTimeRequest:
                data['appraisalTimeRequest'] = appraisalTimeRequest.strip()+' 00:00'
            else:
                pass
            try:
                a = datetime.datetime.strptime(data['appraisalTimeRequest'],'%d/%m/%Y %H:%M')
            except ValueError:
                try:
                    a = datetime.datetime.strptime(data['appraisalTimeRequest'],'%d/%m/%y %H:%M')
                    data['appraisalTimeRequest'] = data['appraisalTimeRequest'][0:6]+'20'+data['appraisalTimeRequest'][6:]
                except ValueError:
                    data['appraisalTimeRequest'] = ''

    cliente = ws['C14'].value
    if isinstance(cliente,type('')):
        if cliente != '':
            data['cliente'] = ws['C14'].value.strip().title()

    if '-' in ws['C16'].value:
        data['clienteRut'] = parseRut(ws['C16'].value)
    else:
        data['clienteRut'] = parseRut(ws['C16'].value+ws['F16'].value)
    
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

    try :
        commune, region = parseCommune(ws['C45'].value)
        data['addressCommune'] = commune
        data['addressRegion'] = region
    except Commune.DoesNotExist:
        pass

    addressStreet = ws['C41'].value
    if isinstance(addressStreet,type('')):
        if addressStreet != '':
            addressStreet, addressNumber, addressNumber2 = parseAddress(addressStreet,
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
            data['solicitanteEjecutivoRut'] = parseRut(solicitanteEjecutivoRut)

    cliente = ws['H9'].value
    if isinstance(cliente,type('')):
        if cliente != '':
            data['cliente'] = cliente.strip().title()

    clienteRut = ws['H10'].value
    clienteRutDF = ws['J10'].value
    if clienteRut != '' and clienteRutDF != '':
        data['clienteRut'] = parseRut(str(clienteRut)+''+clienteRutDF)

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
            addressStreet, addressNumber, addressNumber2 = parseAddress(address)
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
            commune = Commune.objects.get(name=comuna)
            data['addressCommune'] = commune.id
            data['addressRegion'] = commune.region.code
        if 'ROL' in line.strip():
            data['rol'] = text[i+6+c-1].strip()
        if 'DIRECCION' in line.strip():
            address = ''
            c = 0
            while not 'De propiedad de' in text[i+6+c+1].strip():
                address += text[i+6+c].strip().title()
                c += 1
            addressStreet, addressNumber, addressNumber2 = parseAddress(address)
            data['addressStreet'] = addressStreet
            if addressNumber:
                data['addressNumber'] = addressNumber
            if addressNumber2:
                data['addressNumber2'] = addressNumber2
        if 'Cliente' in line.strip():
            data['cliente'] = text[i+2].strip().title()
        if 'Rut' == line.strip():
            data['clienteRut'] = parseRut(text[i+2])
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
            data['clienteRut'] = parseRut(line.split(':')[1])
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
            data['propietarioRut'] = parseRut(line.split(':')[1])
        elif 'Nombre Contacto' in line.strip():
            data['contacto'] = line.split(':')[1].strip().title()
        elif 'Telefono movil' in line.strip():
            data['contactoTelefono'] = text[i+1].split(':')[1].strip().replace(' ','')
        elif 'Direccion' in line.strip():
            address = line.split(':')[1].strip()
            addressStreet, addressNumber, addressNumber2 = parseAddress(address)
            data['addressStreet'] = addressStreet
            if addressNumber:
                data['addressNumber'] = addressNumber
            if addressNumber2:
                data['addressNumber2'] = addressNumber2
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
            elif 'AVANCE' in propertyType:
                data['tipoTasacion'] = Appraisal.AVANCE_DE_OBRA
        elif 'Rol :' in line.strip():
            data['rol'] = line.split(':')[1].strip()
        elif 'Comuna' in line.strip():
            commune = line.split(':')[1].strip().title()
            commune, region = parseCommune(commune)
            data['addressCommune'] = commune
            data['addressRegion'] = region
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