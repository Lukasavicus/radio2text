import json
import time

from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from openai import OpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers.string import StrOutputParser
from dotenv import load_dotenv, find_dotenv
import argparse
import os

"""
    Usage: python3 C3PO.py "2.silver/2024-12-11-11-00/transcription_chunks" "3.gold/2024-12-11-11-00/answers.json"
"""

_ = load_dotenv(find_dotenv())


def execute_llm(input_list, template):
    # Local LLM
    prompt = PromptTemplate.from_template(template=template)
    # Groq
    chat = ChatGroq(model="llama-3.1-70b-versatile")
    chain = prompt | chat | StrOutputParser()

    answers = chain.batch(input_list)
    return answers

def main(input_path, output_path):
    template = """
        Você é um especialista em processamento de linguagem natural, com a missão de identificar palavras-chave em transcrições de programas de rádio. Imagine que você está participando da promoção "Caçada ao Apê" da Rádio Metropolitana. O objetivo é encontrar palavras-chave específicas mencionadas durante a programação para concorrer a um apartamento em São Paulo. 

        Sua tarefa:
        - Analisar: Cada trecho de texto que lhe for fornecido é uma transcrição de um segmento do programa de rádio.
        - Identificar: Extraia apenas a palavra-chave mencionada no contexto da promoção "Caçada ao Apê". 
        - Priorizar: Caso haja múltiplas palavras que poderiam ser consideradas chaves, priorize aquelas que:
            - São repetidas com frequência.
            - São pronunciadas de forma enfática ou com destaque.
            - Estão diretamente relacionadas à promoção (ex: código, senha, local).
        - Ignorar: Se nenhuma palavra-chave clara for encontrada, retorne "NONE".

        Restrições:
        - Foco na promoção: Desconsidere qualquer outra informação que não esteja diretamente relacionada à promoção "Caçada ao Apê".
        - Uma palavra por vez: Retorne apenas uma palavra-chave por trecho de texto.
        - Evitar informações pessoais: Não revele informações pessoais como nomes, endereços ou números de telefone.

        Exemplo:
        - Trecho: "Metropolitana 1337 a maior promoção do rádio chegou casada Wap Metropolitana Metropolitana vamos lá tem mais uma 'Polônia' 'Polônia' mais palavra chave para você você já participou é uma promoção do rádio para ganhar um AP novinho mobiliado continue ouvindo a Metropolitana tem que juntar cinco palavras-chave acessa lá Metropolitana fm.com.br barra caçada para gerar o seu cupom quanto mais você gerar Claro mais chances você tem de ganhar as inscrições já vão encerrar Viu é amanhã não fique de fora da maior Caçada do Brasil até Metropolitana anota aí ó 'Polônia' a minha alma tá armada e apontada para a cara do Sucesso."
        - Saída: Polônia

        Lembre-se:
        - Contextualização: Utilize o contexto do trecho para identificar a palavra-chave mais relevante.
        - Precisão: Evite ambiguidades e retorne apenas a palavra-chave mais provável.
        - Eficiência: Processe os dados de forma rápida e eficiente.

        A seguir análise o seguinte trecho de texto e identifique a palavra-chave:
        {text}

        Responda apenas com a palavra-chave.
    """
    
    chunk_size = 15
    input_list = []
    file_list = []
    if os.path.isfile(input_path):
        with open(input_path, 'r') as file:
            input_list = file.read().splitlines()
            file_list.append(os.path.join(input_path, input_list))
    elif os.path.isdir(input_path):
        for filename in os.listdir(input_path):
            if filename.endswith(".txt"):
                with open(os.path.join(input_path, filename), 'r') as file:
                    input_list.extend(file.read().splitlines())
                    file_list.append(os.path.join(input_path, filename))
    
    chunks = [input_list[x:x+chunk_size] for x in range(0, len(input_list), chunk_size)]
    
    print(f"Processing {len(input_list)} lines in {len(chunks)} chunks.")
    # print(chunks)
    answers = []
    for chunk in chunks:
        answers_c = execute_llm(chunk, template)
        answers.append(answers_c)
        print(list(zip(chunk, answers_c)))
        time.sleep(80)

    answers = [item for sublist in answers for item in sublist]
    print(answers)
    result = dict(zip(file_list, answers))

    dir_path = '/'.join(output_path.split("/")[:-1])
    os.makedirs(dir_path, exist_ok=True)

    print(f"Writing to {dir_path} {output_path} - {result}")
    with open(output_path, "w+", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=4)

def make_cli():
    parser = argparse.ArgumentParser(description="Process text files to identify keywords.")
    parser.add_argument('input_path', type=str, help="Path to a text file or directory containing text files.")
    parser.add_argument('output_path', type=str, help="Path to a the output text file.")
    args = parser.parse_args()
    main(args.input_path, args.output_path)

if __name__ == "__main__":
    make_cli()
