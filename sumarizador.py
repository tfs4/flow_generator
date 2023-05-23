from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer


def obter_topicos_do_texto(texto):
    parser = PlaintextParser.from_string(texto, Tokenizer("portuguese"))
    summarizer = TextRankSummarizer()
    resumo = summarizer(parser.document, 3)  # Define o número de sentenças do resumo desejado

    topicos = [str(sentenca) for sentenca in resumo]
    return topicos


# Exemplo de uso
texto = """
Decido. No caso em exame, verifica-se que as partes entabularam acordo acerca da união estável e da partilha do patrimônio comum, sendo que os documentos apresentados são suficientes para satisfazer os requisitos legais.

Quanto aos bens, as partes acordaram acerca dos termos da partilha: veículo placa JGC 5565 (mov. 1 - arq. 7) e ágio do imóvel de matrícula n. 59.187 (mov. 7 - arq. 2/4). 

Ressalte-se que, apesar da não comprovação da propriedade do imóvel de matrícula n. 59.187 (arq. 2/4 – mov. 7), alienado fiduciariamente, houve acordo acerca dos direitos pessoais (posse) relativos ao patrimônio e a transação entabulada fará lei somente entre os envolvidos, razão pela qual não haverá determinação deste juízo para registro na matrícula. 

Pelo exposto, HOMOLOGO o acordo celebrado nos presentes autos (mov. 19), para que surta seus efeitos jurídicos e legais, e DECLARO dissolvida a união estável havida entre ROBSON GOMES DA CUNHA E ZAIRA DE OLIVEIRA BARROS, com termo final em abril de 2020. 

Consequentemente, decreto a extinção do processo, com resolução de mérito, nos termos do artigo 487, I e III, b, do Código de Processo Civil. 

Sem custas, nos termos do §3º do art. 90 do Código de Processo Civil.  

Homologada a dispensa do prazo recursal, expeçam-se os documentos e ofícios necessários e, em seguida, arquivem-se os autos com as cautelas de estilo. Publicada eletronicamente.
"""

topicos = obter_topicos_do_texto(texto)

for topico in topicos:
    print(topico)