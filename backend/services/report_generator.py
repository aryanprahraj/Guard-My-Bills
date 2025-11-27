from reportlab.lib.pagesizes import letter, landscape
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle, SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
import os
import matplotlib.pyplot as plt
import base64
from io import BytesIO
from reportlab.platypus import Image as RLImage

def get_logo_image(width=120):
	logo_path = os.path.join(os.path.dirname(__file__), '../assets/guard_my_bills_logo.png')
	if os.path.exists(logo_path):
		from PIL import Image as PILImage, ImageFilter
		pil_img = PILImage.open(logo_path).convert('RGBA')
		pil_img = pil_img.filter(ImageFilter.SHARPEN)
		# Calculate aspect ratio and fit within 140x50 without stretching
		max_width, max_height = 140, 50
		orig_width, orig_height = pil_img.size
		ratio = min(max_width / orig_width, max_height / orig_height)
		new_width = int(orig_width * ratio)
		new_height = int(orig_height * ratio)
		pil_img = pil_img.resize((new_width, new_height), PILImage.LANCZOS)
		buf = BytesIO()
		pil_img.save(buf, format='PNG')
		buf.seek(0)
		img = Image(buf, new_width, new_height)
		img.hAlign = 'CENTER'
		return img
	return None

def chart_to_rlimage(fig, width=400):
    buf = BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    img = RLImage(buf, width, width * 0.6)
    return img

def generate_pdf_report(summary, transactions, spending_analytics, charts, output_path):
	doc = SimpleDocTemplate(output_path, pagesize=landscape(letter), leftMargin=12, rightMargin=12, topMargin=24, bottomMargin=24)
	styles = getSampleStyleSheet()
	elements = []
	# Logo at the top
	logo = get_logo_image(width=140)
	if logo:
		elements.append(logo)
		elements.append(Spacer(1, 24))
	# Title
	elements.append(Paragraph("Guard My Bills - Fraud Analysis Report", styles['Title']))
	elements.append(Spacer(1, 12))
	# Summary
	elements.append(Paragraph("<b>Summary</b>", styles['Heading2']))
	for k, v in summary.items():
		elements.append(Paragraph(f"{k.replace('_',' ').capitalize()}: {v}", styles['Normal']))
	elements.append(Spacer(1, 12))
	# Suspicious transactions table
	elements.append(Paragraph("<b>Suspicious Transactions</b>", styles['Heading2']))
	suspicious = [t for t in transactions if t.get('risk_level') in ('HIGH','MEDIUM')]
	if suspicious:
		table_data = [["Date", "Time", "Merchant", "City", "Country", "Amount", "Risk", "Fraud Prob.", "Reasons"]]
		for t in suspicious:
			table_data.append([
				t.get('date'), t.get('time'), t.get('merchant_name'), t.get('city'), t.get('country'),
				f"{t.get('amount'):.2f}", t.get('risk_level'), f"{t.get('fraud_probability'):.2f}", ', '.join(t.get('reasons', []))
			])
		# Wider columns for Country and Reasons, narrower for others
		col_widths = [55, 38, 70, 55, 120, 55, 38, 55, 220]
		tbl = Table(table_data, colWidths=col_widths, repeatRows=1)
		tbl.setStyle(TableStyle([
			('BACKGROUND', (0,0), (-1,0), colors.grey),
			('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
			('ALIGN', (0,0), (-1,0), 'CENTER'),
			('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
			('FONTSIZE', (0,0), (-1,0), 10),
			('BOTTOMPADDING', (0,0), (-1,0), 10),
			('BACKGROUND', (0,1), (-1,-1), colors.beige),
			('GRID', (0,0), (-1,-1), 1, colors.black),
			('FONTSIZE', (0,1), (-1,-1), 8),
			('VALIGN', (0,1), (-1,-1), 'TOP'),
			('ALIGN', (0,1), (-3,-1), 'CENTER'),
			('ALIGN', (4,1), (4,-1), 'LEFT'),  # Country left-align
			('ALIGN', (8,1), (8,-1), 'LEFT'),  # Reasons left-align
			('LEFTPADDING', (0,0), (-1,-1), 2),
			('RIGHTPADDING', (0,0), (-1,-1), 2),
		]))
		# Enable word wrap for Country and Reasons columns
		from reportlab.lib.styles import ParagraphStyle
		wrap_style = ParagraphStyle('wrap', fontSize=8, leading=10)
		for row_idx in range(1, len(table_data)):
			tbl._cellvalues[row_idx][4] = Paragraph(str(tbl._cellvalues[row_idx][4]), wrap_style)
			tbl._cellvalues[row_idx][8] = Paragraph(str(tbl._cellvalues[row_idx][8]), wrap_style)
		elements.append(tbl)
	else:
		elements.append(Paragraph("No suspicious transactions detected.", styles['Normal']))
	elements.append(Spacer(1, 12))
	# Spending Analytics section removed as requested
	doc.build(elements)

def generate_spending_pdf_report(summary, output_path):
	from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
	from reportlab.lib.styles import getSampleStyleSheet
	from reportlab.lib.pagesizes import letter, landscape
	import os
	from io import BytesIO
	styles = getSampleStyleSheet()
	elements = []
	# Logo at the top
	def get_logo_image(width=120):
		logo_path = os.path.join(os.path.dirname(__file__), '../assets/guard_my_bills_logo.png')
		if os.path.exists(logo_path):
			from PIL import Image as PILImage, ImageFilter
			pil_img = PILImage.open(logo_path).convert('RGBA')
			pil_img = pil_img.filter(ImageFilter.SHARPEN)
			max_width, max_height = 140, 50
			orig_width, orig_height = pil_img.size
			ratio = min(max_width / orig_width, max_height / orig_height)
			new_width = int(orig_width * ratio)
			new_height = int(orig_height * ratio)
			pil_img = pil_img.resize((new_width, new_height), PILImage.LANCZOS)
			buf = BytesIO()
			pil_img.save(buf, format='PNG')
			buf.seek(0)
			img = Image(buf, new_width, new_height)
			img.hAlign = 'CENTER'
			return img
		return None
	logo = get_logo_image(width=140)
	if logo:
		elements.append(logo)
		elements.append(Spacer(1, 24))
	# Title
	elements.append(Paragraph("Guard My Bills - Spending Analysis Report", styles['Title']))
	elements.append(Spacer(1, 12))
	# Summary
	elements.append(Paragraph("<b>Spending Summary</b>", styles['Heading2']))
	# Define expected keys for summary, but allow for any keys present
	expected_keys = [
		'amount', 'total_transactions', 'total_spent', 'total_income', 'largest_expense', 'largest_income',
		'average_expense', 'average_income', 'most_frequent_category', 'most_frequent_merchant', 'period_start', 'period_end'
	]
	# Print all keys in summary, but show N/A for missing or None values
	keys_to_show = list(summary.keys()) if summary else expected_keys
	shown = set()
	for k in keys_to_show:
		if k in shown:
			continue
		v = summary.get(k, 'N/A')
		if v is None:
			v = 'N/A'
		elements.append(Paragraph(f"{k.replace('_',' ').capitalize()}: {v}", styles['Normal']))
		shown.add(k)
	# Also show any expected keys not present
	for k in expected_keys:
		if k not in shown:
			elements.append(Paragraph(f"{k.replace('_',' ').capitalize()}: N/A", styles['Normal']))
			shown.add(k)
	elements.append(Spacer(1, 12))
	doc = SimpleDocTemplate(output_path, pagesize=landscape(letter), leftMargin=12, rightMargin=12, topMargin=24, bottomMargin=24)
	doc.build(elements)
