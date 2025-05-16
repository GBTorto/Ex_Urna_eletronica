import tkinter as tk
from tkinter import ttk
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

    janela.bind("<Control-Alt-m>", administrador)
    
    # Limpa widgets anteriores
    for widget in janela.winfo_children():
        widget.destroy()

    lbl_titulo = tk.Label(janela, text="Escolha uma opção:")
    btn_votacao = tk.Button(janela, text="Iniciar Votação", command=digitar_cpf)
    btn_encerrar = tk.Button(janela, text="Encerrar Votação", command=encerrar_votacao)

    # Posiciona os widgets
    lbl_titulo.pack(pady=10)
    btn_votacao.pack(pady=5, fill=tk.X, padx=50)
    btn_encerrar.pack(pady=5, fill=tk.X, padx=50)

    # Aplica hover apenas nos botões (não no Label)
    hover(btn_votacao, cor_normal, cor_hover)
    hover(btn_encerrar, cor_normal, cor_hover)

def administrador(event=None):
    janela_senha_adm = tk.Toplevel(janela)
    janela_senha_adm.title("Digite a senha")
    janela_senha_adm.geometry(f"{400}x{250}+{x + 200}+{y + 125}")

    tk.Label(janela_senha_adm, text="Digite a senha:").pack(pady=5)
    entrada_senha = tk.Entry(janela_senha_adm)
    entrada_senha.pack(pady=5)
    
    def verificacao():
        senha = entrada_senha.get()
        if senha == "1234":
            messagebox.showwarning("Olá!", "Bem vindo de volta administrador!")
            menu_administrador(janela_senha_adm)
        else:
            messagebox.showerror("Alerta!", "Vaza daqui vagabundo!")

    btn_acessar = tk.Button(janela_senha_adm, text="Entrar", command=verificacao)
    btn_acessar.pack(pady=5)

    hover(btn_acessar, cor_normal, cor_hover)

def menu_administrador(janela_senha_adm):
    global janela_adm
    janela_senha_adm.destroy()
    janela_adm = tk.Toplevel(janela)
    janela_adm.geometry(f"{largura}x{altura}+{x}+{y}")
    janela_adm.configure(padx=20, pady=20)

    lbl_titulo_adm = tk.Label(janela_adm, text="O que faremos hoje?")
    btn_candidatos = tk.Button(janela_adm, text="Lista de andidatos", command=lista_candidatos)
    btn_cadastro = tk.Button(janela_adm, text="Cadastro de Candidato", command=cadastra_candidato)

    lbl_titulo_adm.pack(pady=10)
    btn_candidatos.pack(pady=5, fill=tk.X, padx=50)
    btn_cadastro.pack(pady=5, fill=tk.X, padx=50)

    hover(btn_candidatos, cor_normal, cor_hover)
    hover(btn_cadastro, cor_normal, cor_hover)

def cadastra_candidato():
    janela_cadastro = tk.Toplevel(janela_adm)
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
            filetypes=(("Arquivos de imagem", "*.jpg *.jpeg *.png"), ("Todos os arquivos", "*.*")), parent=janela_cadastro
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

def scroll_imagens(container):
    imagens = []  # Lista para armazenar referências das imagens

    for candidato in candidatos_json:
        try:
            # 1. Carrega a imagem com tratamento de erro
            imagem = Image.open(candidato["imagem"]).resize((150, 150))
            imagem_tk = ImageTk.PhotoImage(imagem)
            imagens.append(imagem_tk)  # Mantém a referência

            # 2. Cria um frame para cada candidato (cartão)
            frame_candidato = tk.Frame(container)
            frame_candidato.pack(pady=10)

            # 3. Exibe a imagem (COM REFERÊNCIA ADICIONAL)
            lbl_imagem = tk.Label(frame_candidato, image=imagem_tk)
            lbl_imagem.image = imagem_tk  # Referência extra (CRÍTICO!)
            lbl_imagem.pack(padx=(0, 0))

            # 4. Exibe informações do candidato
            tk.Label(
                frame_candidato,
                text=f"{candidato['numero']} - {candidato['nome']}\n{candidato['partido']}",
                font=('Arial', 10)
            ).pack(padx=(0, 0))

        except Exception as e:
            print(f"Erro ao carregar imagem: {e}")
            # Placeholder se a imagem falhar
            tk.Label(
                container,
                text=f"{candidato['numero']} - {candidato['nome']}\n(Imagem não disponível)",
                font=('Arial', 10)
            ).pack(pady=10)

    return imagens  # Retorna a lista de referências

