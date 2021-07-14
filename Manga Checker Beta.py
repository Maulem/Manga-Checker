import tkinter as tk
from functools import partial
import win32api
from urllib.request import Request, urlopen
import json

###| Global |###
item_clicked  = ""
data_file = "data.json"
settings_file = "settings.json"
new_user = False
double_click_preventer = False

def cap_number_search(link):

    ###| Faz o download do HTML da pagina em questão |###
    try:
        req = Request(link, headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urlopen(req).read()
        
    except:
        return -1, "o link esta errado ou o site fora do ar!"

    ###| Checa se encontrou o número do capitulo |###
    result_number = webpage.find(b'container-box default color-brown')
    if result_number == -1:
        return -2, "não foi possivel achar o número de capitulos"

    ###| Checa se encontrou o nome do capitulo |###
    result_title = webpage.find(b'<title>')
    if result_title == -1:
        return -3, "não foi possivel achar o titulo da obra"

    is_a_number = True      #| Indica se o caractere encontrado é um número
    number_address = 141    #| Número de caracteres depois do result onde se encontra o número de capitulos
    number_list = []        #| Lista dos algarismos do número de capitulos
    number_string = ""      #| String que vai receber o número de capitulos

    ###| Vai checando os caracteres, se não for um algarismo ele para |###
    while is_a_number:
        is_a_number = False
        char = chr(webpage[result_number + number_address + 1])

        ##| Checa ver se o caractere encontrado é um algarismo |##
        for i in range(10):
            if char == str(i):
                number_list.append(char)
                is_a_number = True
                number_address += 1


    index = 0               #| Indice dos caracteres do titulo
    title_address = 7       #| Número de caracteres depois do result onde se encontra o titulo
    title_list = []         #| Lista dos caracteres do titulo
    title_string = ""       #| String que vai receber o titulo

    ###| Captura o titulo da pagina da web |###
    while True:
        char = chr(webpage[result_title + title_address + index])
        if char == '<':
            break
        title_list.append(char)
        index += 1

    ###| Salva a lista de algarismos/caracteres em uma string |###
    number_string = number_string.join(number_list)
    title_string = title_string.join(title_list)

    ###| Remove o resto do titulo |###
    cut = title_string.find(" MangÃ¡ (pt-BR) - MangaLivre")
    title_list.clear()
    for i in range(cut):
        title_list.append(title_string[i])
    title_string = ""
    title_string = title_string.join(title_list)

    return number_string, title_string

###| Checa se o arquivo settings.json existe |###
try:
    with open(settings_file, "r") as readed:
        settings = json.load(readed)
except:
    ##| Se não existe cria ele e coloca as configurações padrão |##
    default_settings = {
    "colour_theme"                  : "light",
    "version"                       : "beta"
    }
    settings = default_settings
    json_object = json.dumps(settings, indent = 4)
    with open(settings_file, "w") as outfile:
        outfile.write(json_object)

###| Checa se o arquivo data.json existe |###
try:
    with open(data_file, "r") as readed:
        links_dict = json.load(readed)
except:
    ##| Se não existe cria ele e coloca esses links de exemplo |##
    example_links = {
    "https://mangalivre.net/manga/kanojo-mo-kanojo/9386"               : ["Kanojo no Kanojo"                , 65 ],
    "https://mangalivre.net/manga/uzaki-chan-wa-asobitai/7365"         : ["Uzaki Chan Wa Asobitai"          , 82 ],
    "https://mangalivre.net/manga/ijiranaide-nagatoro-san/6938"        : ["Ijiranaide, Nagatoro San"        , 110],
    "https://mangalivre.net/manga/kanojo-okarishimasu/6763"            : ["Kanojo Okarishimasu"             , 203],
    "https://mangalivre.net/manga/boruto-naruto-next-generations/3637" : ["Boruto: Naruto Next Generations" , 59 ]
    }
    links_dict = example_links
    json_object = json.dumps(links_dict, indent = 4)
    with open(data_file, "w") as outfile:
        outfile.write(json_object)

    new_user = True     #| Ativa a mensagem de boas vindas

###| Light Setup |###
bg_colour               = "dodgerblue4"
main_colour             = bg_colour
item_colour             = "light sky blue"
font_colour             = "gray10"
button_colour           = "lightcyan2"
button_font_colour      = "gray10"
button_clicked_colour   = item_colour
text_bg_colour          = "white"
theme_mode              = "Modo escuro"

###| Dark Setup |###
if settings["colour_theme"] == "dark":

    bg_colour               = "#0f244a"
    main_colour             = bg_colour
    item_colour             = "gray11"
    font_colour             = "#cccccc"
    button_colour           = "#1a3970"
    button_font_colour      = "#cccccc"
    button_clicked_colour   = "#1e4385"
    text_bg_colour          = "DeepSkyBlue4"
    theme_mode              = "Modo claro"

main_window = tk.Tk()   #| Cria a janela principal

###| Mensagem de boas vindas assim que o mouse entra na tela |###
def new_user_message(event):
    global new_user
    if new_user:
        message =  "Olá, parece que é a sua primeira vez utilizando o programa!\n\n"
        message += "Por favor digite o link da pagina principal do Mangá (aquela que tem a lista de todos capitulos) "
        message += "que você quer checar e clique em 'Adicionar link' para coloca-lo na lista"
        message += "\n\nExemplo de link de uma pagina principal do Mangá: https://mangalivre.net/manga/boruto-naruto-next-generations/3637"
        message += "\n\nDepois disso, sempre que você quiser checar por novos capitulos é so clicar em 'Atualizar links'."
        message += "\n\nBotamos alguns links de exemplo, mas se preferir pode deleta-los clicando no link e depois em 'Deletar link'"
        win32api.MessageBox(0, message, "Bem vindo")
        new_user = False

###| Adiciona o link digitado na lista e no data.json |###
def add_click(botao):
    link = add_entry.get()
    if link != "":
        if link in links_dict:
            message = "O link: '" + link + "' já está na lista!"
            win32api.MessageBox(0, message, "Erro ao adicionar link")
        else:
            num_caps, series_name = cap_number_search(link)
            if int(num_caps) > 0:
                links_dict[link] = [series_name, int(num_caps)]
                listbox.insert(tk.END, link)
                add_entry.delete(0, len(link))

                json_object = json.dumps(links_dict, indent = 4)
                with open(data_file, "w") as outfile:
                    outfile.write(json_object)
            else:
                message = "O link: '" + link + "' não pode ser checado pois " + series_name
                win32api.MessageBox(0, message, "Erro ao adicionar link")

###| Deleta o link selecionado na lista e no data.json |###
def del_click(click):
    if click == False:
        global double_click_preventer
        double_click_preventer = True
        try:
            index = listbox.get(0, tk.END).index(item_clicked)
            listbox.delete(index)

            name_display.configure(text = "")
            number_display.configure(text = "")

            del links_dict[item_clicked]
            json_object = json.dumps(links_dict, indent = 4)
            with open(data_file, "w") as outfile:
                outfile.write(json_object)
        except:
            win32api.MessageBox(0, "Erro: nenhum link selecionado!\
            \n\nPor favor, selecione algum link da lista para ser deletado.",
            "Nenhum link selecionado")
        double_click_preventer = False

###| Atualiza todos os links de acordo com o site e adiciona na lista e no data.json |###
def att_click(botao):
    message = ""
    for link in links_dict:
        num_caps, series_name = cap_number_search(link)
        if int(num_caps) > 0:
            if int(links_dict[link][1]) != int(num_caps):
                links_dict[link] = [series_name, int(num_caps)]

                series_name = series_name + " tem novos capitulos!\n"
                message = message + series_name

                json_object = json.dumps(links_dict, indent = 4)
                with open(data_file, "w") as outfile:
                    outfile.write(json_object)
        else:
            series_name = "\n\rO link: " + link + " não pode ser checado!\nMotivo: " + series_name + "\n\n"
            message = message + series_name
    if message != "":
        win32api.MessageBox(0, message, "Novas atualizações!")
    else:
        win32api.MessageBox(0,  "Não há novas atualizações ainda...", "Sem novas atualizações")

###| Mostra como usar o programa para quem precisar de ajuda |###
def help_click(botao):
    message =  "Para adicionar um novo link na lista por favor digite o link da pagina principal do Mangá (aquela que tem a"
    message += " lista de todos capitulos) que você quer checar e clique em 'Adicionar link' para coloca-lo na lista"
    message += "\n\nExemplo de link de uma pagina principal do Mangá: https://mangalivre.net/manga/boruto-naruto-next-generations/3637"
    message += "\n\nDepois disso, sempre que você quiser checar por novos capitulos é so clicar em 'Atualizar links'."
    message += "\n\nBotamos alguns links de exemplo, mas se preferir pode deleta-los clicando no link e depois em 'Deletar link'"
    win32api.MessageBox(0, message, "Como usar o programa")

###| Mensagem de boas vindas assim que o mouse entra na tela |###
def theme_click(botao):
    global bg_colour, main_colour, item_colour, font_colour, button_colour
    global button_font_colour, button_clicked_colour, text_bg_colour, settings

    if settings["colour_theme"] == "dark":
        settings["colour_theme"] = "light"
        theme_but["text"] = "Modo escuro"
        
        ###| Light Setup |###
        bg_colour               = "dodgerblue4"
        main_colour             = bg_colour
        item_colour             = "light sky blue"
        font_colour             = "gray10"
        button_colour           = "lightcyan2"
        button_font_colour      = "gray10"
        button_clicked_colour   = item_colour
        text_bg_colour          = "white"

        json_object = json.dumps(settings, indent = 4)
        with open(settings_file, "w") as outfile:
            outfile.write(json_object)
            

    elif settings["colour_theme"] == "light":
        settings["colour_theme"] = "dark"
        theme_but["text"] = "Modo claro"

        ###| Dark Setup |###
        bg_colour               = "#0f244a"
        main_colour             = bg_colour
        item_colour             = "gray11"
        font_colour             = "#cccccc"
        button_colour           = "#1a3970"
        button_font_colour      = "#cccccc"
        button_clicked_colour   = "#1e4385"
        text_bg_colour          = "DeepSkyBlue4"

        json_object = json.dumps(settings, indent = 4)
        with open(settings_file, "w") as outfile:
            outfile.write(json_object)

    main_window["bg"] = bg_colour

    main_container["bg"] = main_colour

    name_text["bg"] = item_colour
    name_text["fg"] = font_colour

    name_display["bg"] = text_bg_colour
    name_display["fg"] = font_colour

    number_text["bg"] = item_colour
    number_text["fg"] = font_colour

    number_display["bg"] = text_bg_colour
    number_display["fg"] = font_colour

    title_text["bg"] = item_colour
    title_text["fg"] = font_colour

    add_but["bg"] = button_colour
    add_but["fg"] = button_font_colour
    add_but["activebackground"] = button_clicked_colour

    del_but["bg"] = button_colour
    del_but["fg"] = button_font_colour
    del_but["activebackground"] = button_clicked_colour

    att_but["bg"] = button_colour
    att_but["fg"] = button_font_colour
    att_but["activebackground"] = button_clicked_colour

    help_but["bg"] = button_colour
    help_but["fg"] = button_font_colour
    help_but["activebackground"] = button_clicked_colour

    theme_but["bg"] = button_colour
    theme_but["fg"] = button_font_colour
    theme_but["activebackground"] = button_clicked_colour

    add_entry["bg"] = text_bg_colour
    add_entry["fg"] = button_font_colour

    listbox["bg"] = text_bg_colour
    listbox["fg"] = font_colour

    list_container["bg"] = item_colour

    scr["bg"] = "red"

    ###| Cria e separa os espaços do grid |###
    for i in range(5):
        x = 0
        if i == 0:
            x = -18
        tk.Label(main_container, width = 20 + x, bg = main_colour).grid(row = 0, column = i)
    for i in range(9):
        x = -18
        tk.Label(main_container, width = 20 + x, bg = main_colour).grid(row = i, column = 0)


###| Cria um container no centro da tela onde ficarão todo o resto |###
main_container = tk.Label(main_window, width = 30, bg = main_colour, height = 10)
main_container.place(relx = 0.5, rely = 0.5, anchor = tk.CENTER)

###| Cria e separa os espaços do grid |###
for i in range(5):
    x = 0
    if i == 0:
        x = -18
    tk.Label(main_container, width = 20 + x, bg = main_colour).grid(row = 0, column = i)
for i in range(9):
    x = -18
    tk.Label(main_container, width = 20 + x, bg = main_colour).grid(row = i, column = 0)

###| Organiza todos os textos, botões, entradas e etc |###
name_text = tk.Label(main_container, text = "Nome da obra", width = 20, bg = item_colour, fg = font_colour)
name_text.grid(row = 4, column = 1, columnspan = 2, sticky = tk.W + tk.E)

name_display = tk.Label(main_container, text="", width=20, bg = text_bg_colour, fg = font_colour)
name_display.grid(row = 5, column = 1, columnspan = 2, sticky = tk.W + tk.E)

number_text = tk.Label(main_container, text = "Quantidade de capitulos", width = 19, bg = item_colour, fg = font_colour)
number_text.grid(row = 4, column = 3)

number_display = tk.Label(main_container, text = "", width=19, bg = text_bg_colour, fg = font_colour)
number_display.grid(row = 5, column = 3)

title_text = tk.Label(main_container, text = "Links pra procurar por atualizações:", width = 20, bg = item_colour, fg = font_colour)
title_text.grid(row = 1, column = 1, columnspan = 3, sticky = tk.W + tk.E)

add_but = tk.Button(main_container, width = 16, text = "Adicionar link", bg = button_colour, fg = button_font_colour,
activebackground = button_clicked_colour)
add_but["command"] = partial(add_click, add_but)
add_but.grid(row = 7, column = 3)

del_but = tk.Button(main_container, width = 16, text = "Deletar link", bg = button_colour, fg = button_font_colour,
activebackground = button_clicked_colour)
del_but["command"] = partial(del_click, double_click_preventer)
del_but.grid(row = 2, column = 4)

att_but = tk.Button(main_container, width = 16, text = "Atualizar links", bg = button_colour, fg = button_font_colour, cursor = "exchange",
activebackground = button_clicked_colour)
att_but["command"] = partial(att_click, att_but)
att_but.grid(row = 5, column = 4)

help_but = tk.Button(main_container, width = 16, text = "Ajuda", bg = button_colour, fg = button_font_colour,
activebackground = button_clicked_colour)
help_but["command"] = partial(help_click, help_but)
help_but.grid(row = 1, column = 4)

theme_but = tk.Button(main_container, width = 16, text = theme_mode, bg = button_colour, fg = button_font_colour,
activebackground = button_clicked_colour)
theme_but["command"] = partial(theme_click, theme_but)
theme_but.grid(row = 7, column = 4)

add_entry = tk.Entry(main_container, width = 24, bg = text_bg_colour, fg = button_font_colour)
add_entry.grid(row = 7, column = 1, columnspan = 2, sticky = tk.W + tk.E)

###| Callback se o usuário clicar em um elemento da lista |###
def callback(event):
    selection = event.widget.curselection()
    if selection:
        index = selection[0]
        data = event.widget.get(index)
        global item_clicked
        item_clicked = data
        name_display.configure(text = links_dict[data][0])
        number_display.configure(text = links_dict[data][1])
    else:
        name_display.configure(text = "")
        number_display.configure(text = "")

###| Cria o container onde a lista e a Scroll bar vão ficar |###
list_container = tk.Label(main_container, bg = item_colour, height = 10)
list_container.grid(row = 2, column = 1, columnspan = 3, sticky = tk.W + tk.E)

###| Cria a Scroll Bar |###
scr = tk.Scrollbar(list_container, bg = button_colour)
scr.pack(side = tk.RIGHT, fill = tk.Y)

###| Cria a lista |###
listbox = tk.Listbox(list_container, yscrollcommand = scr.set, bg = text_bg_colour, fg = font_colour)
for line in links_dict:
   listbox.insert(tk.END, line)
listbox.pack(side = tk.LEFT, fill = tk.BOTH, expand = True)
listbox.bind("<<ListboxSelect>>", callback)     #| Cria o evento de clicar em algo na lista

scr.config(command = listbox.yview)             #| Faz a Scroll Bar rolar a lista na vertical

main_window.bind("<Enter>", new_user_message)   #| Cria o evento de mostrar uma mensagem para o novo usuário

###| Cria a janela principal |###
main_window.title("Manga Checker")
main_window["bg"] = bg_colour
main_window.geometry("800x400+540+280")
main_window.mainloop()

