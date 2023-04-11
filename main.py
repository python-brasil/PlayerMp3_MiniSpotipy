import time
import pygame
import tkinter as tk
from tkinter import ttk
from tkinter import *
from Functions import *
import os
import fnmatch
from tkinter import filedialog
from tkinter import messagebox
import pickle as pkl

class Mp3():
    
    def __init__(self):
        # Configuracoes da janela
        self.root = tk.Tk()
        self.root.title("SPOTIPY")
        self.root.geometry(center(self.root,620,300))
        self.root.config(bg="black")
        self.root.resizable(False, False)
        
        # Variaveis de iniciais
        self.img_logo = PhotoImage(file=r"img\LOGO-SPOTIPY.png")
        self.img_lupa = PhotoImage(file=r"img\icone_lupa.png")
        self.img_btn_play = PhotoImage(file=r"img\btn_play.png")
        self.img_btn_pause = PhotoImage(file=r"img\btn_pause.png")
        self.jan_config = None
        pygame.mixer.init()
        # Funcoes essenciais
        self.containers()
        self.lista_musicas()
        self.itens_sub01_container01()
        self.itens_sub02_container01()
        self.itens_container02()
        # self.mp3_config()
        # self.update_progress()
        
        # Inicializacao da janela
        self.root.mainloop()

    def containers(self):
        self.fr_container01 = tk.Frame(
            self.root,
            height=300,
            width=500,
            bg='blue'
            )
        
        self.fr_container02 = tk.Frame(
            self.root,
            height=300,
            width=120,
            bg="black"
            )
        
        self.fr_sub01_container01 = tk.Frame(
            self.fr_container01,
            bg='green',
            height=230,
            width=500,
        )
        
        self.fr_sub02_container01 = tk.Frame(
            self.fr_container01,
            bg='gray',
            height=70,
            width=500,
        )
        self.fr_container01.propagate(0)
        self.fr_container02.propagate(0)
        self.fr_sub01_container01.propagate(0)
        self.fr_sub02_container01.propagate(0)
        self.fr_container02.pack(side=LEFT)
        self.fr_container01.pack(side=LEFT)
        self.fr_sub01_container01.pack()
        self.fr_sub02_container01.pack()
               
    def itens_sub01_container01(self):
        
        self.search_var = tk.StringVar()
        self.fr_container_pesquisa = Frame(
            self.fr_sub01_container01,
        )
        self.lb_img_lupa = Label(
            self.fr_container_pesquisa,
            bg='#00d856',
            image=self.img_lupa,
        )
        self.search_box = tk.Entry(
            self.fr_container_pesquisa,
            bg='#1c1c1c',
            fg='#fff',
            width=380,
            textvariable=self.search_var,
            bd=0,
            highlightthickness=1,
            highlightbackground='#00d856',
            highlightcolor='#00d856',
        )
        self.fr_container_pesquisa.pack()
        self.lb_img_lupa.pack(side=LEFT)
        self.search_box.pack(side=LEFT)
        
        self.scrollbar = ttk.Scrollbar(
            self.fr_sub01_container01,
            )
        
        #self.scrollbar.pack(side="right", fill="y")
        
        self.lista = tk.Listbox(
            self.fr_sub01_container01, 
            #yscrollcommand=self.scrollbar.set,
            highlightthickness = 0,
            bd=0,
            bg='#1c1c1c',
            fg='#fff',
            selectmode=tk.SINGLE,
            selectbackground='#343434',
            justify='left'
            )
        
        for i in self.arquivos_mp3:
            self.lista.insert(tk.END, i)
        
        self.lista.bind('<<ListboxSelect>>', self.on_select)   
         
        self.lista.pack(fill="both", expand=True)
        # Associa a scrollbar com o widget que ela controla
        self.scrollbar.config(command=self.lista.yview)
        
        def filter_listbox(*args):
            search_term = self.search_var.get()
            self.lista.delete(0, tk.END)
            for item in self.arquivos_mp3:
                if search_term.lower() in item.lower():
                    self.lista.insert(tk.END, item)
        self.search_var.trace('w', filter_listbox)
        
        for item in self.arquivos_mp3:
            self.lista.insert(tk.END, item)
        filter_listbox()
         
    def itens_container02(self):
        self.lb_img_logo = Label(
            self.fr_container02,
            image=self.img_logo,
            bg='black',
        )
        
        self.btn_procurar_msc = Button(
            self.fr_container02,
            text='Find Music',
            bg='black',
            activebackground='#00d856',
            fg='white',
            width=19,
            bd=0,
            command=self.update_lista_msc
        )
        
        self.btn_config = Button(
            self.fr_container02,
            text='Configuração',
            bg='black',
            activebackground='#00d856',
            fg='white',
            width=19,
            bd=0,
            command=self.win_config
        )
        
        self.lb_img_logo.pack(pady=10)
        self.btn_procurar_msc.pack()
        self.btn_config.pack()
       
    def itens_sub02_container01(self):
        
        style = ttk.Style()
        style.theme_use('alt')

        style.configure(
            'custom.Horizontal.TProgressbar', 
            troughcolor='gray', 
            background='#00d856',
            thickness=5
            )    
            
        self.progress_bar = ttk.Progressbar(
            self.fr_sub02_container01, 
            style='custom.Horizontal.TProgressbar',
            orient="horizontal", 
            length=500,
            mode="determinate"
            )
        
        self.play_button = Button(
            self.fr_sub02_container01, 
            image=self.img_btn_play,  
            bd=0,
            bg='gray',
            activebackground='gray',
            command=self.play_music
            )

        self.progress_bar.pack()
        self.play_button.pack(pady=10)
   
    def lista_musicas(self):
        self.arquivos_mp3 = []
        def find_mp3_files(start_dir):
            for dirpath, dirnames, filenames in os.walk(start_dir):
                for filename in filenames:
                    if fnmatch.fnmatch(filename, '*.mp3'):
                        yield os.path.join(filename)

        if os.path.exists('arquivo_geral_configuracao.pickle'):
            with open('arquivo_geral_configuracao.pickle', 'rb') as f:
                dados_recuperados = pkl.load(f)
            start_dir = dados_recuperados['diretorio padrao']
          
        # Define o diretório inicial onde a busca deve começar
        else:
            start_dir = '/'
        # Chama a função find_mp3_files para encontrar todos os arquivos mp3 em todos os diretórios do sistema de arquivos
        for mp3_file in find_mp3_files(start_dir):
            self.arquivos_mp3.append(mp3_file.replace('.mp3',''))  
        self.arquivos_mp3 = sorted(self.arquivos_mp3)
                
    def update_lista_msc(self):
        self.directory = filedialog.askdirectory()
        
        self.lista.delete(0, tk.END)
        
        self.arquivos_mp3 = []
        
        def find_mp3_files(start_dir):
            for dirpath, dirnames, filenames in os.walk(start_dir):
                for filename in filenames:
                    if fnmatch.fnmatch(filename, '*.mp3'):
                        yield os.path.join(filename)

        # Define o diretório inicial onde a busca deve começar
        start_dir = self.directory
        # Chama a função find_mp3_files para encontrar todos os arquivos mp3 em todos os diretórios do sistema de arquivos
        for mp3_file in find_mp3_files(start_dir):
            self.arquivos_mp3.append(mp3_file.replace('.mp3',''))  
        self.arquivos_mp3 = sorted(self.arquivos_mp3)
        
        #Se caso a pasta não conter nenhum arquivo mp3 ele buscara todos os arquivos .mp3 do PC
        if len(self.arquivos_mp3) == 0:
            messagebox.showwarning("NENHUM ARQUIVO", "Nenhum arquivo .mp3 encontrado")
            self.lista_musicas()
            for i in self.arquivos_mp3:
                self.lista.insert(tk.END, i)
        else:
            for i in self.arquivos_mp3:
                self.lista.insert(tk.END, i)      
    
    def pegar_pasta_padrao(self):
        self.diretorio_padrao = filedialog.askdirectory()
    
    def salvar_config(self):
        try:
            print(self.diretorio_padrao)
            self.arquivo_geral_configuracao = {'diretorio padrao': self.diretorio_padrao}
        
            self.en_input_pasta_padrao.insert(0, self.arquivo_geral_configuracao['diretorio padrao'])
            
            if os.path.exists('arquivo_geral_configuracao.pickle'):
                with open('arquivo_geral_configuracao.pickle', 'rb') as f:
                    dados_recuperados = pkl.load(f)
                    
                dados_recuperados['diretorio padrao'] = self.diretorio_padrao
                
                with open('arquivo_geral_configuracao.pickle', 'wb') as f:
                    pkl.dump(dados_recuperados, f)
            else:
                with open('arquivo_geral_configuracao.pickle', 'wb') as f:
                    pkl.dump(self.arquivo_geral_configuracao, f)
                    
            messagebox.showinfo("Configurações", "Configurações Salvas")
            self.lista.delete(0, tk.END)
            
            def find_mp3_files(start_dir):
                for dirpath, dirnames, filenames in os.walk(start_dir):
                    for filename in filenames:
                        if fnmatch.fnmatch(filename, '*.mp3'):
                            yield os.path.join(filename)
                            
            for mp3_file in find_mp3_files(dados_recuperados['diretorio padrao']):
                self.arquivos_mp3.append(mp3_file.replace('.mp3',''))  
            self.arquivos_mp3 = sorted(self.arquivos_mp3)
            
            #Se caso a pasta não conter nenhum arquivo mp3 ele buscara todos os arquivos .mp3 do PC
            if len(self.arquivos_mp3) == 0:
                messagebox.showwarning("NENHUM ARQUIVO", "Nenhum arquivo .mp3 encontrado")
                self.lista_musicas()
                for i in self.arquivos_mp3:
                    self.lista.insert(tk.END, i)
            else:
                for i in self.arquivos_mp3:
                    self.lista.insert(tk.END, i)
                
            
        except AttributeError:
            messagebox.showinfo("Configurações", "Nenhuma alteração foi feita")
      
    def win_config(self):
        if self.jan_config is None:
            self.jan_config =Tk()
            self.jan_config.protocol("WM_DELETE_WINDOW", self.fecha_win_config)
            self.jan_config.title("Configurações")
            self.jan_config.geometry(center(self.jan_config,300,200))
            self.jan_config.resizable(False, False)
            self.jan_config.config(bg='black')
            
            self.lb_pasta_padrao = Label(
                self.jan_config,
                text='Pasta Padrão:',
                font='Calibri 8',
                bg='black',
                fg='gray'
            )
            
            self.btn_pasta_padrao = Button(
                self.jan_config,
                text='Pesquisar',
                fg='white',
                bg='#00d856',
                activebackground='#00d856',
                activeforeground='black',
                bd=0,
                command=self.pegar_pasta_padrao
            )
            self.en_input_pasta_padrao = Entry(
                self.jan_config,
                bg='black',
                fg='white',
                width=30,
                font='Calibri 11',
                bd=0,
                highlightthickness=1,
                highlightbackground='#00d856',
                highlightcolor='#00d856',
            )
            self.btn_salvar = Button(
                self.jan_config,
                text='Salvar',
                fg='white',
                bg='#00d856',
                activebackground='#00d856',
                activeforeground='black',
                bd=0,
                command=self.salvar_config
            )
            
            self.lb_pasta_padrao.grid(row=0, columnspan=1, sticky=E)
            self.btn_pasta_padrao.grid(row=1, column=0, sticky=E)
            self.en_input_pasta_padrao.grid(row=1, column=1, sticky=W)
            self.btn_salvar.grid(row=2, column=1, sticky=E,pady=5)
            
            if os.path.exists('arquivo_geral_configuracao.pickle'):
                with open('arquivo_geral_configuracao.pickle', 'rb') as f:
                    dados_recuperados = pkl.load(f)
                self.en_input_pasta_padrao.insert(tk.END, dados_recuperados['diretorio padrao'])
        else:
            # Se já foi, basta colocá-la na frente
            self.jan_config.lift()
            
    def fecha_win_config(self):
        # Seta de novo em None para recriar quando abrir
        self.jan_config.destroy()
        self.jan_config = None  
    
    def on_select(self, event):
        # Obter o índice do item selecionado
        index = event.widget.curselection()[0]
        # Obter o valor do item a partir do índice
        value = event.widget.get(index)
        # Imprimir o valor do item selecionado
        if os.path.exists('arquivo_geral_configuracao.pickle'):
            with open('arquivo_geral_configuracao.pickle', 'rb') as f:
                dados_recuperados = pkl.load(f)
        else:
            with open('arquivo_geral_configuracao.pickle', 'wb') as f:
                pkl.dump(self.arquivo_geral_configuracao, f)
        print(dados_recuperados['diretorio padrao']+'/'+value)
        # self.path_audio = dados_recuperados['diretorio padrao']+'/'+value
        # self.mp3_config
        self.audio_file = dados_recuperados['diretorio padrao']+'/'+value+'.mp3'
        time.sleep(2)
        pygame.mixer.music.load(self.audio_file)
        self.audio_info = pygame.mixer.Sound(self.audio_file).get_length() * 1000
        # self.update_progress() 
        self.play_music()
        
    def mp3_config(self):
        pygame.mixer.init()
        # if self.path_audio is not None:
        #     print('opa')
        # else:
        # self.audio_file = ''
        # pygame.mixer.music.load(self.audio_file)
        # self.audio_info = pygame.mixer.Sound(self.audio_file).get_length() * 1000
        
    def update_progress(self):
        self.current_time = pygame.mixer.music.get_pos()  # Obtenha o tempo atual em milissegundos
        self.progress_bar["value"] = self.current_time / self.audio_info * 100  # Calcule o valor da barra de progresso
        self.fr_container02.after(50, self.update_progress)  # Atualize a barra de progresso a cada 50 milissegundos
        self.fr_container02.mainloop()

    def criar_btn_play(self):
        self.play_button = Button(
            self.fr_sub02_container01, 
            image=self.img_btn_play,  
            bd=0,
            bg='gray',
            activebackground='gray',
            command=self.play_music
            )
        
        self.current_time = pygame.mixer.music.get_pos()  # Obtenha o tempo atual em milissegundos
        self.progress_bar["value"] = self.current_time / self.audio_info * 100  # Calcule o valor da barra de progresso
        
        self.play_button.pack(pady=10)    
    
    def criar_btn_pause(self):
        self.pause_button = Button(
            self.fr_sub02_container01, 
            image=self.img_btn_pause,  
            bd=0,
            bg='gray',
            activebackground='gray',
            command=self.pause_music
            )
        self.pause_button.pack(pady=10)  
        
    def play_music(self):
        pygame.mixer.music.play()
        self.play_button.destroy()
        self.criar_btn_pause()
        
    def pause_music(self):
        pygame.mixer.music.pause()
        self.pause_button.destroy()
        self.criar_btn_play()
        
Mp3()