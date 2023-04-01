from PIL import Image, ImageDraw, ImageFont
import os
import pandas as pd

def reduz_icon(icon):
    icon = icon.resize((100, 100))
    return icon


def flow_generate(df):
    img = Image.new('RGBA', (800, 300), color=(255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
   # draw.line((700, 125, 100, 125), fill='black', width=5)

    arrow_size = 20  # tamanho da seta em pixels
    arrow_base = (40 - arrow_size, 250)  # ponto da base da seta
    arrow_tip = (760 + arrow_size, 250)  # ponto da ponta da seta
    draw.line((arrow_base, arrow_tip), fill='black', width=5)

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
        img.paste(i, (x, y))
        font = ImageFont.truetype("fonts/arial.ttf", 20)
        draw.text((text_x, text_y), text, fill='black', font=font)



        k = k + d

    img.save('foto.png')

if __name__ == '__main__':
    df = pd.read_csv('data.csv')
    flow_generate(df)
