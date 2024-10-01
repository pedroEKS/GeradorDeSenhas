import random
import string
import tkinter as tk
from tkinter import messagebox
import pyperclip
from cryptography.fernet import Fernet

def gerar_chave():
    return Fernet.generate_key()

def criptografar_senha(senha, chave): #Função de criptografar 
    f = Fernet(chave)
    return f.encrypt(senha.encode())

def gerar_senha(tamanho, incluir_maiusculas, incluir_minusculas, incluir_numeros, incluir_simbolos):
    caracteres = ''
    if incluir_maiusculas:
        caracteres += string.ascii_uppercase
    if incluir_minusculas:
        caracteres += string.ascii_lowercase
    if incluir_numeros:
        caracteres += string.digits
    if incluir_simbolos:
        caracteres += string.punctuation

    if not caracteres:
        return "Selecione pelo menos um tipo de caractere."

    senha = ''.join(random.choice(caracteres) for _ in range(tamanho))
    return senha

def avaliar_forca_senha(senha): #Avalição da força da senha
    length = len(senha)
    has_upper = any(c.isupper() for c in senha)
    has_lower = any(c.islower() for c in senha)
    has_digit = any(c.isdigit() for c in senha)
    has_symbol = any(c in string.punctuation for c in senha)

    score = sum([has_upper, has_lower, has_digit, has_symbol])

    if length >= 12 and score >= 3:
        return "Senha forte"
    elif length >= 8 and score >= 2:
        return "Senha média"
    else:
        return "Senha fraca"

def copiar_para_clipboard(senha): #Copia a senha
    pyperclip.copy(senha)
    messagebox.showinfo("Copiar", "Senha copiada para a área de transferência!")

def salvar_senha(senha, chave):# Salva a senha em um arquivo
    senha_criptografada = criptografar_senha(senha, chave)
    with open("senhas.txt", "a") as file:
        file.write(senha_criptografada.decode() + "\n")
    messagebox.showinfo("Salvar", "Senha salva com sucesso!")

# Interface gráfica (Tkinter)
def criar_interface():
    # Janela principal
    root = tk.Tk()
    root.title("Gerador de Senhas Seguras")

    lbl_tamanho = tk.Label(root, text="Tamanho da senha:")
    lbl_tamanho.pack()
    entry_tamanho = tk.Entry(root)
    entry_tamanho.pack()

    var_maiusculas = tk.BooleanVar()
    var_minusculas = tk.BooleanVar()
    var_numeros = tk.BooleanVar()
    var_simbolos = tk.BooleanVar()

    tk.Checkbutton(root, text="Incluir Letras Maiúsculas", variable=var_maiusculas).pack()
    tk.Checkbutton(root, text="Incluir Letras Minúsculas", variable=var_minusculas).pack()
    tk.Checkbutton(root, text="Incluir Números", variable=var_numeros).pack()
    tk.Checkbutton(root, text="Incluir Símbolos", variable=var_simbolos).pack()

    def gerar(): # Botão para gerar senha
        tamanho = int(entry_tamanho.get())
        incluir_maiusculas = var_maiusculas.get()
        incluir_minusculas = var_minusculas.get()
        incluir_numeros = var_numeros.get()
        incluir_simbolos = var_simbolos.get()

        senha = gerar_senha(tamanho, incluir_maiusculas, incluir_minusculas, incluir_numeros, incluir_simbolos)
        lbl_senha.config(text=senha)

        # Avaliar força da senha
        forca = avaliar_forca_senha(senha)
        lbl_forca.config(text=f"Força da senha: {forca}")

    btn_gerar = tk.Button(root, text="Gerar Senha", command=gerar)
    btn_gerar.pack()

    # Exibir senha gerada
    lbl_senha = tk.Label(root, text="")
    lbl_senha.pack()

    # Exibir força da senha
    lbl_forca = tk.Label(root, text="")
    lbl_forca.pack()

    # Botão para copiar a senha
    btn_copiar = tk.Button(root, text="Copiar Senha", command=lambda: copiar_para_clipboard(lbl_senha.cget("text")))
    btn_copiar.pack()

    # Botão para salvar a senha
    chave = gerar_chave()  
    btn_salvar = tk.Button(root, text="Salvar Senha", command=lambda: salvar_senha(lbl_senha.cget("text"), chave))
    btn_salvar.pack()

    root.mainloop()

if __name__ == "__main__":
    criar_interface()