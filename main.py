import os
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib.colors import blue, gray, white
from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.units import mm, cm

def reduz_icon(icon):
    icon = icon.resize((100, 100))
    return icon


def gera_head(c):
    tj = ImageReader('imgs/logo_tj.png')
    c.drawImage(tj, 20, 650, width=200, height=100, mask='auto')
    return c

def pdf_generator(metadaos):
    autor = metadaos.iloc[0]['data']
    reu = metadaos.iloc[1]['data']
    num_processo = metadaos.iloc[2]['data']
    acao = metadaos.iloc[3]['data']
    pedido_autor = metadaos.iloc[4]['data']
    pedido_rel = metadaos.iloc[5]['data']
    acordo = metadaos.iloc[6]['data']
    decisao = metadaos.iloc[7]['data']

    lista_pedido_autor = pedido_autor.split(";")
    lista_pedido_reu = pedido_rel.split(";")
    lista_acordo = acordo.split(";")
    lista_decisao = decisao.split(";")




    BLUE = (0, 0, 1)  # ou BLUE = (0, 0, 255)
    # Criar um novo PDF com uma página em branco
    c = canvas.Canvas("output.pdf", pagesize=letter)
    c.setFont("Helvetica-Bold", 12)

    width, height = c._pagesize


    c.radialGradient(100 * mm, 150 * mm, 300 * mm, (white, gray), extend=False)

    c.setFillColorRGB(1 / 255 * 1, 1 / 255 * 83, 1 / 255 * 165)
    c.drawString(80, 570, 'AUTOR:'+autor)
    c.drawString(350, 570, 'REU:'+reu)
    c.drawString(200, 520, 'Processo n.' + num_processo)
    c.drawString(190, 490, 'Ação:' + acao)

    c.setFillColorRGB(0.5, 0.5, 0.5)
    c.drawString(250, 310, 'RESUMO DO PROCESSO')

    c.setFillColorRGB(1 / 255 * 1, 1 / 255 * 83, 1 / 255 * 165)
    y = 550 / 2 - 12
    c.setLineWidth(0)
    for item in lista_pedido_autor:
        y -= 12 * 1.2
        c.circle(110, y+4, 2, fill=1)
        c.drawString(120, y, item)

    y = 550 / 2 - 12
    for item in lista_pedido_reu:
        y -= 12 * 1.2
        c.circle(360, y+4, 2, fill=1)
        c.drawString(370, y, item)

    y = 300 / 2 - 12
    for item in lista_acordo:
        y -= 12 * 1.2
        c.circle(160, y+4, 2, fill=1)
        c.drawString(180, y, item)


    c.setFillColorRGB(0.5, 0.5, 0.5)
    c.drawString(290, 150, 'ACORDO')

#


    c.setPageSize((612, 792))
    c = gera_head(c)



    img = ImageReader('foto.png')
    resumo = ImageReader('imgs/img_resumo.png')




    c.drawImage(img, 150, 350, width=320, height=120, mask='auto')

    c.drawImage(resumo, 230, 600, width=145, height=14, mask='auto')


    c.showPage()
    c.radialGradient(100 * mm, 150 * mm, 300 * mm, (white, gray), extend=False)
    c = gera_head(c)
    c.setFillColorRGB(0.5, 0.5, 0.5)
    c.drawString(250, 600, 'DECISÕES DA JUÍZA:')

    y = 800 / 2 - 12
    for item in lista_decisao:
        y -= 12 * 1.2
        c.circle(160, y + 4, 2, fill=1)
        c.drawString(180, y, item)

    c.save()

def flow_generate(df):
    img = Image.new('RGBA', (800, 300), color=(255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
   # draw.line((700, 125, 100, 125), fill='black', width=5)

    arrow_size = 20  # tamanho da seta em pixels
    arrow_base = (40 - arrow_size, 250)  # ponto da base da seta
    arrow_tip = (760 + arrow_size, 250)  # ponto da ponta da seta
    draw.line((arrow_base, arrow_tip), fill='black', width=5)

    #RESUMO DA SENTENÇA

    draw.polygon([arrow_tip, (arrow_tip[0] - arrow_size, arrow_tip[1] + arrow_size),
                  (arrow_tip[0] - arrow_size, arrow_tip[1] - arrow_size)], fill='black')

    if df.shape[0] == 2:
        d = int(2220 / df.shape[0])
    if df.shape[0] == 3:
        d = int(1655/df.shape[0])
    if df.shape[0] == 4:
        d = int(1480/df.shape[0])
    if df.shape[0] == 5:
        d = int(1400/df.shape[0])


    k = 200
    for index, row in df.iterrows():
        ico = ''
        if row[0] == 'CASAMENTO':
            ico = 'casal.png'
        elif row[0] == 'NASCIMENTO':
            ico = 'bebe.png'
        elif row[0] == 'PATRIMONIO':
            ico = 'patrimonio.png'
        elif row[0] == 'DIVORCIO':
            ico = 'divorcio.png'
        elif row[0] == 'INICIO':
            ico = 'coracao.png'

        i = Image.open('icos/'+ico)
        i = reduz_icon(i)


        text = os.path.splitext(row[1])[0]
        bbox = draw.textbbox((0, 0), text)
        text_width = bbox[2] - bbox[0]

        x = (k - i.width) // 2
        y = (250 - i.height) // 2

        text_x = (k-50 - text_width) // 2
        text_y = y + i.height + 20
        img.paste(i, (x, y), i)


        font = ImageFont.truetype("fonts/arial.ttf", 20)
        draw.text((text_x, text_y), text, fill='black', font=font)



        k = k + d

    img.save('foto.png', dpi=(600, 600))

if __name__ == '__main__':
    # img = Image.new('RGBA', (333, 149), color=(255, 255, 255, 0))
    # i = Image.open('imgs/logo_tj.png')
    # i = i.resize((333, 149))
    # img.paste(i, (0, 0), i)
    # img.save('logo_tj.png', dpi=(600, 600))

    df = pd.read_csv('data.csv')
    flow_generate(df)

    metadaos = pd.read_csv('metadata.csv')
    pdf_generator(metadaos)
