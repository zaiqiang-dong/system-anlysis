from reportlab.lib.pagesizes import A0, portrait, landscape
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.colors import HexColor
import os
import math
from reportlab.pdfgen import canvas
import pandas as pd

(w, h) = portrait(A0)
headStr=''

paidingTop = 160
paidingBottom = 160
paidingLeft = paidingRight = (w - 1920) / 2
contentPaiding = 100

colorT = HexColor('#2c3e50')
colorG = HexColor('#3eaf7c')

allParagraph=[]

styleSheet = getSampleStyleSheet()
h1 = styleSheet['Heading1']
h1.pageBreakBefore = 1
h1.keepWithNext = 1
h1.outlineLevel = 0
h1.fontSize = 72
h1.leading = 72

styleSheet = getSampleStyleSheet()
h2 = styleSheet['Heading2']
h2.keepWithNext = 1
h2.outlineLevel = 1
h2.fontSize = 64
h2.leading = 64

styleSheet = getSampleStyleSheet()
h3 = styleSheet['Heading3']
h3.keepWithNext = 1
h3.outlineLevel = 2
h3.fontSize = 48
h3.leading = 48


def processRy(c, ry):
    if (ry - paidingBottom - contentPaiding) > 30:
        return ry
    else:
        c.showPage()
        reportDrawHead(c)
        return h
def createIndext(c, p):
    lv = 0
    sty = p.style.name
    if sty == "Heading1":
        lv = 0
    elif sty == "Heading2":
        lv = 1
    elif sty == "Heading3":
        lv = 2
    key = str(hash(p))
    txt = p.getPlainText()
    c.bookmarkPage(key)
    c.addOutlineEntry(txt, key, level=lv, closed=0)

def reportDrawHead(c):
    #head
    c.setStrokeColor(colorG)
    c.setLineWidth(8)
    c.line(paidingLeft, h - paidingTop , w - paidingRight, h - paidingTop)
    c.setLineWidth(4)
    c.line(paidingLeft, h - paidingTop -10 , w - paidingRight, h - paidingTop -10)
    #footer
    c.setLineWidth(8)
    c.line(paidingLeft, paidingBottom , w / 2 - 100 , paidingBottom)
    c.line(w / 2  + 100, paidingBottom , w - paidingRight , paidingBottom)

    styleSheet = getSampleStyleSheet()
    hpnum= styleSheet['Heading1']
    hpnum.pageBreakBefore = 1
    hpnum.keepWithNext = 1
    hpnum.outlineLevel = 0
    hpnum.fontSize = 48
    hpnum.leading = 12

    hpnum.textColor = colorG
    pnum = c.getPageNumber()
    p = Paragraph(str(pnum), hpnum)
    wp,hp = p.wrap(100, 48)
    p.drawOn(c, w / 2 - wp / 2, paidingBottom + hp )

    th = styleSheet['Italic']
    th.pageBreakBefore = 1
    th.keepWithNext = 1
    th.fontSize = 36
    th.leading = 36
    th.textColor = colorT

    p = Paragraph(headStr, th)
    wp,hp = p.wrap(1000, 0)
    p.drawOn(c, w - wp, h - paidingTop + 10)



def reportDrawH1(c,name, y = 0):

    hp = Paragraph(name, h1)
    whp,hhp=hp.wrap(1000,1000)

    ry = h - paidingTop - hhp  - contentPaiding

    hp.drawOn(c, paidingLeft, ry)
    allParagraph.append(hp)

    # key = str(hash(hp))
    # txt = name
    # c.bookmarkPage(key)
    # c.addOutlineEntry(txt, key, level=0, closed=0)
    createIndext(c, hp)
    return processRy(c,ry)

def reportDrawH2(c,name, y):

    hp = Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;" + name, h2)
    whp,hhp=hp.wrap(1000,1000)

    ry = y - hhp - contentPaiding
    hp.drawOn(c, paidingLeft, ry)

    createIndext(c, hp)
    # key = str(hash(hp))
    # txt = name
    # c.bookmarkPage(key)
    # c.addOutlineEntry(txt, key, level=1, closed=0)

    return processRy(c,ry)

def reportDrawH3(c,name, y):

    hp = Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;" + name, h3)
    whp,hhp=hp.wrap(2000,0)
    if y - hhp - paidingBottom - contentPaiding*2 < 0:
        c.showPage()
        reportDrawHead(c)
        y = h - contentPaiding
    ry = y - hhp - contentPaiding * 2
    hp.drawOn(c, paidingLeft, ry)

    createIndext(c, hp)
    # key = str(hash(hp))
    # txt = name
    # c.bookmarkPage(key)
    # c.addOutlineEntry(txt, key, level=2, closed=0)

    return processRy(c,ry)

def reportDrawCover(c, CodeVersion, testTime):
    styles = getSampleStyleSheet()
    styleH1 = styles['Heading1']
    styleH1.fontSize = 80
    styleH1.leading = 80
    styleH1.textColor = colorT
    cover = [[CodeVersion + "-TEST-REPORT"]]
    data = [[Paragraph(str(cell), styleH1) for cell in row] for row in cover]
    t = Table(data)
    wt, ht = t.wrap(0, 0)
    t.drawOn(c, (w - wt ) / 2 , (h / 3) * 2)

    styleH1.fontSize = 50
    styleH1.leading = 50
    cover = [[testTime]]
    data = [[Paragraph(str(cell), styleH1) for cell in row] for row in cover]
    st = Table(data)
    st.wrap(0, 0)
    st.drawOn(c, (w - wt) / 2 , (h / 3) * 2 - 160)
    createIndext(c, Paragraph("Cover", h1))


