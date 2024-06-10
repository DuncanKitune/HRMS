from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from .models import Payslip
import pandas as pd
from .models import Employee, io

def generate_payslip_pdf(payslip):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    c.drawString(100, 750, f"Payslip for {payslip.employee.full_name}")
    c.drawString(100, 730, f"Month: {payslip.month}")
    c.drawString(100, 710, f"Gross Pay: {payslip.gross_pay}")
    c.drawString(100, 690, f"Net Pay: {payslip.net_pay}")
    c.drawString(100, 670, f"PAYE: {payslip.paye}")
    c.drawString(100, 650, f"NHIF: {payslip.nhif}")
    c.drawString(100, 630, f"NSSF: {payslip.nssf}")
    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer



def generate_employee_report():
    employees = Employee.objects.all().values()
    df = pd.DataFrame(list(employees))
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer) as writer:
        df.to_excel(writer, index=False)
    buffer.seek(0)
    return buffer