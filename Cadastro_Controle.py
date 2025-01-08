import sqlite3 as sql
import tkinter
from tkinter import ttk
from tkcalendar import DateEntry
from tkinter import messagebox
import smtplib
import email.message
from threading import Thread
import schedule
import time
from datetime import datetime

conn = sql.connect('Dados_Projetos.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS cadastros(
               id INTEGER PRIMARY KEY AUTOINCREMENT, 
               projeto TEXT NOT NULL,
               responsavel TEXT NOT NULL,
               email TEXT NOT NULL,
               previsão TEXT NOT NULL,
               status TEXT NOT NULL,
               prazo TEXT NOT NULL
               )'''
               )




def enviar_email():
    dif = 10

    if dif <= 3:
        corpo_email = """
        <p>Olá, Matheus Marques.</p>
        <p>Você está de Parabéns pela namorada que tem muito zica!</p>
        """

        msg = email.message.Message()
        msg['Subject'] = "Primeiro Teste"
        msg['From'] = 'testepy42@gmail.com'
        msg['To'] = 'testepy42@gmail.com'
        password = 'kndp ltga tuzs zdty' 
        msg.add_header('Content-Type', 'text/html')
        msg.set_payload(corpo_email)

        s = smtplib.SMTP('smtp.gmail.com: 587')
        s.starttls()
        # Login Credentials for sending the mail
        s.login(msg['From'], password)
        s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))
        print('Email enviado')
    else:
        print("Dentro do prazo")


def janela_cadastrar():
    janela02 = tkinter.Tk()

    

    texto_projeto = label(janela02, text="Projeto", font=("Arial", 12))
    texto_projeto.grid(column=0, row=1, padx=10, pady=10)
    projeto_cad = entrada(janela02, width=30, font=("Arial", 12))
    projeto_cad.grid(column=0, row=2, padx=10, pady=10)

    texto_responsavel = label(janela02, text="Responsavel", font=("Arial", 12))
    texto_responsavel.grid(column=1, row=1, padx=10, pady=10)
    responsavel_cad = entrada(janela02, width=30, font=("Arial", 12))
    responsavel_cad.grid(column=1, row=2, padx=10, pady=10)

    texto_email = label(janela02, text="Email", font=("Arial", 12))
    texto_email.grid(column=2, row=1, padx=10, pady=10)
    email_cad = entrada(janela02, width=30, font=("Arial", 12))
    email_cad.grid(column=2, row=2, padx=10, pady=10)

    texto_previsao = label(janela02, text="Previsão", font=("Arial", 12))
    texto_previsao.grid(column=3, row=1, padx=10, pady=10)
    previsao_cad = DateEntry(janela02, date_pattern="dd/MM/yyyy")
    previsao_cad.grid(column=3, row=2, padx=10, pady=10)

    texto_status = label(janela02, text="Status", font=("Arial", 12))
    texto_status.grid(column=4, row=1, padx=10, pady=10)
    status_cad = susp(janela02, values=["Finalizado", "Pendente", "Atrasado"], state="readonly")  # Apenas leitura
    status_cad.set("Selecione uma opção")  # Valor padrão
    status_cad.grid(column=4, row=2, padx=10, pady=10)

    texto_prazo = label(janela02, text="Prazo", font=("Arial", 12))
    texto_prazo.grid(column=5, row=1, padx=10, pady=10)
    prazo_cad = DateEntry(janela02, date_pattern="dd/MM/yyyy")
    prazo_cad.grid(column=5, row=2, padx=10, pady=10)

    def cadastrar():
         
        projeto = projeto_cad.get()
        responsavel = responsavel_cad.get()
        email = email_cad.get()
        previsao = previsao_cad.get()
        status = status_cad.get()
        prazo = prazo_cad.get()

        if not projeto or not previsao or not status or not prazo:
                    print("Todos os campos precisam ser preenchidos!")
                    return

        cursor.execute('''
            INSERT INTO
                        cadastros (projeto, responsavel, email, previsão, status, prazo)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (projeto, responsavel, email, previsao, status, prazo))
            
        conn.commit()
        print("Cadastro Realizado com sucesso")

        projeto_cad.delete(0, tkinter.END)
        responsavel_cad.delete(0, tkinter.END)
        email_cad.delete(0, tkinter.END)
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

    listbox = tkinter.Listbox(janela_lista, width=100, height=15, font=("Arial", 10))
    listbox.pack(pady=15)

    
    for linha in linhas_para_exibir:
        listbox.insert(tkinter.END, f"ID: {linha[0]} | Projeto: {linha[1]} | Responsavel: {linha[2]} | Email: {linha[3]} | Previsão: {linha[4]} | Status: {linha[5]} | Prazo: {linha[6]}")

    botao_fechar = tkinter.Button(janela_lista, text="Fechar", command=janela_lista.destroy)
    botao_fechar.pack(pady=10)

    janela_lista.mainloop()

