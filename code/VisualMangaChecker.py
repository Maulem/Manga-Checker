###| Visual Manga Checker |###
###| Developed by Maulem  |###
###|      22/10/2021      |###

###| IMPORTS |###

import tkinter as tk
from functools import partial
import win32api
import json
import pyautogui
import cv2
import numpy as np
import subprocess
import os
import time
import pyperclip

###| VARIÁVEIS GLOBAIS |###

x_centro = 1
y_centro = 1
x_region = 0
y_region = 0
width_region = 0
height_region = 0
item_clicked  = ""
home_dir  = os.path.expanduser("~")
final_dir = home_dir + "/AppData/Roaming/Manga Checker"
data_file = final_dir + "/data.json"
settings_file = final_dir + "/settings.json"
new_user = False
double_click_preventer = False

###| FUNÇÕES |###

###| Mensagem de boas vindas assim que o mouse entra na tela |###
def new_user_message(event):
    global new_user
    if new_user:
        message =  "Olá, parece que é a sua primeira vez utilizando o programa!\n\n"
        message += "Por favor digite o link da pagina principal do Mangá (aquela que tem a lista de todos capitulos) "
        message += "que você quer checar e clique em 'Adicionar link' para coloca-lo na lista"
        message += "\n\nExemplo de link de uma pagina principal do Mangá: https://mangalivre.net/manga/boruto-naruto-next-generations/3637"
        message += "\n\nDepois disso, sempre que você quiser checar por novos capitulos é so clicar em 'Atualizar links', mas não mexa o mouse me quanto os links são atualizados."
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
            start_browser()
            num_caps, series_name = cap_number_search(link)
            os.system("TASKKILL /F /IM msedge.exe")
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
    start_browser()
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

    os.system("TASKKILL /F /IM msedge.exe")

    if message != "":
        win32api.MessageBox(0, message, "Novas atualizações!")
    else:
        win32api.MessageBox(0,  "Não há novas atualizações ainda...", "Sem novas atualizações")

###| Mostra como usar o programa para quem precisar de ajuda |###
def help_click(botao):
    message =  "Para adicionar um novo link na lista por favor digite o link da pagina principal do Mangá (aquela que tem a"
    message += " lista de todos capitulos) que você quer checar e clique em 'Adicionar link' para coloca-lo na lista"
    message += "\n\nExemplo de link de uma pagina principal do Mangá: https://mangalivre.net/manga/boruto-naruto-next-generations/3637"
    message += "\n\nDepois disso, sempre que você quiser checar por novos capitulos é so clicar em 'Atualizar links', mas não mexa o mouse me quanto os links são atualizados."
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

###| Checa se o número é negativo e se for torna positivo
def check_negative(num):
    if num < 0:
        num *= -1

###| Tira um screenshot e salva na pasta temp
def take_screenshot(x = 0, y = 0, width = 1980, height = 1080):
    Screenshot = pyautogui.screenshot(region = (x, y, width, height))
    file = "temp/temp_screenshot.png"
    Screenshot.save(file)

