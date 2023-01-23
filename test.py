# import os

# path = "CLONE RESULT/Command Day Secondary School, Enugu _ Manage Student Grade Report_files"

# for filename in os.listdir(path):
#     if filename.endswith("..js"):
#         os.rename(os.path.join(path, filename), os.path.join(path, filename[:-4] + ".js"))

# import PyPDF2

# pdf_file = open('CLONE RESULT/ADI.pdf', 'rb')
# pdf_reader = PyPDF2.PdfReader(pdf_file)

# html_file = open('output.html', 'w')

# for page in range(len(pdf_reader.pages)):
# 	pdf_page = pdf_reader.pages[page]
# 	html_file.write(pdf_page.extract_text())

# pdf_file.close()
# html_file.close()


# import fitz
# print(fitz.__doc__)

# doc = fitz.open('CLONE RESULT/ADI.pdf')

# page = doc.load_page(0)
# # print(page)

# # pix = page.get_pixmap()
# # print(pix)

# # pix.save("page-%i.png" % page.number)

# text = page.get_text('html')
# file = open("page-%i.html" % page.number, 'w')
# file.write(text)
# file.close()
# # print(text)