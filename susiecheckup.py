


import tkinter as tk
from tkinter import messagebox
import colorama
from colorama import Fore, Style
import spacy
import docx
import pdfplumber

# Inicializa o Colorama (para colorir o terminal no Windows)
colorama.init()

# Variável da senha correta
SENHA_CORRETA = "botdf123@"


# -----------------------------------------------------
# Função de Validação da Senha
# -----------------------------------------------------
def validar_senha():
    """
    Valida a senha inserida pelo usuário.
    """
    senha = entrada_senha.get()
    if senha == SENHA_CORRETA:
        # Fecha a janela após senha correta
        janela_senha.destroy()
        mensagem_sobre_susy()
        abrir_menu_terminal()
    else:
        # Mostra mensagem de erro se a senha estiver incorreta
        messagebox.showerror("Senha Incorreta", "Ops! Senha inválida. Tente novamente.")


# -----------------------------------------------------
# Exibe a mensagem "Quem é I.A Susy?"
# -----------------------------------------------------
def mensagem_sobre_susy():
    """
    Exibe a introdução sobre o programa após senha correta.
    """
    print(Fore.CYAN + """
*************************************************************
                        Quem é a I.A Susy?
*************************************************************
O **I.A Susy** foi desenvolvido com o objetivo de ajudar o Senhor,
facilitando tarefas do dia a dia. 

Ela aprende comandos personalizados, executa funções específicas
e guarda memórias para se tornar cada vez mais útil.

Sua missão é garantir uma interação prática, auxiliando e tornando
as atividades do Senhor mais simples e eficientes.
*************************************************************\n\n""" + Style.RESET_ALL)


# -----------------------------------------------------
# Janela de Login - Pede a Senha
# -----------------------------------------------------
def solicitar_senha():
    """
    Cria uma janela inicial para solicitar a senha ao usuário.
    """
    global janela_senha, entrada_senha

    # Configura a janela do Tkinter para a senha
    janela_senha = tk.Tk()
    janela_senha.title("Entrada Segura")
    janela_senha.geometry("400x200")
    janela_senha.resizable(False, False)

    # Instrução na janela
    lbl_instrucoes = tk.Label(janela_senha, text="Por favor, insira a senha para acessar a Susy:", font=("Arial", 12))
    lbl_instrucoes.pack(pady=10)

    # Caixa de entrada para a senha
    entrada_senha = tk.Entry(janela_senha, show="*", font=("Arial", 14), width=25)
    entrada_senha.pack(pady=10)

    # Botão de validação
    btn_validar = tk.Button(janela_senha, text="Entrar", font=("Arial", 12), command=validar_senha)
    entrada_senha.bind("<Return>", lambda event: validar_senha())  # Tecla Enter para validar a senha
    btn_validar.pack(pady=10)

    # Garantir que a janela está em destaque
    janela_senha.lift()
    janela_senha.focus_force()

    janela_senha.mainloop()


# -----------------------------------------------------
# Menu Principal no Terminal
# -----------------------------------------------------
def abrir_menu_terminal():
    """
    Exibe o menu principal no terminal e processa comandos do usuário.
    """
    while True:
        print(Fore.CYAN + "=" * 50)
        print(Fore.YELLOW + Style.BRIGHT + "Bem-vindo ao Menu Principal!")
        print(Fore.CYAN + "=" * 50 + Style.RESET_ALL)

        print(Fore.GREEN + "Escolha uma opção:")
        print(Fore.BLUE + "Comandos disponíveis:")
        print(Fore.YELLOW + "     - Digite 'sobre' para reler quem é a Susy.")
        print(Fore.MAGENTA + "     - Digite 'modo escola' para acessar o menu do Modo Escola.")
        print(Fore.GREEN + "     - Digite 'ativar modo escola' para começar a detecção de perguntas escolares.")
        print(Fore.RED + "     - Digite 'sair' para encerrar o programa.")
        print(Fore.CYAN + "=" * 50 + Style.RESET_ALL)

        resposta = input(Fore.MAGENTA + "Digite seu comando aqui: " + Fore.RESET)

        if resposta.strip().lower() == "sobre":
            mensagem_sobre_susy()
        elif resposta.strip().lower() == "modo escola":
            iniciar_modo_escola()
            print(Fore.GREEN + "\nO modo escola ainda será implementado nesta sessão!\n" + Style.RESET_ALL)
        elif resposta.strip().lower() == "sair":
            print(Fore.YELLOW + "\nPrograma encerrado. Até a próxima." + Style.RESET_ALL)
            break
        else:
            print(Fore.RED + "\nComando inválido! Por favor, tente novamente.\n" + Style.RESET_ALL)

