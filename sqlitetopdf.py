import psycopg2
from datetime import date
from fpdf import FPDF
import matplotlib.pyplot as plt
from database import DBHelper
db = DBHelper()

class CustomPDF(FPDF):
	
	def header(self):
		today = date.today()
		# dd/mm/YY
		d1 = today.strftime("%d/%m/%Y")
		self.set_y(32)
		self.set_font('Arial', 'B', 15)
		self.image('logo.png', 10, 5, 30,30, link = 'http://skbot.epizy.com/')
		self.set_font('Arial', 'I', 14)
		self.cell(230)
		self.cell(0, -30, d1, ln=1)

		# Line break
		self.ln(10)
		
	def footer(self):
		self.set_y(-10)
		
		self.set_font('Arial', 'I', 12)
		self.cell(250)
		self.cell(0, 0, 'By Sumit Kothari', ln=1)
		
		# Add a page number
		page = 'Page ' + str(self.page_no()) + '/{nb}'
		self.cell(0, 10, page, 0, 0, 'C')

	def chart(self, v, Name):
		s = db.getpdf(v)
		s = list(s)
		fig = plt.figure(figsize=(6,4))
		ax = fig.add_axes((0.15,0,.5,1))
		#plt.title('%Present for each Subject')
		labels = 'Physics', 'Chemistry', 'Maths', 'CP'
		sizes = [s[2], s[3], s[4], s[5]]
		colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue']
		explode = (0.1, 0, 0, 0)  # explode 1st slice

		# Plot
		plt.pie(sizes, explode=explode, labels=labels, colors=colors,
		autopct='%1.1f%%', shadow=True, startangle=140)
		plt.axis('equal')
		#plt.title("%Present for each Subject", bbox={'facecolor':'0.8', 'pad':5})
		plt.savefig(str(Name)+'.png')



	def simple_table(self, v, Name, spacing=1):
		s = db.getpdf(v)
		s = list(s)
		s.pop(0)
		s.pop(8)
		s[7] = round(s[7],2)
		s = list(map(str, s))
		s[7] = s[7] + "%"
		#print(s)
		data = [['Name','Physics','Chemistry','Maths','CP','Present','Total lecture','Percentage'],
				s
				
				]
		
		pdf = CustomPDF(orientation='L')
		pdf.alias_nb_pages()
		pdf.add_page()
		pdf.cell(150)
		pdf.set_y(43)
		pdf.set_font('Arial', 'I', 20)
		pdf.cell(0, 0, 'Attendence Report for '+str(Name), ln=1)
		pdf.set_y(50)
		pdf.set_font("Helvetica", size=14)

		col_width = pdf.w / 8.5
		row_height = pdf.font_size*1.5
		for row in data:
			for item in row:
				pdf.cell(col_width, row_height*spacing,
						 txt=item, border=1)
			pdf.ln(row_height*spacing)
		pdf.image(str(Name)+'.png', x = 60, y = 70, w = 0, h = 0)
		pdf.output(str(Name)+'.pdf')
	