def iniciar_votacao(nome, cpf):
    global votacao_ativa
    votacao_ativa = True
    
    janela_votacao = tk.Toplevel(janela)
    janela_votacao.title("Votação")
    janela_votacao.geometry(f"{largura}x{altura}+{x}+{y}")
    janela_votacao.grab_set()

    # --- Área de Scroll ---
    # Frame principal para organizar os widgets
    main_frame = tk.Frame(janela_votacao)
    main_frame.pack(fill=tk.BOTH, expand=True)

    # 1. Canvas e Scrollbar
    canvas = tk.Canvas(main_frame, width=200)

    # Habilita o scroll com o mouse (adicione estas linhas)
    canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
    canvas.bind_all("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))  # Para Linux (scroll up)
    canvas.bind_all("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))   # Para Linux (scroll down)

    scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)

    # 2. Frame INTERNO para os candidatos (dentro do canvas)
    inner_frame = tk.Frame(canvas)
    inner_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    inner_frame.configure(padx=0)

    # 3. Vincula o frame ao canvas
    canvas.create_window((0, 0), window=inner_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    # 4. Layout do scroll
    canvas.pack(side=tk.LEFT, fill=tk.Y, expand=False, padx=(50, 0))
    scrollbar.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 0))

    # --- Carrega as imagens (com referência retornada) ---
    imagens = scroll_imagens(inner_frame)  # As imagens persistem aqui!

    # --- Área de votação ---
    tk.Label(
        main_frame,
        text=f"Eleitor: {nome}\nCPF: {cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}",
        font=('Arial', 12)
    ).pack(pady=10, padx=(0, 0))

    tk.Label(
        main_frame,
        text="Digite o número do candidato:",
        font=('Arial', 14)
    ).pack(pady=10, padx=(0, 0))

    entrada_voto = tk.Entry(main_frame, font=('Arial', 16), justify='center')
    entrada_voto.pack(pady=10, padx=(0, 0))
    entrada_voto.focus_set()

    numeros = []

    def on_key_press(event):
        # Permite apenas números, backspace e delete
        if event.char.isdigit():
            numeros.append(event.char)
            print(numeros)

            entrada_voto.delete(0, tk.END)
            entrada_voto.insert(0, ''.join(numeros))
            filtrar_candidatos(''.join(numeros))

        elif event.keysym in ('BackSpace', 'Delete'):
            if numeros:
                numeros.pop()
                entrada_voto.delete(0, tk.END)
                entrada_voto.insert(0, ''.join(numeros))
                filtrar_candidatos(''.join(numeros))
        return "break"  # Impede o comportamento padrão do Entry

    # Vincula o evento de teclado
    entrada_voto.bind("<Key>", on_key_press)

    imagens_tk = []

    def filtrar_candidatos(numero):
        for widget in inner_frame.winfo_children():
            widget.destroy()

        for candidato in candidatos_json:
            numero_candidato = candidato["numero"]

            # Verifica se o número do candidato começa com os dígitos já digitados
            if numero_candidato.startswith(numero):
                # Carrega a imagem
                imagem = Image.open(candidato["imagem"])
                imagem = imagem.resize((150, 150))  # Redimensiona se necessário
                imagem_tk = ImageTk.PhotoImage(imagem)
                imagens_tk.append(imagem_tk)  # Guarda a referência

                # Cria e exibe um Label com a imagem
                label_imagem = tk.Label(inner_frame, image=imagem_tk)
                label_imagem.pack(pady=20)

                # Cria e exibe um Label com o nome do candidato
                label_nome = tk.Label(inner_frame, text=f"{candidato['nome']} ({numero_candidato})")
                label_nome.pack()
                print(f"Candidato possível: {candidato['nome']} (número: {numero_candidato})")

        
    
    # entrada_voto.bind("<Key>", tecla_pressionada)

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

    
    tk.Button(main_frame, text="Confirmar Voto", command=confirmar_voto, 
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