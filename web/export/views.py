from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import ExportForm
from django.http import JsonResponse
from .fill import read_excel
from openpyxl import load_workbook
import zipfile

@login_required(login_url='/user/login')
def main(request):
    form = ExportForm()
    context = {'form':form}
    return render(request, 'export/index.html', context)

def export(request):

    print(request.POST)
    print(request.FILES)


    data = {}

    if 'archivo' not in request.FILES.keys():

        data['error'] = 'Debe elegir un archivo o ingresar una url antes de importar.'
        return JsonResponse(data)

    else:

        file = request.FILES['archivo']

        print(file)

        filetype = file._name.split('.')[1]

        if filetype == 'xls':

            data['error'] = "No es posible importar archivos excel '.xls'. Se recomienda guardar el archivo en formato '.xlsx'."
            return JsonResponse(data)

        elif filetype == 'xlsx':

            try:
                wb = load_workbook(filename=file,read_only=True,data_only=True)
            except zipfile.BadZipFile:
                data['error'] = "Archivo parece estar asegurado. Se recomienda abrir y volver a guardar el archivo."
                return JsonResponse(data)

            appraisal = read_excel(wb)

            print(appraisal)


    data = {"a":"b"}

    return JsonResponse(data)

    #app = read_excel("Formato Garantias Generales 3436.xlsx")

    #fill_web(app)