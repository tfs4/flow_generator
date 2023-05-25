import os
import pandas as pd

from reportlab.lib.utils import ImageReader
from reportlab.lib.colors import blue, gray, white
from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.units import mm, cm
from reportlab.lib.colors import HexColor

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph, Frame
from br_gender.base import br_gender_info
import config
import importador
import sumarizador_decisao

import json



def carrega_dados():
    f = open('sentencas/sentenca_1.json')
    data = json.load(f)


    config.AUTOR = data['autor']
    config.REU = data['reu']
    config.NUM_PROCESSO = data['numero']
    config.ACAO = data['acao']
    config.PEDIDO_AUTOR = ""
    config.PEDIDO_REU = ""
    config.ACORDO = ""
    #config.DECISAO = ""
    config.NOME_JUIZ = data['magistrado']
    config.CONSILIACAO = ""




def genero_masculino(nome):
    partes = nome.split()
    print(partes)
    if br_gender_info.get_gender(partes[0]) == 'Male':
        return True
    else:
        return False

def gera_pagina(c):

    c.showPage()
    c.radialGradient(100 * mm, 150 * mm, 300 * mm, (white, gray), extend=False)
    c = gera_head(c)
    PAGE_WIDTH, PAGE_HEIGHT = letter

    pdf_canvas = c

    x, y = inch, inch
    width, height = PAGE_WIDTH - 2 * inch, PAGE_HEIGHT - 2 * inch


    c.setFillColorRGB(0.5, 0.5, 0.5)
    c.setFont('Helvetica-Bold', 12)
    c.drawString(190, 600, 'AUDIÊNCIA VIRTUAL DE CONCILIAÇÃO')





    c.setFillColorRGB(0.5, 0.5, 0.5)
    c.drawString(110, 400, 'DECISÕES DA JUÍZA:')
    c.setFont('Helvetica-Bold', 12)
    c.setFillColorRGB(0, 0, 0)
    c.drawString(110, 100, config.NOME_JUIZ)


    c.setFont('Helvetica', 9)
    c.setFillColorRGB(0, 0, 0)
    if genero_masculino(config.NOME_JUIZ):
        c.drawString(145, 85, 'Juíza de Direito')
    else:
        c.drawString(145, 85, 'Juíza de Direito')

    text_color = HexColor("#0153A5")
    style = ParagraphStyle(name="my_style", fontSize=11, leading=12, textColor=text_color)

    k = 0
    for item in config.DECISAO:
        ico_ok = ImageReader('imgs/verifica.png')
        c.drawImage(ico_ok, x-50 + inch / 2, y+215-k + inch, width=25, height=25, mask='auto')

        frame = Frame(x-20 + inch / 2, y-300-k + inch / 2, width-200 - inch, height - inch, showBoundary=0)
        paragraph = Paragraph(item, style=style)
        frame.addFromList([paragraph], pdf_canvas)
        k = k+55
    return pdf_canvas


def draw_checklist(canvas, x, y, width, items):
    canvas.setFont('Helvetica', 12)
    canvas.rect(x, y, width, len(items)*20 + 20, stroke=1, fill=0)
    canvas.line(x, y+20, x+width, y+20)
    canvas.setFont('Helvetica-Bold', 12)
    for i, item in enumerate(items):
        canvas.drawCheckmark(x+10, y+25+i*20, 10)
        canvas.drawString(x+25, y+20+i*20, item)

def reduz_icon(icon):
    icon = icon.resize((100, 100))
    return icon


def gera_head(c):
    tj = ImageReader('imgs/logo_tj.png')
    c.drawImage(tj, 20, 650, width=200, height=100, mask='auto')
    return c

def pdf_generator():

    lista_pedido_autor = config.PEDIDO_AUTOR.split(";")
    lista_pedido_reu = config.PEDIDO_REU.split(";")
    lista_acordo = config.ACORDO.split(";")





    BLUE = (0, 0, 1)  # ou BLUE = (0, 0, 255)
    # Criar um novo PDF com uma página em branco
    c = canvas.Canvas("output_.pdf", pagesize=letter)
    c.setFont("Helvetica-Bold", 12)

    width, height = c._pagesize


    c.radialGradient(100 * mm, 150 * mm, 300 * mm, (white, gray), extend=False)

    c.setFillColorRGB(1 / 255 * 1, 1 / 255 * 83, 1 / 255 * 165)

    if genero_masculino(config.AUTOR):
        c.drawString(80, 570, 'AUTOR: '+config.AUTOR)
    else:
        c.drawString(80, 570, 'AUTORA: '+config.AUTOR)

    if genero_masculino(config.REU):
        c.drawString(350, 570, 'REU: '+config.REU)
    else:
        c.drawString(350, 570, 'RÉ: ' + config.REU)
    c.drawString(200, 520, 'Processo n. ' + config.NUM_PROCESSO)
    c.drawString(190, 490, 'Ação:' + config.ACAO)

    c.setFillColorRGB(0.5, 0.5, 0.5)
    c.drawString(250, 310, 'RESUMO DO PROCESSO')

    c.setFont("Helvetica", 12)
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

    c.setFont("Helvetica-Bold", 12)
    c.setFillColorRGB(0.5, 0.5, 0.5)
    c.drawString(290, 150, 'ACORDO')

    c.setFont("Helvetica", 12)


    c.setPageSize((612, 792))
    c = gera_head(c)



    img = ImageReader('foto.png')
    # resumo = ImageReader('imgs/img_resumo.png')
    # 
    c.drawImage(img, 150, 350, width=320, height=120, mask='auto')
    # c.drawImage(resumo, 230, 600, width=145, height=14, mask='auto')

    c.setFont("Helvetica-Bold", 12)
    c.setFillColorRGB(1 / 255 * 1, 1 / 255 * 83, 1 / 255 * 165)
    c.drawString(230, 600, 'RESUMO DA SENTENÇA')


    c = gera_pagina(c)

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

    dados_tabela = importador.obter_dados_tabela('5234338.35.2018.8.09.0175')
    for linha in dados_tabela:
        if linha[2] == 'Decisão':
            config.DECISAO = sumarizador_decisao.processa_decisao(linha[4])

    carrega_dados()
    df = pd.read_csv('data.csv')
    flow_generate(df)
    metadaos = pd.read_csv('metadata.csv')
    pdf_generator()
    f = open('sentencas/sentenca_1.json')
    data = json.load(f)
    print(data['autor'])




