from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, inch
from reportlab.platypus import Image, Paragraph, SimpleDocTemplate, Table
from reportlab.lib.styles import getSampleStyleSheet
doc = SimpleDocTemplate("complex_cell_values.pdf", pagesize=letter)
# container for the 'Flowable' objects
elements = []
styleSheet = getSampleStyleSheet()

P0 = Paragraph('A paragraph1', styleSheet["BodyText"])
multiline_text =  '''
The ReportLab Left
Logo
Image'''
P = Paragraph(multiline_text,
              styleSheet["BodyText"])
data= [['A', 'B', 'C', P0, 'D'],
       ['00', '01', '02', [P,P], '04'],
       ['10', '11', '12', [P,P], '14'],
       ['20', '21', '22', '23', '24'],
       ['30', '31', '32', '33', '34']]
table = Table(data,style=[('GRID',(1,1),(-2,-2),1,colors.green),
                          ('BOX',(0,0),(1,-1),2,colors.red),
                          ('LINEABOVE',(1,2),(-2,2),1,colors.blue),
                          ('LINEBEFORE',(2,1),(2,-2),1,colors.pink),
                          ('BACKGROUND', (0, 0), (0, 1), colors.pink),
                          ('BACKGROUND', (1, 1), (1, 2), colors.lavender),
                          ('BACKGROUND', (2, 2), (2, 3), colors.orange),
                          ('BOX',(0,0),(-1,-1),2,colors.black),
                          ('GRID',(0,0),(-1,-1),0.5,colors.black),
                          ('VALIGN',(3,0),(3,0),'BOTTOM'),
                          ('BACKGROUND',(3,0),(3,0),colors.limegreen),
                          ('BACKGROUND',(3,1),(3,1),colors.khaki),
                          ('ALIGN',(3,1),(3,1),'CENTER'),
                          ('BACKGROUND',(3,2),(3,2),colors.beige),
                          ('ALIGN',(3,2),(3,2),'LEFT'),
                          ])
table._argW[3] = 1.5*inch
elements.append(table)
# write the document to disk
doc.build(elements)