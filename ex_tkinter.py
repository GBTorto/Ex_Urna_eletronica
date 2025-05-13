import tkinter as tk
from tkinter import messagebox
from tkinter import scrolledtext as st
import json
from PIL import Image, ImageTk

arquivo_json = "candidatos.json"

candidatos = []
votantes = set()
votacao_ativa = False

janela = tk.Tk()
janela.title("Urna Eletrônica")

# Obter largura e altura da tela
largura_tela = janela.winfo_screenwidth()
altura_tela = janela.winfo_screenheight()
largura, altura = 1000, 500

# Calcular coordenadas x e y para centralizar
x = (largura_tela // 2) - (largura // 2)
y = (altura_tela // 2) - (altura // 2)

def mostra_menu():
    janela.geometry(f"{largura_tela}x{altura_tela}")
    janela.configure(padx=20, pady=20)
    label_menu = tk.Label(janela, text="Escolha uma opção:")
    label_menu.pack(pady=10)
    tk.Button(janela, text="Cadastro de Candidato", command=cadastra_candidato).pack(pady=5)
    tk.Button(janela, text="Candidatos", command=lista_candidatos).pack(pady=5)
    tk.Button(janela, text="Iniciar Votação", command=iniciar_votacao).pack(pady=5)
    tk.Button(janela, text="Encerrar Votação", command=encerrar_votacao).pack(pady=5)

def cadastra_candidato():
    janela_cadastro = tk.Toplevel(janela)
    janela_cadastro.title("Cadastro de Candidato")
    janela_cadastro.geometry(f"{largura_tela}x{altura_tela}")
    tk.Label(janela_cadastro, text="Número do Candidato:").pack(pady=5)
    entrada_numero = tk.Entry(janela_cadastro)
    entrada_numero.pack(pady=5)
    tk.Label(janela_cadastro, text="Nome do Candidato:").pack(pady=5)
    entrada_nome = tk.Entry(janela_cadastro)
    entrada_nome.pack(pady=5)
    tk.Label(janela_cadastro, text="Partido do Candidato:").pack(pady=5)
    entrada_partido = tk.Entry(janela_cadastro)
    entrada_partido.pack(pady=5)

    def salvar_candidato():
        with open (arquivo_json, "r") as file:
            candidatos = json.load(file)
        
        numero = entrada_numero.get()
        nome = entrada_nome.get()
        partido = entrada_partido.get()


        candidatos.append

        if not numero or not nome or not partido:
            messagebox.showwarning("Erro", "Preencha todos os campos.")
            return
        candidatos.append({"numero": numero, "nome": nome, "partido": partido, "votos": 0})
        messagebox.showinfo("Sucesso", "Candidato cadastrado com sucesso!")
        janela_cadastro.destroy()

    tk.Button(janela_cadastro, text="Salvar", command=salvar_candidato).pack(pady=5)

def lista_candidatos():
    janela_candidatos = tk.Toplevel(janela)
    janela_candidatos.title("Candidatos")
    janela_candidatos.geometry(f"{largura_tela}x{altura_tela}")

    fotos = []
    indice_atual = [0]

    with open(arquivo_json, "r") as file:
        candidatos = json.load(file)
    
    try:
        imagem = Image.open(candidatos[indice_atual[0]]["imagem"]).resize((150, 150))
        foto = ImageTk.PhotoImage(imagem)
        fotos.append(foto)

        imagem_label = tk.Label(janela_candidatos, image=foto)

    except (KeyError, FileNotFoundError):
        imagem_label = tk.Label(janela_candidatos, text=f"Foto do candidato não registrada")
        
    imagem_label.pack()

    info_label = tk.Label(janela_candidatos, text=f"{candidatos[indice_atual[0]]['nome']} ({candidatos[indice_atual[0]]['partido']}) {candidatos[indice_atual[0]]['numero']}")
    info_label.pack()
    
    def trocar_imagem():
        try:
            indice_atual[0] = (indice_atual[0] + 1) % len(candidatos)
            novo_caminho = candidatos[indice_atual[0]]["imagem"]
            imagem = Image.open(novo_caminho).resize((150, 150))
            nova_foto = ImageTk.PhotoImage(imagem)
            fotos.append(nova_foto)
            imagem_label.configure(image=nova_foto)
        except (KeyError, FileNotFoundError):
            imagem_label.configure(image="", text="Foto do candidato não registrada")
            
        info_label.configure(text=f"{candidatos[indice_atual[0]]['nome']} ({candidatos[indice_atual[0]]['partido']}) {candidatos[indice_atual[0]]['numero']}")

    tk.Button(janela_candidatos, text="Proximo", command=trocar_imagem).pack(pady=5)

def iniciar_votacao():
    global votacao_ativa
    votacao_ativa = True
    registrar_voto()

def registrar_voto():
    if votacao_ativa:
        janela_votacao = tk.Toplevel(janela)
        janela_votacao.title("Votação")
        janela_votacao.geometry(f"{largura_tela}x{altura_tela}")
        tk.Label(janela_votacao, text="Digite sua matrícula:").pack(pady=5)
        entrada_matricula = tk.Entry(janela_votacao)
        entrada_matricula.pack(pady=5)
        tk.Label(janela_votacao, text="Digite o número do candidato:").pack(pady=5)
        entrada_voto = tk.Entry(janela_votacao)
        entrada_voto.pack(pady=5)

        def confirmar_voto():
            matricula = entrada_matricula.get()
            voto = entrada_voto.get()
            if not matricula:
                messagebox.showwarning("Erro", "Matrícula não pode ser vazia.")
                return
            if matricula in votantes:
                messagebox.showwarning("Erro", "Esta matrícula já votou.")
                return
            candidato = next((c for c in candidatos if c["numero"] == voto), None)
            if candidato:
                confirmar = messagebox.askyesno("Confirmação", f"Confirmar voto para {candidato['nome']} ({candidato['partido']})?")
                if confirmar:
                    candidato["votos"] += 1
                    votantes.add(matricula)
                    messagebox.showinfo("Sucesso", "Voto registrado com sucesso!")
                    janela_votacao.destroy()
                    registrar_voto()
            else:
                confirmar = messagebox.askyesno("Confirmação", "Candidato inexistente. Confirmar voto nulo?")
                if confirmar:
                    votantes.add(matricula)
                    messagebox.showinfo("Sucesso", "Voto nulo registrado!")
                    janela_votacao.destroy()
                    registrar_voto()

        tk.Button(janela_votacao, text="Votar", command=confirmar_voto).pack(pady=5)

def imprime_relatorio():
    janela_relatorio = tk.Toplevel(janela)
    janela_relatorio.title("Resultados")
    janela_relatorio.geometry(f"{largura_tela}x{altura_tela}")
    total_votos = sum(c["votos"] for c in candidatos)
    if total_votos > 0:
        for candidato in candidatos:
            tk.Label(janela_relatorio, text=f"{candidato['nome']} ({candidato['partido']}): {candidato['votos']} votos").pack(pady=5)
    else:
        tk.Label(janela_relatorio, text="Não houve votos válidos.").pack(pady=5)
    tk.Button(janela_relatorio, text="Fechar", command=janela_relatorio.destroy).pack(pady=5)

def encerrar_votacao():
    global votacao_ativa
    votacao_ativa = False
    imprime_relatorio()

# Chamada principal
mostra_menu()
janela.mainloop()