def reportDrawTable(c, ifile, ry, colw=None):
    styles = getSampleStyleSheet()
    styleN = styles['Normal']
    styleN.wordWrap = 'CJK'
    styleN.fontSize = 24
    styleN.leading = 40

    df = pd.read_csv(ifile)
    cols = df.columns.tolist()
    data = df.values.tolist()
    data.insert(0, cols)

    tableStyle = [
        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
        ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
        ]

    data = [[Paragraph(str(cell), styleN) for cell in row] for row in data]

    t = Table(data, colWidths=colw)
    wt, ht = t.wrap(0, 0)
    remainY = ry - paidingBottom - ht

    datap= []
    dataa= []

    needSplit = False

    if remainY < 0:
        remainY = -remainY
        p = remainY / ht
        lendata = len(data)
        splitP = math.floor(lendata * p)
        datap = data[0:p]
        dataa = data[p:]
        needSplit = True

    if not needSplit:
        print(" table no need split.")
        t.setStyle(TableStyle(tableStyle))
        t.split(0,0)
        t.drawOn(c, paidingLeft , ry - contentPaiding - ht - paidingTop)
        return processRy(c,ry)
    else:
        t = Table(datap, colWidths=colw)
        t.setStyle(TableStyle(tableStyle))
        t.split(0,0)
        pw, ph = t.wrap(0, 0)
        t.drawOn(c, paidingLeft , ry - ph)

        t = Table(dataa, colWidths=colw)
        t.setStyle(TableStyle(tableStyle))
        t.split(0,0)
        aw, ah = t.wrap(0, 0)
        ry = h - ah - paidingTop - contentPaiding
        t.drawOn(c, paidingLeft , ry)

        return processRy(c,ry)


def reportDrawImage(c,path, imgW, imgH, y):
    txt = path.split('/')[-1].split('.')[0]
    ry = reportDrawH3(c, txt, y)
    ry = ry - imgH - paidingBottom
    if ry <= 0:
        c.showPage()
        reportDrawHead(c)
        ry = h - paidingBottom - imgH - contentPaiding
    c.drawImage(path, paidingLeft, ry, imgW, imgH)
    return processRy(c,ry)



def reportDrawMemory(c,img_path, imgW, imgH, y):
    pages = 0
    l = os.listdir(img_path)
    i = 0
    ry = y
    while i < len(l):
        f = img_path + "/"+  str(l[i])
        print(f)
        ry = reportDrawImage(c, f, imgW, imgH, ry)
        i += 1
    return ry

def createReport(outdir, testVersion, testTime):
    c = canvas.Canvas(outdir + "/Report.pdf", pagesize = portrait(A0))
    global headStr
    headStr = testVersion + "-REPORT"
    reportDrawHead(c)
    reportDrawCover(c,testVersion, testTime)
    c.showPage()


    l = os.listdir(outdir + "/process-loginfo/")
    logcatResult = outdir+"/process-loginfo/"+l[0]
    print(logcatResult)
    reportDrawHead(c)
    ry = reportDrawH1(c, "1 Logcat Log Analyst")
    ry = reportDrawH2(c, "1.1 Analyst out", ry)
    print(logcatResult)
    reportDrawTable(c, str(logcatResult), ry, colw=[100,1500, 200,120])
    c.showPage()

    memoryResultProcessPath = outdir + "/process-memory-info/"
    memoryResultPssPath = outdir + "/total-pss-info/"
    memoryResultMemPath = outdir + "/total-meminfo/"

    reportDrawHead(c)
    ry = reportDrawH1(c, "2 Memory Info Analyst")
    ry = reportDrawH2(c, "2.1 Memory Total Info", ry)
    ry = reportDrawMemory(c,memoryResultMemPath,1920 , 1200, ry)
    c.showPage()
    reportDrawHead(c)
    ry = h - paidingTop
    ry = reportDrawH2(c, "2.2 Memory Pss info", ry)
    ry = reportDrawMemory(c,memoryResultPssPath ,1920 ,720, ry)
    c.showPage()
    reportDrawHead(c)
    ry = h - paidingTop
    ry = reportDrawH2(c, "2.3 Precess Memory info", ry)
    reportDrawMemory(c,memoryResultProcessPath,1920 ,640, ry)
    c.showPage()
    c.save()

    pass


if __name__ == "__main__":
    # c = canvas.Canvas("./adbc.pdf", pagesize = portrait(A0))

    # reportDrawHead(c)
    # reportDrawCover(c,"NREAL-21231-26724345345", "2020-03-27-19-32-22")
    # c.showPage()
    # reportDrawHead(c)
    # ry = reportDrawH1(c, "1 Logcat Log Analyst")
    # ry = reportDrawH2(c, "1.1 Analyst out", ry)

    # reportDrawTable(c, "../out/report-2020-03-27-19-32-22/process-loginfo/process-loginfo-2020-03-27-19-34-08.csv", ry, colw=[100,1500, 200,120])
    # c.showPage()
    # reportDrawHead(c)
    # ry = reportDrawH1(c, "2 Memory Info Analyst")
    # ry = reportDrawH2(c, "2.1 Precess Memory info", ry)
    # reportDrawMemory(c,"../out/report-2020-03-27-19-32-22/process-memory-info/",1920 ,640, ry)
    # c.showPage()
    # c.save()

    createReport("../out/report-2020-03-27-19-32-22", "NREAL-21231-26724345345", "2020-03-27-19-32-22")
