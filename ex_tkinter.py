import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import scrolledtext as st
import json
from PIL import Image, ImageTk

arquivo_json = "candidatos.json"

with open(arquivo_json, "r") as file:
    candidatos_json = json.load(file)

# candidatos = []
votantes = set()
votacao_ativa = False

janela = tk.Tk()
janela.title("Urna Eletrônica")

# Obter largura e altura da tela
largura_tela = janela.winfo_screenwidth()
altura_tela = janela.winfo_screenheight()
largura, altura = 800, 500

# Calcular coordenadas x e y para centralizar
x = (largura_tela // 2) - (largura // 2)
y = (altura_tela // 2) - (altura // 2)

def mostra_menu():
    janela.geometry(f"{largura}x{altura}+{x}+{y}")
    janela.configure(padx=20, pady=20)
    label_menu = tk.Label(janela, text="Escolha uma opção:")
    label_menu.pack(pady=10)
    tk.Button(janela, text="Candidatos", command=lista_candidatos).pack(pady=5)
    tk.Button(janela, text="Cadastro de Candidato", command=cadastra_candidato).pack(pady=5)
    tk.Button(janela, text="Iniciar Votação", command=iniciar_votacao).pack(pady=5)
    tk.Button(janela, text="Encerrar Votação", command=encerrar_votacao).pack(pady=5)

def cadastra_candidato():
    janela_cadastro = tk.Toplevel(janela)
    janela_cadastro.title("Cadastro de Candidato")
    janela_cadastro.geometry(f"{largura}x{altura}+{x}+{y}")

    caminho_imagem = tk.StringVar(value="")
    foto = [None]

    tk.Label(janela_cadastro, text="Número do Candidato:").pack(pady=5)
    entrada_numero = tk.Entry(janela_cadastro)
    entrada_numero.pack(pady=5)

    tk.Label(janela_cadastro, text="Nome do Candidato:").pack(pady=5)
    entrada_nome = tk.Entry(janela_cadastro)
    entrada_nome.pack(pady=5)

    tk.Label(janela_cadastro, text="Partido do Candidato:").pack(pady=5)
    entrada_partido = tk.Entry(janela_cadastro)
    entrada_partido.pack(pady=5)

    lbl_caminho = tk.Label(janela_cadastro, text="Nenhuma foto selecionada")
    lbl_caminho.pack(pady=5)

    lbl_imagem = tk.Label(janela_cadastro)
    lbl_imagem.pack(pady=10)

    def selecionar_imagem():
            caminho = filedialog.askopenfilename(
                parent=janela_cadastro,
                title="Selecione uma foto",
                filetypes=(("Arquivos de imagem", "*.jpg *.jpeg *.png"), ("Todos os arquivos", "*.*"))
            )


            if caminho:  # Se usuário selecionou algo
                try:
                    caminho_imagem.set(caminho)
                    lbl_caminho.config(text=caminho)
                    
                    # Carrega e exibe a imagem
                    img = Image.open(caminho)
                    img.thumbnail((150, 150))
                    foto[0] = ImageTk.PhotoImage(img)  # Mantém referência
                    lbl_imagem.config(image=foto[0])
                    
                except Exception as e:
                    messagebox.showerror("Erro", f"Não foi possível carregar a imagem:\n{str(e)}")

    def salvar_candidato():
        # with open (arquivo_json, "r") as file:
        #     candidatos_json = json.load(file)
        
        numero = entrada_numero.get()
        nome = entrada_nome.get()
        partido = entrada_partido.get()


        # candidatos.append

        if not numero or not nome or not partido:
            messagebox.showwarning("Erro", "Preencha todos os campos.")
            return
        
        # candidatos.append({"numero": numero, "nome": nome, "partido": partido, "votos": 0})
        candidatos_json.append({"numero": numero, "nome": nome, "partido": partido, "votos": 0, "imagem": caminho_imagem.get()})
        messagebox.showinfo("Sucesso", "Candidato cadastrado com sucesso!")
        
        with open (arquivo_json, "w") as file:
            json.dump(candidatos_json, file, indent=4)
        

        janela_cadastro.destroy()

    tk.Button(janela_cadastro, text="selecionar imagem", command=selecionar_imagem).pack(pady=5)

    tk.Button(janela_cadastro, text="Salvar", command=salvar_candidato).pack(pady=5)

def lista_candidatos():
    with open(arquivo_json, "r") as file:
        candidatos_json = json.load(file)

    janela_candidatos = tk.Toplevel(janela)
    janela_candidatos.title("Candidatos")
    janela_candidatos.geometry(f"{largura}x{altura}+{x}+{y}")

    fotos = []
    indice_atual = [0]
    
    try:
        imagem = Image.open(candidatos_json[indice_atual[0]]["imagem"]).resize((150, 150))
        foto = ImageTk.PhotoImage(imagem)
        fotos.append(foto)

        imagem_label = tk.Label(janela_candidatos, image=foto)

    except (KeyError, FileNotFoundError):
        imagem_label = tk.Label(janela_candidatos, text=f"Foto do candidato não registrada")
        
    imagem_label.pack()

    info_label = tk.Label(janela_candidatos, text=f"{candidatos_json[indice_atual[0]]['nome']} ({candidatos_json[indice_atual[0]]['partido']}) {candidatos_json[indice_atual[0]]['numero']}")
    info_label.pack()
    
    def trocar_imagem():
        try:
            indice_atual[0] = (indice_atual[0] + 1) % len(candidatos_json)
            novo_caminho = candidatos_json[indice_atual[0]]["imagem"]
            imagem = Image.open(novo_caminho).resize((150, 150))

            nova_foto = ImageTk.PhotoImage(imagem)
            fotos.append(nova_foto)
            imagem_label.configure(image=nova_foto)
            
        except (KeyError, FileNotFoundError, AttributeError):
            imagem_label.configure(image="", text="Foto do candidato não registrada")
            
        info_label.configure(text=f"{candidatos_json[indice_atual[0]]['nome']} ({candidatos_json[indice_atual[0]]['partido']}) {candidatos_json[indice_atual[0]]['numero']}")
    
    def trocar_imagem_anterior():
        try:
            indice_atual[0] = (indice_atual[0] - 1) % len(candidatos_json)
            novo_caminho = candidatos_json[indice_atual[0]]["imagem"]
            imagem = Image.open(novo_caminho).resize((150, 150))

            nova_foto = ImageTk.PhotoImage(imagem)
            fotos.append(nova_foto)
            imagem_label.configure(image=nova_foto)

        except (KeyError, FileNotFoundError, AttributeError):
            imagem_label.configure(image="", text="Foto do candidato não registrada")
            
        info_label.configure(text=f"{candidatos_json[indice_atual[0]]['nome']} ({candidatos_json[indice_atual[0]]['partido']}) {candidatos_json[indice_atual[0]]['numero']}")

    def deletar_candidato():
        if 0 <= indice_atual < len(candidatos_json):
            candidato_deletado = candidatos_json.pop(indice_atual)
        
        with open(arquivo_json, "w") as file:
            json.dump(candidatos_json, file, indent=4)

    tk.Button(janela_candidatos, text="Proximo", command=trocar_imagem).place(x=700, y=100)
    tk.Button(janela_candidatos, text="Proximo", command=trocar_imagem_anterior).place(x=100, y=100)
    tk.Button(janela_candidatos, text="Deletar candidato", command=deletar_candidato).pack(pady=5)

def iniciar_votacao():
    global votacao_ativa
    votacao_ativa = True
    registrar_voto()

def registrar_voto():
    if votacao_ativa:
        janela_votacao = tk.Toplevel(janela)
        janela_votacao.title("Votação")
        janela_votacao.geometry(f"{largura}x{altura}+{x}+{y}")
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
            candidato = next((c for c in candidatos_json if c["numero"] == voto), None)
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
    janela_relatorio.geometry(f"{largura}x{altura}+{x}+{y}")
    total_votos = sum(c["votos"] for c in candidatos_json)
    if total_votos > 0:
        for candidato in candidatos_json:
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
