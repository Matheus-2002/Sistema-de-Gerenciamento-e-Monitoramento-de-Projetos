import sqlite3 as sql
import tkinter

conn = sql.connect('Dados_Projetos.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS cadastros(
               id INTEGER PRIMARY KEY AUTOINCREMENT, 
               projeto TEXT NOT NULL,
               previsão TEXT NOT NULL,
               status TEXT NOT NULL,
               prazo TEXT NOT NULL
               )'''
               )







def janela_cadastrar():
    janela02 = tkinter.Tk()

    

    texto_projeto = label(janela02, text="Projeto", font=("Arial", 12))
    texto_projeto.grid(column=0, row=1, padx=10, pady=10)
    projeto_cad = entrada(janela02, width=30, font=("Arial", 12))
    projeto_cad.grid(column=0, row=2, padx=10, pady=10)

    texto_previsao = label(janela02, text="Previsão", font=("Arial", 12))
    texto_previsao.grid(column=1, row=1, padx=10, pady=10)
    previsao_cad = entrada(janela02, width=30, font=("Arial", 12))
    previsao_cad.grid(column=1, row=2, padx=10, pady=10)

    texto_status = label(janela02, text="Status", font=("Arial", 12))
    texto_status.grid(column=2, row=1, padx=10, pady=10)
    status_cad = entrada(janela02, width=30, font=("Arial", 12))
    status_cad.grid(column=2, row=2, padx=10, pady=10)

    texto_prazo = label(janela02, text="Prazo", font=("Arial", 12))
    texto_prazo.grid(column=3, row=1, padx=10, pady=10)
    prazo_cad = entrada(janela02, width=30, font=("Arial", 12))
    prazo_cad.grid(column=3, row=2, padx=10, pady=10)

    def cadastrar():
         
        projeto = projeto_cad.get()
        previsao = previsao_cad.get()
        status = status_cad.get()
        prazo = prazo_cad.get()

        if not projeto or not previsao or not status or not prazo:
                    print("Todos os campos precisam ser preenchidos!")
                    return

        cursor.execute('''
            INSERT INTO
                        cadastros (projeto, previsão, status, prazo)
            VALUES (?, ?, ?, ?)
        ''', (projeto, previsao, status, prazo))
            
        conn.commit()
        print("Cadastro Realizado com sucesso")

        projeto_cad.delete(0, tkinter.END)
        previsao_cad.delete(0, tkinter.END)
        status_cad.delete(0, tkinter.END)
        prazo_cad.delete(0, tkinter.END)

    cadastramento = botao(janela02, text="Cadastrar", command= cadastrar)
    cadastramento.grid(row=3, column=1, columnspan=2, pady=10)


def exibir_projetos():
    cursor.execute("SELECT * FROM cadastros")
    todas_as_linhas = cursor.fetchall()

    
    if len(todas_as_linhas) > 10:
        
        linhas_para_exibir = todas_as_linhas[:5] + todas_as_linhas[-5:]
    else:
        
        linhas_para_exibir = todas_as_linhas

    
    janela_lista = tkinter.Tk()
    janela_lista.title("Exibir Projetos")

    titulo = tkinter.Label(janela_lista, text="Lista de Projetos", font=("Arial", 14))
    titulo.pack(pady=10)

    listbox = tkinter.Listbox(janela_lista, width=100, height=15, font=("Arial", 12))
    listbox.pack(pady=10)

    
    for linha in linhas_para_exibir:
        listbox.insert(tkinter.END, f"ID: {linha[0]} | Projeto: {linha[1]} | Previsão: {linha[2]} | Status: {linha[3]} | Prazo: {linha[4]}")

    botao_fechar = tkinter.Button(janela_lista, text="Fechar", command=janela_lista.destroy)
    botao_fechar.pack(pady=10)

    janela_lista.mainloop()

def alterar_projeto_tk():
    
    janela_alterar = tkinter.Tk()
    janela_alterar.title("Alterar Projeto")

    
    cursor.execute("SELECT * FROM cadastros")
    projetos = cursor.fetchall()

    label_titulo = tkinter.Label(janela_alterar, text="Selecione o ID do Projeto para Alterar", font=("Arial", 14))
    label_titulo.pack(pady=10)

    listbox = tkinter.Listbox(janela_alterar, width=100, height=15, font=("Arial", 12))
    for projeto in projetos:
        listbox.insert(tkinter.END, f"ID: {projeto[0]} | Projeto: {projeto[1]} | Previsão: {projeto[2]} | Status: {projeto[3]} | Prazo: {projeto[4]}")
    listbox.pack(pady=10)

    label_id = tkinter.Label(janela_alterar, text="ID do Projeto:", font=("Arial", 12))
    label_id.pack()
    entrada_id = tkinter.Entry(janela_alterar, font=("Arial", 12))
    entrada_id.pack(pady=5)

    
    campos = ["Projeto", "Previsão", "Status", "Prazo"]
    entradas = {}

    for campo in campos:
        label = tkinter.Label(janela_alterar, text=f"Novo {campo} (deixe vazio para não alterar):", font=("Arial", 12))
        label.pack()
        entrada = tkinter.Entry(janela_alterar, font=("Arial", 12))
        entrada.pack(pady=5)
        entradas[campo] = entrada

    
    def salvar_alteracoes():
        try:
            id_projeto = int(entrada_id.get())
        except ValueError:
            tkinter.messagebox.showerror("Erro", "Por favor, insira um ID válido.")
            return

        
        cursor.execute("SELECT * FROM cadastros WHERE id = ?", (id_projeto,))
        projeto_selecionado = cursor.fetchone()
        if not projeto_selecionado:
            tkinter.messagebox.showerror("Erro", "Projeto não encontrado.")
            return

        
        for campo, entrada in entradas.items():
            novo_valor = entrada.get().strip()
            if novo_valor:  
                coluna = campo.lower()
                cursor.execute(f"UPDATE cadastros SET {coluna} = ? WHERE id = ?", (novo_valor, id_projeto))

        conn.commit()
        tkinter.messagebox.showinfo("Sucesso", f"Projeto com ID {id_projeto} alterado com sucesso!")
        janela_alterar.destroy()

    
    botao_salvar = tkinter.Button(janela_alterar, text="Salvar Alterações", font=("Arial", 12), command=salvar_alteracoes)
    botao_salvar.pack(pady=10)

    
    botao_fechar = tkinter.Button(janela_alterar, text="Fechar", font=("Arial", 12), command=janela_alterar.destroy)
    botao_fechar.pack(pady=10)

    janela_alterar.mainloop()

entrada = tkinter.Entry
janela = tkinter.Tk()
label = tkinter.Label
botao = tkinter.Button
janela.title("SGMP")

titulo_principal = label(janela, text = "GERENCIADOR DE PROJETOS", font=("Arial", 16))
titulo_principal.grid(column=1, row=0, padx=10, pady=10)

botao_cadastrar = botao(janela, text = "Cadastrar", command=janela_cadastrar)
botao_cadastrar.grid(column=0, row=1, padx=10, pady=10)

botao_exibir = botao(janela, text="Exibir Projetos", command=exibir_projetos)
botao_exibir.grid(column=1, row=1, padx=10, pady=10)

botao_alterar = botao(janela, text="Alterar Projeto", command=alterar_projeto_tk)
botao_alterar.grid(column=2, row=1, padx=10, pady=10)


janela.mainloop()