def alterar_projeto_tk():
    # Janela para alterar projetos
    janela_alterar = tkinter.Tk()
    janela_alterar.title("Alterar Projeto")

    cursor.execute("SELECT * FROM cadastros")
    projetos = cursor.fetchall()

    label_titulo = tkinter.Label(janela_alterar, text="Selecione um Projeto para Alterar", font=("Arial", 14))
    label_titulo.grid(column=0, row=0, padx=10, pady=10, columnspan=2)

    # Listbox para exibir os projetos
    listbox = tkinter.Listbox(janela_alterar, width=100, height=15, font=("Arial", 12))
    for projeto in projetos:
        listbox.insert(tkinter.END, f"ID: {projeto[0]} | Projeto: {projeto[1]} | Responsavel: {projeto[2]} | Email: {projeto[3]} | Previsão: {projeto[4]} | Status: {projeto[5]} | Prazo: {projeto[6]}")
    listbox.grid(column=0, row=1, padx=10, pady=10, columnspan=2)

    # Campos para edição
    labels = ["Projeto", "Responsavel", "Email", "Previsão", "Status", "Prazo"]
    entradas = {}
    for i, label_text in enumerate(labels):
        label = tkinter.Label(janela_alterar, text=f"Novo {label_text}:", font=("Arial", 12))
        label.grid(column=0, row=2+i, padx=10, pady=5)
        if label_text in ["Previsão", "Prazo"]:
            entrada = DateEntry(janela_alterar, date_pattern="dd/MM/yyyy")
        elif label_text == "Status":
            entrada = ttk.Combobox(janela_alterar, values=["Finalizado", "Pendente", "Atrasado"], state="readonly")
            entrada.set("Selecione uma opção")
        else:
            entrada = tkinter.Entry(janela_alterar, font=("Arial", 12))
        entrada.grid(column=1, row=2+i, padx=10, pady=5)
        entradas[label_text.lower()] = entrada

    def carregar_projeto(event):
        # Recupera o projeto selecionado na lista
        selecionado = listbox.curselection()
        if not selecionado:
            return
        index = selecionado[0]
        projeto = projetos[index]
        
        # Preenche os campos com os valores do projeto selecionado
        entradas["projeto"].delete(0, tkinter.END)
        entradas["projeto"].insert(0, projeto[1])
        entradas["responsavel"].delete(0, tkinter.END)
        entradas["responsavel"].insert(0, projeto[2])
        entradas["email"].delete(0, tkinter.END)
        entradas["email"].insert(0, projeto[3])
        entradas["previsão"].set_date(projeto[4])
        entradas["status"].set(projeto[5])
        entradas["prazo"].set_date(projeto[6])

    listbox.bind("<<ListboxSelect>>", carregar_projeto)

    def salvar_alteracoes():
        selecionado = listbox.curselection()
        if not selecionado:
            messagebox.showerror("Erro", "Nenhum projeto selecionado!")
            return
        index = selecionado[0]
        id_projeto = projetos[index][0]

        novos_valores = {
            "projeto": entradas["projeto"].get().strip(),
            "responsavel": entradas["responsavel"].get().strip(),
            "email": entradas["email"].get().strip(),
            "previsão": entradas["previsão"].get(),
            "status": entradas["status"].get(),
            "prazo": entradas["prazo"].get(),
        }

        for coluna, valor in novos_valores.items():
            if valor:
                cursor.execute(f"UPDATE cadastros SET {coluna} = ? WHERE id = ?", (valor, id_projeto))

        conn.commit()
        messagebox.showinfo("Sucesso", "Projeto alterado com sucesso!")
        janela_alterar.destroy()

    botao_salvar = tkinter.Button(janela_alterar, text="Salvar Alterações", font=("Arial", 12), command=salvar_alteracoes)
    botao_salvar.grid(column=0, row=6, columnspan=2, pady=10)

    botao_fechar = tkinter.Button(janela_alterar, text="Fechar", font=("Arial", 12), command=janela_alterar.destroy)
    botao_fechar.grid(column=0, row=7, columnspan=2, pady=10)

    janela_alterar.mainloop()

entrada = tkinter.Entry
janela = tkinter.Tk()
label = tkinter.Label
botao = tkinter.Button
susp = ttk.Combobox
janela.title("SGMP")

titulo_principal = label(janela, text = "GERENCIADOR DE PROJETOS", font=("Arial", 16))
titulo_principal.grid(column=1, row=0, padx=10, pady=10)

botao_cadastrar = botao(janela, text = "Cadastrar", command=janela_cadastrar)
botao_cadastrar.grid(column=0, row=1, padx=10, pady=10)

botao_exibir = botao(janela, text="Exibir Projetos", command=exibir_projetos)
botao_exibir.grid(column=1, row=1, padx=10, pady=10)

botao_alterar = botao(janela, text="Alterar Projeto", command=alterar_projeto_tk)
botao_alterar.grid(column=2, row=1, padx=10, pady=10)

janela.geometry("520x400")

def ini_agen():
    schedule.every().second.do(enviar_email)
    while True:
        schedule.run_pending()
        time.sleep(1)

thread_agendamento = Thread(target=ini_agen)
thread_agendamento.daemon = True
thread_agendamento.start()


cursor.execute("SELECT * FROM cadastros")
projetos10 = cursor.fetchall()
print(projetos10)

janela.mainloop()



