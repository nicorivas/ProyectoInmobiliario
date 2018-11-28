from openpyxl import load_workbook

def importAppraisal(request):
    data = {}
    file = request.FILES['archivo']