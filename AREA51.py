#AREA DESTINADA A REALIZAR TODO E QUALQUER TIPO DE TESTE DE CÓDIGO

import tkinter as tk

def on_select(event):
    # Obter o índice do item selecionado
    index = event.widget.curselection()[0]
    # Obter o valor do item a partir do índice
    value = event.widget.get(index)
    # Imprimir o valor do item selecionado
    print(value)

# Criar uma janela do tkinter
root = tk.Tk()

# Criar um campo Listbox e adicionar alguns itens
listbox = tk.Listbox(root)
listbox.insert(0, "Item 1")
listbox.insert(1, "Item 2")
listbox.insert(2, "Item 3")

# Associar a função on_select ao evento de seleção de um item
listbox.bind("<<ListboxSelect>>", on_select)

# Exibir o campo Listbox na janela
listbox.pack()

# Iniciar o loop de eventos da janela
root.mainloop()