###| Calcula centros, desenha caixas e faz a homografia
def drawBoxes_doHomografy_calcCenter(kp1, kp2, img_pesquisa, img_screenshot, good):
    
    ###| Código nesta função é de autoria do Mirandão (github:mirwox) misturado com o meu código ###|
    out = img_screenshot.copy()
    
    src_pts = np.float32([ kp1[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
    dst_pts = np.float32([ kp2[m.trainIdx].pt for m in good ]).reshape(-1,1,2)


    # Tenta achar uma trasformacao composta de rotacao, translacao e escala que situe uma imagem na outra
    # Esta transformação é chamada de homografia 
    # Para saber mais veja 
    # https://docs.opencv.org/3.4/d9/dab/tutorial_homography.html
    M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)
    matchesMask = mask.ravel().tolist()

    ###| Transforma a imagem em cinza
    img_pesquisa_gray = cv2.cvtColor(img_pesquisa, cv2.COLOR_BGR2GRAY)

    h,w = img_pesquisa_gray.shape
    # Um retângulo com as dimensões da imagem original
    pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)

    # Transforma os pontos do retângulo para onde estao na imagem destino usando a homografia encontrada
    dst = cv2.perspectiveTransform(pts,M)

    ###| Declara as variaveis globais
    global x_centro
    global y_centro
    global x_region
    global y_region
    global width_region
    global height_region

    ###| Zera as variaveis globais
    x_region = 0
    y_region = 0
    width_region = 0
    height_region = 0
    x_centro = 0
    y_centro = 0

    ###| Calcula o centro da caixa
    for x in range(len(dst)):
        x_centro += dst[x][0][0]
        y_centro += dst[x][0][1]
    x_centro /= len(dst)
    y_centro /= len(dst)

    ###| Salva as variaveis globais
    x_region = int(dst[0][0][0])
    y_region = int(dst[0][0][1])
    
    ###| Impede que esses números sejam negativos
    check_negative(x_region)
    check_negative(y_region)

    ###| Essas variaveis serão usadas pra calcular a largura e altura
    x2 = int(dst[2][0][0])
    y2 = int(dst[2][0][1])

    ###| Impede que esses números sejam negativos
    check_negative(x2)
    check_negative(y2)

    ###| Salva as variaveis globais
    width_region = x2 - x_region
    height_region = y2 - y_region

    if 0:
        print("x:{0} y:{1} x2:{2} y2:{3} width:{4} height:{5} xcentro:{6} ycentro:{7}".format(x_region, y_region, x2, y2, width_region, height_region, x_centro, y_centro))

    ###| Transforma o centro em inteiros
    x_centro = int(x_centro)
    y_centro = int(y_centro)

    ###| Desenha um circulo no centro da imagem
    out = cv2.circle(out, (x_centro, y_centro), radius=2, color=(255, 255, 0), thickness=-1)

    # Desenha um contorno em vermelho ao redor de onde o objeto foi encontrado
    img2b = cv2.polylines(out,[np.int32(dst)],True,(255,255,0),5, cv2.LINE_AA)
    
    return img2b

###| Analiza o screenshot tirado
def check_screenshot(img_pesquisa, img_screenshot, print_type = "", precision = 10, extratime = 0):

    ##| Transforma as imagens em cinza e salva
    img_pesquisa_gray = cv2.cvtColor(img_pesquisa, cv2.COLOR_BGR2GRAY)
    img_screenshot_gray = cv2.cvtColor(img_screenshot, cv2.COLOR_BGR2GRAY)

    ##| Inicia um cronometro
    time_start = time.time()

    while(time.time() < time_start + extratime + 0.0001):
            
        ##| Inicia  o Brisk (vai comparar as imagens)
        brisk = cv2.BRISK_create()

        ##| Encontra os Keypoints das imagens entre si e cria os decriptors para fazer os matchs
        keypoints1, descriptors1 = brisk.detectAndCompute(img_pesquisa_gray, None)
        keypoints2, descriptors2 = brisk.detectAndCompute(img_screenshot_gray, None)

        ##| Inicia os matchs
        bf = cv2.BFMatcher(cv2.NORM_HAMMING)

        try:
            #| Achou match
            matches = bf.knnMatch(descriptors1,descriptors2,k=2)
        except:
            #| Caso de erro ele insere um match ruim
            matches = [[1,2]]

        ##| Inicia a lista de matchs bons vazia
        good = []

        ##| Decide que matchs são bons
        try:
            for m,n in matches:
                if m.distance < 0.7*n.distance:
                    good.append(m)             
        except:
            print("Erro de comparação de matchs!")

        if print_type == "linhas":
            if len(good) > precision:
                ##| Desenha os matchs caso tenha suficientes
                output = cv2.drawMatches(img1 = img_pesquisa,
                                        keypoints1 = keypoints1,
                                        img2 = img_screenshot,
                                        keypoints2 = keypoints2,
                                        matches1to2 = good,
                                        outImg = None,
                                        flags = cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
            else:
                ##| Não desenha os matchs pois não tem suficientes
                output = cv2.drawMatches(img1 = img_pesquisa,
                                        keypoints1 = keypoints1,
                                        img2 = img_screenshot,
                                        keypoints2 = keypoints2,
                                        matches1to2 = [],
                                        outImg = None,
                                        flags = cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
            ##| Mostra a imagem
            cv2.imshow("Linhas", output)

        ##| Encontra a homografia, calcula centro e etc
        if len(good) > precision:
            output = drawBoxes_doHomografy_calcCenter(keypoints1, keypoints2, img_pesquisa, img_screenshot, good)
        else:
            output = img_screenshot

        ##| Mostra a imagem
        if print_type == "quadrado":
            cv2.imshow("Quadrado", output)

        ##| Fecha a imagem pressionando q
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

###| Faz o download do HTML da pagina em questão e procura informações
def cap_number_search(link):

    ###| Move o cursor para a barra de pesquisa e digita um site
    pyautogui.moveTo(x_centro, y_centro, duration=0, tween=pyautogui.easeInOutQuad)
    pyautogui.click()
    pyautogui.write(link, interval=0)
    pyautogui.typewrite(["Enter"])

    pyautogui.sleep(1)

    ###| Acessa o html da pagina
    with pyautogui.hold("Ctrl"):
        pyautogui.press("u")

    ###| Baixa o HTML da página acessada
    with pyautogui.hold("Ctrl"):
        pyautogui.press("a")

    with pyautogui.hold("Ctrl"):
        pyautogui.press("c")

    webpage = pyperclip.paste()
    
    ###| Checa se o resultado foi vazio |###
    if webpage == "":
        return -1, "o link esta errado ou o site fora do ar!"

    ###| Checa se encontrou o número do capitulo |###
    result_number = webpage.find('container-box default color-brown')
    if result_number == -1:
        return -2, "não foi possivel achar o número de capitulos"


    ###| Checa se encontrou o nome do capitulo |###
    result_title = webpage.find('<title>')
    if result_title == -1:
        return -3, "não foi possivel achar o titulo da obra"

    is_a_number = True      #| Indica se o caractere encontrado é um número
    number_address = 144    #| Número de caracteres depois do result onde se encontra o número de capitulos
    number_list = []        #| Lista dos algarismos do número de capitulos
    number_string = ""      #| String que vai receber o número de capitulos
    

    ###| Vai checando os caracteres, se não for um algarismo ele para |###
    while is_a_number:
        is_a_number = False
        char = webpage[result_number + number_address + 1]
        
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
        char = webpage[result_title + title_address + index]
        
        if char == '<':
            break
        title_list.append(char)
        index += 1
    
    ###| Salva a lista de algarismos/caracteres em uma string |###
    number_string = number_string.join(number_list)
    title_string = title_string.join(title_list)
    
    ###| Remove o resto do titulo |###
    cut = title_string.find(" Mangá (pt-BR) - MangaLivre")
    if cut == -1:
        return -3, "Erro ao editar o titulo da obra"
    title_list.clear()
    for i in range(cut):
        title_list.append(title_string[i])
    title_string = ""
    title_string = title_string.join(title_list)


    return number_string, title_string

###| Inicia o navegador na web e prepara pra procurar por sites
def start_browser():

    ###| Declara as variaveis globais
    global x_centro
    global y_centro
    global x_region
    global y_region
    global width_region
    global height_region

    ###| "Zera" as variaveis globais
    x_centro = 1
    y_centro = 1
    x_region = 0
    y_region = 0
    width_region = 0
    height_region = 0

    ###| Abre o Edge
    subprocess.Popen(['C:\Program Files (x86)\Microsoft\Edge\Application\\msedge.exe'])

    pyautogui.sleep(2)

    ###| Pega o endereço
    path = os.getcwd()
    path = path + "\\temp"

    ###| Cria um diretorio se precisar
    try:
        os.mkdir(path)
    except OSError:
        print ("Creation of the directory %s failed" % path)
    else:
        print ("Successfully created the directory %s " % path)

    ###| Carrega a imagem da barra de pesquisa
    img_pesquisa = cv2.imread('barra_pesquisa.png')

    ###| Procura no screenshot a barra de pesquisa
    while (x_centro <= 1 and y_centro <= 1):
        take_screenshot()
        img_screenshot = cv2.imread("temp\\temp_screenshot.png")
        pyautogui.sleep(0.1)
        check_screenshot(img_pesquisa, img_screenshot)
        if x_centro <= 1 and y_centro <= 1:
            ("Esperando o Edge abrir!")

    ###| Tira screenshot da barra de pesquisa
    take_screenshot(x_region, y_region, width_region, height_region)
    pyautogui.sleep(0.1)

    ###| Salva um backup das posições anteriores
    x_region_backup = x_region
    y_region_backup = y_region
    x_centro_backup = x_centro
    y_centro_backup = y_centro

    ###| Carrega a imagem da barra de pesquisa e do screenshot
    img_pesquisa = cv2.imread('barra_fullscreen.png')
    img_screenshot = cv2.imread("temp\\temp_screenshot.png")

    mult_pesquisa = 3
    pesquisa_resized = cv2.resize(img_pesquisa, (mult_pesquisa*img_pesquisa.shape[1], mult_pesquisa*img_pesquisa.shape[0]), interpolation = cv2.INTER_AREA)
    mult_screenshot = 3
    screenshot_resized = cv2.resize(img_screenshot, (mult_screenshot*img_screenshot.shape[1], mult_screenshot*img_screenshot.shape[0]), interpolation = cv2.INTER_AREA)

    ###| Procura no screenshot o botão de tela cheia

    pyautogui.sleep(0.1)
    
    check_screenshot(pesquisa_resized, screenshot_resized, "dont print", 2)
    
    ###| Checa se o Edge está ou não em tela cheia
    if x_region_backup != x_region or y_region_backup != y_region:
        x_centro /= mult_pesquisa
        y_centro /= mult_pesquisa
        x_centro += x_region_backup
        y_centro += y_region_backup
        pyautogui.moveTo(x_centro, y_centro, duration=0, tween=pyautogui.easeInOutQuad)
        print("Aumentando tela minimizada")
        pyautogui.click()

        x_centro = 1
        y_centro = 1

        pyautogui.sleep(1)

        ###| Carrega a imagem da barra de pesquisa
        img_pesquisa = cv2.imread('barra_pesquisa.png')

        ###| Procura no screenshot a barra de pesquisa
        while (x_centro <= 1 and y_centro <= 1):
            take_screenshot()
            pyautogui.sleep(0.1)
            img_screenshot = cv2.imread("temp\\temp_screenshot.png")
            
            check_screenshot(img_pesquisa, img_screenshot)


###| CÓDIGO PRINCIPAL |###


###| Checa se o arquivo settings.json existe |###
try:
    with open(settings_file, "r") as readed:
        settings = json.load(readed)
except:
    ##| Se não existe cria ele e coloca as configurações padrão |##
    default_settings = {
    "colour_theme"                  : "light",
    "version"                       : "beta - 0.2"
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
    "https://mangalivre.net/manga/one-punch-man/1036"                  : ["One Punch Man"                   , 221],
    "https://mangalivre.net/manga/one-piece/13"                        : ["One Piece"                       , 999],
    "https://mangalivre.net/manga/hunter-x-hunter/59"                  : ["Hunter x Hunter"                 , 390],
    "https://mangalivre.net/manga/seirei-gensouki/7436"                : ["Seirei Gensouki"                 , 24 ],
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

cv2.destroyAllWindows()









