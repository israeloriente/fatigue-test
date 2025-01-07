from tkinter import *
import serial
import socket
import time
import math

global temp1
global temp2
global temp3

y = 0

def create_port():
    global portaUSB
    aux = temp.get()
    portaUSB = serial.Serial(aux, 9600)

def sen_command(cod):
    aux = str(cod)
    portaUSB.write(aux.encode("utf-8"))
    print('enviando dado')

def comando (op):
    global w

    if (op == 1):
        sen_command(temp2)
        print('Iniciando ensaio')
        sigmalinha = float(temp2.get())
        sut = float(temp1.get())
        selinha = sut*0.5
        ka = 4.51*sut**-0.265
        kb = 1.24*11.95**-0.107

        print(selinha)
        print(ka)
        print(kb)


        se = selinha*ka*kb

        sk=(sut)*0.14503773773
        raiza=0.246-(3.08e-3)*sk+(1.51e-5)*sk**2-(2.67e-8)*sk**3
        kt=1.2
        kf = 1.55

        sigma = kf*sigmalinha
        sigma2 = sigma
        print(se)


        f = -(2e-10)*sut**3+(6e-07)*sut**2-0.0008*sut+1.168
        print(sigma)

        print(f)

        a = (f*sut)**2/se

        print(a)

        b = -(1/3)*math.log10((f*sut)/se)

        print(b)

        n = (sigma2/a)**(1/b)

        print (n)
        w = n
        w2 = (str((f'{w:.2e}')) + ' ciclos')
        vida_teorica2 = Label(text=w2,fg = 'black', font='calibrilight 14 bold').place(x=900,y=300)
        z = n/1800
        z2 = (str(int(z)) + ' minutos')
        tempo_est2 = Label(text=z2,fg = 'black', font='calibrilight 14 bold').place(x=900,y=330)

        print(z)


    if (op == 2):
        x=portaUSB.readline().decode('utf-8')
        b = int(x)
        b2 = (str(b) + ' ciclos')
        vida2 = Label(text=b2,fg = 'black', font='calibrilight 14 bold').place(x=900,y=360)
        er = format((abs((w-b)/w)*100),'.2f')
        er2 = (str(er) + ' %')
        erro2 = Label(text=er2,fg = 'black', font='calibrilight 14 bold').place(x=900,y=390)


janela = Tk()

janela.title('ENSAIO DE FADIGA')
janela.geometry('1360x690')
#janela.configure(bg = 'white')

text_Port = Label(text = 'Porta serial:').place(x=50,y=200)
temp = StringVar()
porta = Entry(janela,textvariable = temp).place(x=120,y=200)
botao_port = Button(text='OK', command = create_port).place(x=260,y=195)

title1 = Label(text='ENSAIO DE FADIGA',fg ='black', font='calibrilight 40 bold')
title1.place(x=390,y=20)
title2 = Label(text='POR FLEXÃO ROTATIVA',fg ='black', font='calibrilight 40 bold')
title2.place(x=340,y=100)

# logo1 = PhotoImage(file='ufpb100.png')
# logo1_1 = Label(janela,image=logo1)
# logo1_1.place(x=30,y=30)

# logo2 = PhotoImage(file='gpii.png')
# logo2_2 = Label(janela,image=logo2)
# logo2_2.place(x=1100,y=30)

# logo3 = PhotoImage(file='qr1.png')
# logo3_3 = Label(janela,image=logo3)
# logo3_3.place(x=1200,y=500)

#entrada de dados
title3 = Label(text='DADOS DE ENTRADA',fg ='black', font='calibrilight 20 bold')
title3.place(x=150,y=250)

sut1 = Label(text='Sut do corpo de prova (MPa)',fg = 'black', font='calibrilight 14 bold')
sut1.place(x=50,y=300)
temp1 = StringVar()
porta1 = Entry(janela, textvariable = temp1).place(x=330,y=300)
botao_port1 = Button(text='ok').place(x=500,y=300)

carga = Label(text='Carga aplicada (MPa)',fg = 'black', font='calibrilight 14 bold')
carga.place(x=50,y=350)
temp2 = StringVar()
porta2 = Entry(janela, textvariable = temp2).place(x=330,y=350)
botao_port2 = Button(text='ok').place(x=500,y=350)

botao_start = Button(text='Iniciar ensaio', command = lambda: comando (1)).place(x=500,y=380)
botao_stop = Button(text='Concluir ensaio', command = lambda: comando (2)).place(x=500,y=410)



#resultados


title4 = Label(text='RESULTADOS',fg ='black', font='calibrilight 20 bold')
title4.place(x=830,y=250)

vida_teorica = Label(text='Vida teórica:',fg = 'black', font='calibrilight 14 bold').place(x=700,y=300)
#vida_teorica2 = Label(text=y,fg = 'black', font='calibrilight 14 bold').place(x=900,y=300)

tempo_est = Label(text='Duração do ensaio:',fg = 'black', font='calibrilight 14 bold').place(x=700,y=330)
#tempo_est2 = Label(text='XXX minutos',fg = 'black', font='calibrilight 14 bold').place(x=900,y=330)


vida = Label(text='Vida:',fg = 'black', font='calibrilight 14 bold').place(x=700,y=360)
#vida2 = Label(text=y,fg = 'black', font='calibrilight 14 bold').place(x=900,y=360)

erro = Label(text='Erro:',fg = 'black', font='calibrilight 14 bold').place(x=700,y=390)
#erro2 = Label(text='XY %',fg = 'black', font='calibrilight 14 bold').place(x=900,y=390)

janela.mainloop()
