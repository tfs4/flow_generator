from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer


def obter_topicos_do_texto(texto):
    parser = PlaintextParser.from_string(texto, Tokenizer("portuguese"))
    summarizer = TextRankSummarizer()
    resumo = summarizer(parser.document, 3)
    topicos = [str(sentenca) for sentenca in resumo]
    return topicos


def dividir_texto_apos_decido(texto):
    indice_decido = texto.upper().find("DECIDO")

    if indice_decido != -1:
        parte_apos_decido = texto[indice_decido + 6:].strip()
        return parte_apos_decido
    return ""


def processa_decisao(texto):
    retorno = dividir_texto_apos_decido(texto)
    retorno = obter_topicos_do_texto(retorno)
    return retorno