import tkinter as tk
from tkinter import messagebox, filedialog
import json
from PIL import Image, ImageTk

# Configurações iniciais
arquivo_json = "candidatos.json"

try:
    with open(arquivo_json, "r") as file:
        candidatos_json = json.load(file)
except FileNotFoundError:
    candidatos_json = []
    with open(arquivo_json, "w") as file:
        json.dump(candidatos_json, file)

votantes = set()  # Agora armazena apenas CPFs (strings)
votacao_ativa = False

# Janela principal
janela = tk.Tk()
janela.title("Urna Eletrônica")

# Centralizar janela
largura, altura = 800, 500
largura_tela = janela.winfo_screenwidth()
altura_tela = janela.winfo_screenheight()
x = (largura_tela // 2) - (largura // 2)
y = (altura_tela // 2) - (altura // 2)

cor_normal = "SystemButtonFace"
cor_hover = "#d9d9d9"

def hover(widget, cor_normal, cor_hover):
    # Configuração inicial
    widget.config(bg=cor_normal, cursor="")  # Cursor padrão inicialmente
    
    # Evento quando o mouse entra no widget
    widget.bind("<Enter>", lambda e: (
        e.widget.config(bg=cor_hover, cursor="hand2")
    ))
    
    # Evento quando o mouse sai do widget
    widget.bind("<Leave>", lambda e: (
        e.widget.config(bg=cor_normal, cursor="")
    ))

def mostra_menu():
    janela.geometry(f"{largura}x{altura}+{x}+{y}")
    janela.configure(padx=20, pady=20)
    
    # Limpa widgets anteriores
    for widget in janela.winfo_children():
        widget.destroy()

    lbl_titulo = tk.Label(janela, text="Escolha uma opção:")
    btn_candidatos = tk.Button(janela, text="Candidatos", command=lista_candidatos)
    btn_cadastro = tk.Button(janela, text="Cadastro de Candidato", command=cadastra_candidato)
    btn_votacao = tk.Button(janela, text="Iniciar Votação", command=digitar_cpf)
    btn_encerrar = tk.Button(janela, text="Encerrar Votação", command=encerrar_votacao)

    # Posiciona os widgets
    lbl_titulo.pack(pady=10)
    btn_candidatos.pack(pady=5, fill=tk.X, padx=50)
    btn_cadastro.pack(pady=5, fill=tk.X, padx=50)
    btn_votacao.pack(pady=5, fill=tk.X, padx=50)
    btn_encerrar.pack(pady=5, fill=tk.X, padx=50)

    # Aplica hover apenas nos botões (não no Label)
    hover(btn_candidatos, cor_normal, cor_hover)
    hover(btn_cadastro, cor_normal, cor_hover)
    hover(btn_votacao, cor_normal, cor_hover)
    hover(btn_encerrar, cor_normal, cor_hover)

def administrador():
    janela_senha_administrador = tk.Toplevel(janela)
    janela_senha_administrador.title("Digite a senha")
    janela_senha_administrador.geometry(f"{400}x{250}+{x + 200}+{y + 125}")

    tk.Label(janela_senha_administrador, text="Digite a senha:")
    entrada_senha = tk.Entry(janela_senha_administrador)
    entrada_senha.pack(pady=5)
    
def cadastra_candidato():
    janela_cadastro = tk.Toplevel(janela)
    janela_cadastro.title("Cadastro de Candidato")
    janela_cadastro.geometry(f"{largura}x{altura}+{x}+{y}")

    caminho_imagem = tk.StringVar(value="")
    foto = [None]

    # Widgets de cadastro
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
            title="Selecione uma foto",
            filetypes=(("Arquivos de imagem", "*.jpg *.jpeg *.png"), ("Todos os arquivos", "*.*"))
        )
        if caminho:
            try:
                caminho_imagem.set(caminho)
                lbl_caminho.config(text=caminho)
                img = Image.open(caminho)
                img.thumbnail((150, 150))
                foto[0] = ImageTk.PhotoImage(img)
                lbl_imagem.config(image=foto[0])
            except Exception as e:
                messagebox.showerror("Erro", f"Não foi possível carregar a imagem:\n{str(e)}")

    def salvar_candidato():
        numero = entrada_numero.get()
        nome = entrada_nome.get()
        partido = entrada_partido.get()

        if not numero or not nome or not partido:
            messagebox.showwarning("Erro", "Preencha todos os campos.")
            return
        
        # Verifica se número já existe
        if any(c["numero"] == numero for c in candidatos_json):
            messagebox.showerror("Erro", "Já existe um candidato com este número!")
            return

        candidatos_json.append({
            "numero": numero,
            "nome": nome,
            "partido": partido,
            "votos": 0,
            "imagem": caminho_imagem.get()
        })
        
        with open(arquivo_json, "w") as file:
            json.dump(candidatos_json, file, indent=4)
        
        messagebox.showinfo("Sucesso", "Candidato cadastrado com sucesso!")
        janela_cadastro.destroy()

    tk.Button(janela_cadastro, text="Selecionar Imagem", command=selecionar_imagem).pack(pady=5)
    tk.Button(janela_cadastro, text="Salvar", command=salvar_candidato).pack(pady=5)

def lista_candidatos():
    janela_candidatos = tk.Toplevel(janela)
    janela_candidatos.title("Candidatos")
    janela_candidatos.geometry(f"{largura}x{altura}+{x}+{y}")

    if not candidatos_json:
        tk.Label(janela_candidatos, text="Nenhum candidato cadastrado").pack(pady=50)
        return

    fotos = []
    indice_atual = tk.IntVar(value=0)

    def atualizar_candidato():
        idx = indice_atual.get()
        candidato = candidatos_json[idx]
        
        # Limpa frame da imagem
        for widget in frame_imagem.winfo_children():
            widget.destroy()
        
        # Tenta carregar imagem
        try:
            imagem = Image.open(candidato["imagem"]).resize((150, 150))
            foto = ImageTk.PhotoImage(imagem)
            fotos.append(foto)  # Mantém referência
            tk.Label(frame_imagem, image=foto).pack()
        except (KeyError, FileNotFoundError, AttributeError):
            tk.Label(frame_imagem, text="Foto não disponível").pack()
        
        info_label.config(text=f"{candidato['nome']} ({candidato['partido']}) - Número: {candidato['numero']}\nVotos: {candidato['votos']}")

    frame_imagem = tk.Frame(janela_candidatos)
    frame_imagem.pack(pady=10)

    info_label = tk.Label(janela_candidatos, font=('Arial', 12))
    info_label.pack(pady=10)

    def proximo():
        indice_atual.set((indice_atual.get() + 1) % len(candidatos_json))
        atualizar_candidato()

    def anterior():
        indice_atual.set((indice_atual.get() - 1) % len(candidatos_json))
        atualizar_candidato()

    def deletar_candidato():
        idx = indice_atual.get()
        resposta = messagebox.askyesno(
            "Confirmar Exclusão",
            f"Tem certeza que deseja excluir o candidato {candidatos_json[idx]['nome']}?",
            parent=janela_candidatos
        )
        if resposta:
            candidatos_json.pop(idx)
            with open(arquivo_json, "w") as file:
                json.dump(candidatos_json, file, indent=4)
            
            if not candidatos_json:
                janela_candidatos.destroy()
                messagebox.showinfo("Info", "Nenhum candidato restante")
            else:
                indice_atual.set(min(idx, len(candidatos_json)-1))
                atualizar_candidato()

    tk.Button(janela_candidatos, text="< Anterior", command=anterior).pack(side=tk.LEFT, padx=20)
    tk.Button(janela_candidatos, text="Próximo >", command=proximo).pack(side=tk.RIGHT, padx=20)
    tk.Button(janela_candidatos, text="Deletar", command=deletar_candidato, fg="red").pack(pady=10)

    atualizar_candidato()

def digitar_cpf():
    janela_informacoes = tk.Toplevel(janela)
    janela_informacoes.title("Dados do Eleitor")
    janela_informacoes.geometry(f"{400}x{250}+{x + 200}+{y + 125}")
    janela_informacoes.grab_set()

    tk.Label(janela_informacoes, text="Digite seu nome completo:", font=("Arial", 10, "bold")).pack(pady=(19, 0))
    entrada_nome = tk.Entry(janela_informacoes, width=30)
    entrada_nome.pack(pady=5)

    tk.Label(janela_informacoes, text="RG (apenas números):", font=("Arial", 10, "bold")).pack(pady=(5, 0))
    entrada_rg = tk.Entry(janela_informacoes, width=30)
    entrada_rg.pack(pady=5)

    tk.Label(janela_informacoes, text="CPF (apenas números):", font=("Arial", 10, "bold")).pack(pady=(5, 0))
    entrada_cpf = tk.Entry(janela_informacoes, width=30)
    entrada_cpf.pack(pady=5)
    
    def verificar_informacoes():
        nome = entrada_nome.get().strip()
        cpf = entrada_cpf.get().strip()
        rg = entrada_rg.get().strip()
        
        if not nome or not cpf or not rg:
            messagebox.showwarning("Atenção", "Preencha todos os campos", parent=janela_informacoes)
            return
        
        if not cpf.isdigit() or len(cpf) != 11:
            messagebox.showwarning("CPF Inválido", "CPF deve conter 11 números", parent=janela_informacoes)
            return
            
        if cpf in votantes:
            messagebox.showerror("Erro", "Este CPF já votou!", parent=janela_informacoes)
            return
            
        votantes.add(cpf)  # Registra o CPF para evitar votos duplicados
        janela_informacoes.destroy()
        iniciar_votacao(nome, cpf)

    tk.Button(janela_informacoes, text="Continuar", command=verificar_informacoes).pack(pady=10)

def iniciar_votacao(nome, cpf):
    global votacao_ativa
    votacao_ativa = True
    
    janela_votacao = tk.Toplevel(janela)
    janela_votacao.title("Votação")
    janela_votacao.geometry(f"{largura}x{altura}+{x}+{y}")
    janela_votacao.grab_set()

    tk.Label(janela_votacao, 
             text=f"Eleitor: {nome}\nCPF: {cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}",
             font=('Arial', 12)).pack(pady=10)

    tk.Label(janela_votacao, text="Digite o número do candidato:", font=('Arial', 14)).pack(pady=10)
    entrada_voto = tk.Entry(janela_votacao, font=('Arial', 16), justify='center')
    entrada_voto.pack(pady=10)
    entrada_voto.focus_set()

    def confirmar_voto():
        voto = entrada_voto.get().strip()
        
        if not voto:
            messagebox.showwarning("Voto em branco", "Digite um número ou confirme voto nulo", parent=janela_votacao)
            return
            
        candidato = next((c for c in candidatos_json if c["numero"] == voto), None)
        
        if candidato:
            resposta = messagebox.askyesno(
                "Confirmar Voto",
                f"Confirmar voto para:\n\n{candidato['nome']}\n{candidato['partido']}\nNúmero: {candidato['numero']}",
                parent=janela_votacao
            )
            if resposta:
                candidato["votos"] += 1
                messagebox.showinfo("Sucesso", "Voto registrado com sucesso!", parent=janela_votacao)
                janela_votacao.destroy()
        else:
            resposta = messagebox.askyesno(
                "Voto Nulo",
                "Candidato não encontrado. Deseja confirmar voto nulo?",
                parent=janela_votacao
            )
            if resposta:
                messagebox.showinfo("Voto Nulo", "Voto nulo registrado", parent=janela_votacao)
                janela_votacao.destroy()

    tk.Button(janela_votacao, text="Confirmar Voto", command=confirmar_voto, 
              bg="green", fg="white", font=('Arial', 12)).pack(pady=20)

def imprime_relatorio():
    janela_relatorio = tk.Toplevel(janela)
    janela_relatorio.title("Resultados da Votação")
    janela_relatorio.geometry(f"{largura}x{altura}+{x}+{y}")

    total_votos = sum(c["votos"] for c in candidatos_json)
    tk.Label(janela_relatorio, text=f"RELATÓRIO FINAL\nTotal de votos: {total_votos}", 
             font=('Arial', 14, 'bold')).pack(pady=10)

    if total_votos > 0:
        # Ordena candidatos por votos (decrescente)
        candidatos_ordenados = sorted(candidatos_json, key=lambda x: x["votos"], reverse=True)
        
        frame_resultados = tk.Frame(janela_relatorio)
        frame_resultados.pack(pady=10, fill=tk.BOTH, expand=True)
        
        for i, candidato in enumerate(candidatos_ordenados, 1):
            percentual = (candidato["votos"] / total_votos) * 100 if total_votos > 0 else 0
            tk.Label(frame_resultados, 
                     text=f"{i}º - {candidato['nome']} ({candidato['partido']}): {candidato['votos']} votos ({percentual:.1f}%)",
                     font=('Arial', 12)).pack(anchor='w', padx=20)
    else:
        tk.Label(janela_relatorio, text="Nenhum voto foi registrado.", font=('Arial', 12)).pack(pady=20)

    tk.Button(janela_relatorio, text="Fechar", command=janela_relatorio.destroy).pack(pady=10)

def encerrar_votacao():
    global votacao_ativa
    votacao_ativa = False
    imprime_relatorio()
    # Salva os votos no arquivo JSON
    with open(arquivo_json, "w") as file:
        json.dump(candidatos_json, file, indent=4)

# Inicia o sistema
mostra_menu()
janela.mainloop()