def iniciar_modo_escola():
    """
    Ativa o modo escola para identificar perguntas relacionadas a conteúdos escolares.
    """
    while True:
        print(Fore.GREEN + "\nMODO ESCOLA - Escolha uma opção:" + Style.RESET_ALL)
        print(Fore.YELLOW + "1. Inserir texto diretamente" + Style.RESET_ALL)
        print(Fore.YELLOW + "2. Carregar perguntas de um arquivo .docx" + Style.RESET_ALL)
        print(Fore.YELLOW + "3. Carregar perguntas de um arquivo .pdf" + Style.RESET_ALL)
        print(Fore.RED + "4. Voltar ao menu principal" + Style.RESET_ALL)

        opcao = input(Fore.CYAN + "\nDigite a opção desejada (1/2/3/4): " + Style.RESET_ALL).strip()
        if opcao == "1":
            texto = input(Fore.MAGENTA + "\nDigite ou cole o texto escolar: " + Style.RESET_ALL).strip()
            exibir_perguntas_escolares(texto)
        elif opcao == "2":
            caminho = input(Fore.MAGENTA + "\nDigite o caminho do arquivo .docx: " + Style.RESET_ALL).strip()
            try:
                texto = carregar_texto_docx(caminho)
                exibir_perguntas_escolares(texto)
            except Exception as e:
                print(Fore.RED + f"Erro ao carregar o arquivo .docx: {e}" + Style.RESET_ALL)
        elif opcao == "3":
            caminho = input(Fore.MAGENTA + "\nDigite o caminho do arquivo .pdf: " + Style.RESET_ALL).strip()
            try:
                texto = carregar_texto_pdf(caminho)
                exibir_perguntas_escolares(texto)
            except Exception as e:
                print(Fore.RED + f"Erro ao carregar o arquivo .pdf: {e}" + Style.RESET_ALL)
        elif opcao == "4":
            print(Fore.YELLOW + "Retornando ao menu principal..." + Style.RESET_ALL)
            break
        else:
            print(Fore.RED + "Opção inválida. Tente novamente." + Style.RESET_ALL)

# -----------------------------------------------------
# Funções para Detecção de Perguntas em Texto
# -----------------------------------------------------
def detectar_perguntas_spacy(texto):
    """
    Detecta perguntas em um texto simples utilizando spaCy.
    """
    nlp = spacy.load("pt_core_news_sm")
    doc = nlp(texto)
    perguntas = [sent.text for sent in doc.sents if sent.text.strip().endswith("?")]
    return perguntas

def carregar_texto_docx(caminho):
    """
    Carrega o texto de um arquivo .docx.
    """
    import os
    if not os.path.exists(caminho):
        raise FileNotFoundError("O arquivo .docx não foi encontrado.")
    doc = docx.Document(caminho)
    texto = "\n".join(paragraph.text for paragraph in doc.paragraphs if paragraph.text.strip())
    return texto

def carregar_texto_pdf(caminho):
    """
    Carrega o texto de um arquivo .pdf.
    """
    import os
    if not os.path.exists(caminho):
        raise FileNotFoundError("O arquivo .pdf não foi encontrado.")
    texto = ""
    with pdfplumber.open(caminho) as pdf:
        for page in pdf.pages:
            texto += page.extract_text()
    return texto

