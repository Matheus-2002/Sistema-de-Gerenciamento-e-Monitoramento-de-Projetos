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


def view_projetos():
    cursor.execute("SELECT * FROM cadastros")
    todas_as_linhas = cursor.fetchall()
    for linha in todas_as_linhas:
        print(linha)

def alterar_projeto():
    view_projetos()  # Mostrar os projetos antes de escolher qual alterar

    id_projeto = int(input("\nDigite o ID do projeto que deseja alterar: "))
    print("O que deseja alterar?\n1 - Nome do Projeto\n2 - Previsão\n3 - Status\n4 - Prazo")
    escolha = int(input("Digite o número da opção: "))

    if escolha == 1:
        novo_valor = input("Digite o novo nome do projeto: ")
        coluna = "projeto"
    elif escolha == 2:
        novo_valor = input("Digite a nova previsão de término (DD/MM/AAAA): ")
        coluna = "previsão"
    elif escolha == 3:
        novo_valor = input("Digite o novo status do projeto: ")
        coluna = "status"
    elif escolha == 4:
        novo_valor = input("Digite o novo prazo (DD/MM/AAAA): ")
        coluna = "prazo"
    else:
        print("Opção inválida!")
        return

    # Atualizar o registro no banco de dados
    cursor.execute(f"UPDATE cadastros SET {coluna} = ? WHERE id = ?", (novo_valor, id_projeto))
    conn.commit()
    print(f"\nRegistro com ID {id_projeto} atualizado com sucesso!")

# Adicionar a opção no menu principal
print("CPFL - Controle de Projetos \n")
print("Selecione uma opção\n")
print("1-Cadastrar\n2-Exibir Projetos\n3-Alterar Projeto\n4-Sair")
escolha = int(input())
if escolha == 1:
    cadastrar()
elif escolha == 2:
    view_projetos()
elif escolha == 3:
    alterar_projeto()
elif escolha == 4:
    print("Saindo...")
else:
    print("Opção inválida!")

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

    


def cadastrar(projeto):

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



entrada = tkinter.Entry
janela = tkinter.Tk()
label = tkinter.Label
botao = tkinter.Button
janela.title("SGMP")

titulo_principal = label(janela, text = "GERENCIADOR DE PROJETOS", font=("Arial", 16))
titulo_principal.grid(column=1, row=0, padx=10, pady=10)

botao_cadastrar = botao(janela, text = "Cadastrar", command=janela_cadastrar)
botao_cadastrar.grid(column=1, row=1, padx=10, pady=10)

cadastramento = botao(janela02, text="Cadastrar", command= cadastrar)
cadastramento.grid(row=3, column=1, columnspan=2, pady=10)

janela.mainloop()



