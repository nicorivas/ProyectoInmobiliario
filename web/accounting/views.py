from django.shortcuts import render
from appraisal.models import Appraisal, AppraisalEvaluation
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseNotModified
import xlsxwriter
from pytz import timezone
from _datetime import datetime
import io
from django.http import HttpResponseBadRequest
from .forms import AccountingForm


# Create your views here.

def getTimeFramedAppraisals(tasador, initial, end):
    #Obtiene las tasaciones de un tasador (o todos) en un marco de tiempo
    tasador = int(tasador)
    if tasador==0:
        appraisals = Appraisal.objects.filter(timeFinished__range=[initial, end])
    else:
        appraisals = Appraisal.objects.filter(tasadorUser=tasador, timeFinished__range=[initial, end])
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
    worksheet.write(0, 8, "Gastos tasador")
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
        worksheet.write(row, col + 5, appraisal.getAppraisalPrice())
        worksheet.write(row, col + 6, appraisal.valorUF)
        worksheet.write(row, col + 7, evaluation)
        worksheet.write(row, col + 8, appraisal.getTotalAppraisalExpenses())
        row += 1
    workbook.close()
    output.seek(0)
    filename = 'contabilidad.xlsx'
    response = HttpResponse(output.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    return response

@login_required(login_url='/user/login')
def ajax_accountingView(request):
    tasador = request.GET['tasador']
    try:
        initial = datetime.strptime(request.GET['accountingTimeRequest'] + ":00", '%d/%m/%Y %H:%M:%S')
        end = datetime.strptime(request.GET['accountingTimeDue'] + ":00", '%d/%m/%Y %H:%M:%S')
    except ValueError:
        return HttpResponseBadRequest()
    appraisals = getTimeFramedAppraisals(tasador, initial, end)
    context = {'appraisals': appraisals}
    return render(request, 'accounting/accounting_table.html', context)



@login_required(login_url='/user/login')
def accountingView(request):

    tasadores = list(User.objects.filter(groups__name__in=['tasador']).order_by('last_name'))
    form = AccountingForm()
    context = {'tasadores': tasadores, 'form':form}

    if request.method == "POST":
        print(request.POST)
        tasador = request.POST['tasador']
        try:
            initial = datetime.strptime(request.POST['accountingTimeRequest']+":00", '%d/%m/%Y %H:%M:%S')
            end = datetime.strptime(request.POST['accountingTimeDue']+":00",'%d/%m/%Y %H:%M:%S')
        except ValueError:
            return HttpResponseNotModified()
        localtz = timezone('Chile/Continental')
        initial = localtz.localize(datetime.strptime(str(initial), '%Y-%m-%d %H:%M:%S'))
        end = localtz.localize((datetime.strptime(str(end), '%Y-%m-%d %H:%M:%S')))
        appraisals = getTimeFramedAppraisals(tasador, initial, end)
        return exportAccounting(appraisals)


    return render(request, 'accounting/accounting.html', context )