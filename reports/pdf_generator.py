import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def build_pdf_report(scan, open_ports, risk):
    os.makedirs('instance/generated_reports', exist_ok=True)
    path = f"instance/generated_reports/report_{scan.id}.pdf"
    c = canvas.Canvas(path, pagesize=A4)
    y=800
    c.setFont("Helvetica-Bold", 14); c.drawString(50,y,"Hybrid: Network Security Auditor")
    y-=25; c.setFont("Helvetica",10)
    c.drawString(50,y,f"Target: {scan.target}  | Risk: {risk['level']} | Score: {risk['score']}")
    y-=20; c.drawString(50,y,"Open Ports:")
    for p in open_ports[:40]:
        y-=15; c.drawString(70,y,f"{p['port']} - {p['service']} ({p['status']})")
        if y<80: c.showPage(); y=800
    y-=20; c.drawString(50,y,"Recommendations:")
    for r in risk['recommendations']:
        y-=15; c.drawString(70,y,f"- {r}")
    c.save(); return path
