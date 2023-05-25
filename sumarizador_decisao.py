from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer

from transformers import BartForConditionalGeneration, BartTokenizer
import re


def pre_processamento(texto):
    expressao_regular = r"\([^()]*\)"
    texto_sem_parenteses = re.sub(expressao_regular, '', texto)

    return texto_sem_parenteses


def obter_topicos_do_texto(texto):
    parser = PlaintextParser.from_string(texto, Tokenizer("portuguese"))
    summarizer = TextRankSummarizer()
    resumo = summarizer(parser.document, 5)
    topicos = [str(sentenca) for sentenca in resumo]
    return topicos


def dividir_texto_apos_decido(texto):
    indice_decido = texto.upper().find("DECIDO")

    if indice_decido != -1:
        parte_apos_decido = texto[indice_decido + 6:].strip()
        return parte_apos_decido
    return ""


def sumarize_transformer(texto):
    model = BartForConditionalGeneration.from_pretrained('facebook/bart-large-cnn')
    tokenizer = BartTokenizer.from_pretrained('facebook/bart-large-cnn')
    inputs = tokenizer.batch_encode_plus([texto], max_length=1024, return_tensors='pt', truncation=True)
    min_length = max_length = 70
    resumo_ids = model.generate(inputs['input_ids'], num_beams=4, min_length=min_length, max_length=max_length, early_stopping=True)
    resumo = tokenizer.decode(resumo_ids[0], skip_special_tokens=True)

    return resumo






def processa_decisao(texto):
    result = []
    retorno = dividir_texto_apos_decido(texto)
    retorno = obter_topicos_do_texto(retorno)
    for topico in retorno:
        print(topico)
        topico = pre_processamento(topico)
        topico = sumarize_transformer(topico)
        result.append(topico)

    return result