from urllib.request import Request, urlopen
import win32api

def cap_number_search(link):

    ###| Faz o download do HTML da pagina em questão |###
    req = Request(link, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        webpage = urlopen(req).read()
    except:
        return -1, "Link errado ou site fora do ar!"

    ###| Checa se encontrou o número do capitulo |###
    result_number = webpage.find(b'container-box default color-brown')
    if result_number == -1:
        return -2, "Não achei o número de capitulos"

    ###| Checa se encontrou o nome do capitulo |###
    result_title = webpage.find(b'<title>')
    if result_title == -1:
        return -3, "Não achei o titulo da obra"

    is_a_number = True      #| Indica se o caractere encontrado é um número
    number_address = 141    #| Número de caracteres depois do result onde se encontra o número de capitulos
    number_list = []        #| Lista dos algarismos do número de capitulos
    number_string = ""      #| String que vai receber o número de capitulos

    while is_a_number:
        is_a_number = False
        char = chr(webpage[result_number + number_address + 1])
        ###| Checa ver se o caractere encontrado é um algarismo |###
        for i in range(10):
            if char == str(i):
                number_list.append(char)
                is_a_number = True
                number_address += 1


    index = 0               #| Indice dos caracteres do titulo
    title_address = 7       #| Número de caracteres depois do result onde se encontra o titulo
    title_list = []         #| Lista dos caracteres do titulo
    title_string = ""       #| String que vai receber o titulo

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

if __name__ == "__main__":
    try:
        with open('links.txt', 'r') as readed:
            links_list = list(readed)
    except:
        file = open('links.txt',"w+")
        file.write("http://exemplo1.com\nhttp://exemplo2.com")
        file.close()
        win32api.MessageBox(0, 'Nós criamos um arquivo chamado links.txt para você!\
        \nPor favor, insira os links dos mangas que você quer checar no arquivo links.txt', 'Links não encontrados')
        exit()

    try:
        with open('cap_backup.txt', 'r') as readed:
            last_list = list(readed)
    except:
        file = open('cap_backup.txt',"w+")
        for i in range(len(links_list)):
            if i == len(links_list) - 1:
                file.write('0')
            else:
                file.write('0 \n')
        file.close()
        with open('cap_backup.txt', 'r') as readed:
            last_list = list(readed)

    index = 0
    message = ""
    file = open('cap_backup.txt',"w")
    file.truncate(0)
    
    for i in links_list:
        num_caps, series_name = cap_number_search(i)

        if int(last_list[index]) != int(num_caps) and int(num_caps) > 0:
            series_name = series_name + ' tem novos capitulos!\n'
            message = message + series_name
            file.write(num_caps)
            if index < len(links_list) - 1:
                file.write('\n')
        else:
            file.write(last_list[index])
        if int(num_caps) < 0:
            series_name = '\n\rO link: ' + i + 'não pode ser checado!\nMotivo: ' + series_name + '\n\n'
            message = message + series_name
        index += 1

    file.close()

    if message != "":
        win32api.MessageBox(0, message, 'Novas atualizações!')
    else:
        win32api.MessageBox(0,  'Não há novas atualizações ainda...', 'Sem novas atualizações')
