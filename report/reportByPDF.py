from reportlab.lib.pagesizes import A0, portrait, landscape
import os
import math
from reportlab.pdfgen import canvas

def convert_images_to_pdf(img_path, pdf_path):
    pages = 0
    (w, h) = portrait(A0)
    c = canvas.Canvas(pdf_path, pagesize = portrait(A0))
    l = os.listdir(img_path)
    a = math.floor((w - 1920) / 2)
    b = math.floor((h - 640*5) / 6)
    # for i in l:
    #     f = img_path + "/"+  str(i)
    #     c.drawImage(f, a, 0, 1920, 640)
    #     c.drawImage(f, a, 660, 1920, 640)
    #     c.drawImage(f, a, 1320, 1920, 640)
    #     c.showPage()
    #     pages = pages + 1
    # c.save()

    i = 0
    while (i + 5) < len(l):
        y = b
        f = img_path + "/"+  str(l[i])
        c.drawImage(f, a, y, 1920, 640)
        i += 1
        y += 640 + b
        f = img_path + "/"+  str(l[i])
        c.drawImage(f, a, y, 1920, 640)
        i += 1
        y += 640 + b
        f = img_path + "/"+  str(l[i])
        c.drawImage(f, a, y, 1920, 640)
        i += 1
        y += 640 + b
        f = img_path + "/"+  str(l[i])
        c.drawImage(f, a, y, 1920, 640)
        i += 1
        y += 640 + b
        f = img_path + "/"+  str(l[i])
        c.drawImage(f, a, y, 1920, 640)
        c.showPage()
    c.save()



convert_images_to_pdf("./process-memory-info","./abc.pdf")