def exibir_perguntas(texto):
    """
    Exibe as perguntas encontradas em um determinado texto e salva-as em um arquivo.
    """
    salvar_perguntas_em_arquivo(texto)

    perguntas = detectar_perguntas_spacy(texto)
    salvar_perguntas_em_arquivo(perguntas)
    if perguntas:
        print(Fore.GREEN + "Perguntas encontradas no texto:" + Style.RESET_ALL)
        for i, pergunta in enumerate(perguntas, 1):
            print(Fore.YELLOW + f"{i}. {pergunta}" + Style.RESET_ALL)
    else:
            print(Fore.RED + "Nenhuma pergunta detectada no texto." + Style.RESET_ALL)
def exibir_perguntas_escolares(texto):
    """
    Exibe apenas perguntas relacionadas a conteúdos escolares no texto.
    """
    perguntas = detectar_perguntas_spacy(texto)
    salvar_perguntas_em_arquivo(perguntas)
    if perguntas:
        print(Fore.GREEN + "Perguntas escolares identificadas no texto:" + Style.RESET_ALL)
        for i, pergunta in enumerate(perguntas, 1):
            print(Fore.YELLOW + f"{i}. {pergunta}" + Style.RESET_ALL)
    else:
        print(Fore.RED + "Nenhuma pergunta escolar detectada no texto." + Style.RESET_ALL)
def salvar_perguntas_em_arquivo(perguntas):
    """
    Salva as perguntas em um arquivo na pasta especificada.
    """
    caminho = r"C:\Users\vitor\Desktop\Memórias da Suzy\perguntas_salvas.txt"
    with open(caminho, "w", encoding="utf-8") as arquivo:
        for pergunta in perguntas:
            arquivo.write(pergunta + "\n")
add text before this line
# -----------------------------------------------------
# Inicialização do Programa
# -----------------------------------------------------
if __name__ == "__main__":
    try:
        # Inicia a janela de login
        solicitar_senha()
        print(Fore.CYAN + "Bem-vindo! Vamos verificar perguntas em textos ou arquivos.\n" + Style.RESET_ALL)
        print(Fore.GREEN + "Opções disponíveis:" + Style.RESET_ALL)
        print(Fore.YELLOW + "1. Detectar perguntas em um texto simples" + Style.RESET_ALL)
        print(Fore.YELLOW + "2. Detectar perguntas em um arquivo .docx" + Style.RESET_ALL)
        print(Fore.YELLOW + "3. Detectar perguntas em um arquivo .pdf" + Style.RESET_ALL)
        print(Fore.RED + "Digite 'sair' para encerrar o programa." + Style.RESET_ALL)

        while True:
            opcao = input(Fore.CYAN + "\nDigite a opção desejada (1/2/3/sair): " + Style.RESET_ALL).strip().lower()
            if opcao == "1":
                texto = input(Fore.MAGENTA + "\nDigite ou cole o texto: " + Style.RESET_ALL).strip()
                exibir_perguntas(texto)
            elif opcao == "2":
                caminho = input(Fore.MAGENTA + "\nDigite o caminho do arquivo .docx: " + Style.RESET_ALL).strip()
                try:
                    texto = carregar_texto_docx(caminho)
                    exibir_perguntas(texto)
                except Exception as e:
                    print(Fore.RED + f"Erro ao carregar o arquivo .docx: {e}" + Style.RESET_ALL)
            elif opcao == "3":
                caminho = input(Fore.MAGENTA + "\nDigite o caminho do arquivo .pdf: " + Style.RESET_ALL).strip()
                try:
                    texto = carregar_texto_pdf(caminho)
                    exibir_perguntas(texto)
                except Exception as e:
                    print(Fore.RED + f"Erro ao carregar o arquivo .pdf: {e}" + Style.RESET_ALL)
            elif opcao == "sair":
                print(Fore.YELLOW + "Programa encerrado. Até logo!" + Style.RESET_ALL)
                break
            else:
                print(Fore.RED + "Opção inválida. Tente novamente." + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"Um erro inesperado ocorreu: {e}" + Style.RESET_ALL)




