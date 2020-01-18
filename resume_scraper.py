from pdfminer.high_level import *

resume_data = extract_text("resumes/Will Lu Resume.pdf")

print(resume_data)
