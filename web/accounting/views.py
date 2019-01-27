from django.shortcuts import render
from appraisal.models import Appraisal, AppraisalEvaluation
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import xlsxwriter
from pytz import timezone
from _datetime import datetime
import io


# Create your views here.

def getTimeFramedAppraisals(tasador, initial, end):
    #Obtiene las tasaciones de un tasador (o todos) en un marco de tiempo
    tasador = int(tasador)
    if tasador==0:
        appraisals = Appraisal.objects.filter(timeFinished__range=[initial, end])
        print(appraisals)
        print('todos')
    else:
        appraisals = Appraisal.objects.filter(tasadorUser=tasador, timeFinished__range=[initial, end])
        print(appraisals)
        print(tasador)
    return appraisals


def exportAccounting(appraisals):
    #recibe una lista de appraisals u devuelve un excel con los campos requeridos para hacer contabilidad de tasaciones
    #workbook = xlsxwriter.Workbook('C:/Users/Pablo Ferreiro/Desktop/users.xlsx')
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    worksheet = workbook.add_worksheet()
    worksheet.write(0, 0, "ID Tasación")
    worksheet.write(0, 1, "Solicitante")
    worksheet.write(0, 2, "Codigo Tasación")
    worksheet.write(0, 3, "Tipo de Tasación")
    worksheet.write(0, 4, "Tasador")
    worksheet.write(0, 5, "Valor Tasado")
    worksheet.write(0, 6, "Valor UF tasación")
    worksheet.write(0, 7, "Evaluación de la tasación")
    row = 1
    col = 0
    for appraisal in appraisals:

        try:
            evaluation = AppraisalEvaluation.objects.get(appraisal=appraisal).evaluationResult
        except AppraisalEvaluation.DoesNotExist:
            evaluation = 0
        try:
            user = User.objects.get(username=appraisal.tasadorUser)
            tasador = user.first_name + ' ' + user.last_name
        except (User.DoesNotExist, TypeError):
            tasador = None
        worksheet.write(row, col, appraisal.id)
        worksheet.write(row, col + 1, appraisal.get_solicitante_display())
        worksheet.write(row, col + 2, appraisal.solicitanteCodigo)
        worksheet.write(row, col + 3, appraisal.get_tipoTasacion_display())
        worksheet.write(row, col + 4, tasador)
        worksheet.write(row, col + 5, appraisal.price)
        worksheet.write(row, col + 6, appraisal.valorUF)
        worksheet.write(row, col + 7, evaluation)
        row += 1
    workbook.close()
    output.seek(0)
    filename = 'contabilidad.xlsx'
    response = HttpResponse(output.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    return response

@login_required(login_url='/user/login')
def accountingView(request):

    if request.method == "POST":
        print(request.POST)
        tasador = request.POST['tasador']
        initial = datetime.strptime(request.POST['appraisalTimeRequest']+":00", '%d/%m/%Y %H:%M:%S')
        end = datetime.strptime(request.POST['appraisalTimeRequest2']+":00",'%d/%m/%Y %H:%M:%S')
        localtz = timezone('Chile/Continental')
        initial = localtz.localize(datetime.strptime(str(initial), '%Y-%m-%d %H:%M:%S'))
        end = localtz.localize((datetime.strptime(str(end), '%Y-%m-%d %H:%M:%S')))
        appraisals = getTimeFramedAppraisals(tasador, initial, end)
        return exportAccounting(appraisals)


    tasadores = list(User.objects.filter(groups__name__in=['tasador']))
    context = {'tasadores': tasadores}
    return render(request, 'accounting/accounting.html', context )