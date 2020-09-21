#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Plotar o gráfico com o filtro
# importing the required module 
import matplotlib.pyplot as plt
import os
import pandas as pd


# In[2]:



class Sinal():
    def __init__(self,
                nome_arquivo_entrada="",
                caminho="", 
                reverse=False,
                grava_imagem=False):
        self.caminho = caminho
        self.nome_arquivo_entrada = nome_arquivo_entrada
        self.reverse = reverse
        self.lista_sinal = list()
    

    def quant_lista_arquivo(self):

        # Transformar em um try
        if self.caminho != "" and self.nome_arquivo_entrada != "":
            arquivo = os.path.join(self.caminho, self.nome_arquivo_entrada)
        else:
            arquivo = self.nome_arquivo_entrada
            
        with open(arquivo, "r") as f:
            num_lines = 0
            vetor_entrada_sinais = list()
            for i, l in enumerate(f):
                # se não é uma linha em branco, adiciona na lista de sinais e conta o registro
                if l.strip():
                    vetor_entrada_sinais.append(float(l.strip()))
                    num_lines += 1

        # Se o usuarío optar por inverter a série temporal dos dados
        if self.reverse:
            vetor_entrada_sinais.reverse()

        self.lista_sinal = vetor_entrada_sinais
        
        return(num_lines, vetor_entrada_sinais)

    def gera_filtro_media(self, valor_media):
        self.valor_media = valor_media
        filtro_h = list()
        for i in range(1, self.valor_media+1):
            filtro_h.append(1/self.valor_media)
        return filtro_h

    def gera_filtro_gaussiano(self, tamanho):
        self.tamanho = tamanho
        lista_filtro_gaussiano = list()
        linha = self.tamanho - 1
        soma_coef = 0

        # utilizado pra calcular cada valor co Triangulo de Pascal
        def coeficiente_binomial(linha, kaesimo):
            #linha! / (kesimo! * (linha - kesimo)!)
            def fatorial(numero):
                fatorial = 1
                while (numero > 0):
                    fatorial = fatorial * numero
                    numero -= 1
                    
                return fatorial

            n = fatorial(linha)
            k = fatorial(kaesimo)
            diferenca = linha - kaesimo
            diferenca = fatorial(diferenca)
            coef_binomial = n / (k * diferenca)
            return coef_binomial

        for i in range(linha+1):
            coef_binomial = coeficiente_binomial(linha,i)
            soma_coef = soma_coef + coef_binomial
            lista_filtro_gaussiano.append(coef_binomial)
        
        for n in range(len(lista_filtro_gaussiano)):
            lista_filtro_gaussiano[n] = lista_filtro_gaussiano[n] / soma_coef
        
        return lista_filtro_gaussiano

    # FIltra o sinal pelo cálculo da Convolução entre entrada e filtro
    def filtra_sinal(self, sinais_entrada, filtro_h):
        self.sinais_entrada = sinais_entrada
        self.filtro_h = filtro_h
        self.dimensao_x = len(sinais_entrada)
        self.dimensao_filtro_h = len(self.filtro_h)

        # dimensao de y => critério de parada
        self.dimensao_y_n = self.dimensao_x + self.dimensao_filtro_h - 1

        saida_y = list()
        #dim_x = len(sinais_entrada)
        for n in range(self.dimensao_y_n):
            saida_temp = 0
            #saida_y[n] = 0
            for k in range(self.dimensao_filtro_h):
                posicao_x = n - k
                
                if n - k < 0:
                    posicao_negativa = n - k
                    #espelhando o valor do negativo para o positivo
                    #o primeiro valor negativo é espelhado no primeiro valor positivo e assim por diante, ou seja,
                    #x[-1] = x[0], x[-2] = x[1]
                    posicao_x = posicao_negativa*(-1) - 1 
                    valor_posicao = self.sinais_entrada[posicao_x]
                    # print("Posição negativa:", posicao_negativa)
                    # print("Posicao espelhada:", posicao_x)
                    # print("Valor de x nessa posicao. x[{0}] = x[{1}] = {2}".format(posicao_negativa, posicao_x, valor_posicao))

                elif n - k >= self.dimensao_x:
                    #posicao_transborda ocorre quando x[n-k] é maior que as posicoes do sinal de entrada x
                    posicao_transborda = n - k
                    quant_sobra = posicao_transborda - self.dimensao_x
                    
                    # para espelhar a posicao_x, o primeira valor que transborda len(x) + 1 é igual a
                    # o ultimo valor possivel de x, x[len(x)], o segundo que transborda, len(x) + 2
                    # é igual a x[len[x] - 1] e assim por diante.
                    #print(quant_sobra)
                    posicao_x = self.dimensao_x - quant_sobra - 1
                    #print(posicao_x)
                    valor_posicao = self.sinais_entrada[posicao_x]
                    
                    # print("Posição que transbordou:", posicao_transborda)
                    # print("Posicao espelhada:", posicao_x)
                    # print("Valor de x nessa posicao. x[{0}] = x[{1}] = {2}".format(posicao_transborda, posicao_x, valor_posicao))
                else:
                    valor_posicao = self.sinais_entrada[n-k]
                    #print("Nao transbordou pra nenhum lado. n-k = {} Vapor_posicao é igual {}".format(n-k, valor_posicao))
                
                saida_temp = saida_temp + (self.filtro_h[k] * valor_posicao)
                #dicionario_y[n] = dicionario_y[n] + (filtro_h[k] * valor_posicao)
            saida_y.append(saida_temp)
        
        # Remove as bordas dos
        
        return saida_y

    def remove_sinais_sobra(self, tamanho_filtro, sinal_filtrado):
        self.sinal_filtrado = sinal_filtrado
        self.tamanho_filtro = tamanho_filtro
        
        # remove o mesmo tanto de sinais que adicionamos (se adicionamamos 11(tamanho_filtro) - 1(definicao)), entao
        # deletamos do sinal de saida 5 no começo e 5 no final de sua lista.
        quant_excluir = tamanho_filtro//2

        del(self.sinal_filtrado[:quant_excluir])
        del(self.sinal_filtrado[-quant_excluir:])

        return self.sinal_filtrado

    #Plotar gráfico com matplob
    def plotar_grafico(self, *args, **kwargs):
        # *args contem as listas com os sinais
        # **kwargs contem os nomes que queremos salvar os arquivos do grafico
        self.sinal = args
        self.nome_grafico = kwargs

        #print(self.nome_grafico.items())
        #print(self.sinal)
        caminho_graficos = 'graficos'
        #print(type(self.sinal))
        df = pd.DataFrame()
        data = dict()
        data = self.nome_grafico
        nomes = list()
        for key in data.keys():
            nomes.append(key)


        # data = {
        #     "Media5":self.sinal[0],
        #     "Media11":self.sinal[1],
        #     "SinalBruto":self.sinal[2]
        # }

        df = pd.DataFrame(data, columns=nomes)
        print(df)
        df.plot()
        plt.show()


        # plt.plot(self.sinal[0], self.sinal[1])
        # plt.savefig(caminho_graficos + '/teste.png')
        # plt.show()

            # if self.nome != None:
            #     if(os.path.exists(caminho_graficos)):
            #         plt.savefig(caminho_graficos + '/nome.png')



#Classe para geração dos filtros de Média ou Gaussiano
class GeraFiltroSinal():
    def __init__ (self, lista_sinais_entrada):
        self.lista_sinais_entrada = lista_sinais_entrada


    def cria_filtro_media(self, valor_media):
        self.valor_media = valor_media
        filtro_h = list()
        for i in range(1, self.valor_media+1):
            filtro_h.append(1/self.valor_media)
        return filtro_h

    def cria_filtro_gausiano(self, valor_gaussiano):
        pass
    

class FiltraSinal():
    def __init__(self, sinal_entrada, lista_filtro, tipo_filtro="media"):
        self.sinal_entrada = sinal_entrada
        self.lista_filtro = lista_filtro
        self.tipo_filtro = tipo_filtro

    def criterio_parada(self):
        quant_sinais_entrada = len(self.sinal_entrada)
        quant_sinais_saida = len(self.lista_filtro)
        return quant_sinais_entrada + quant_sinais_saida - 1

    def filtro_media(self):
        pass


def main():
    
    #1) Escolher um dos sinais disponiveis no arquivo de sinais
    arquivo_sinais = "dolar.txt"
    entrada = Sinal(arquivo_sinais, reverse=True)
    quant_sinais, vetor_entrada_sinais = entrada.quant_lista_arquivo()


    #2 Filtragem da Média

    #2-a) Gerar o filtro da media 5: m_5
    # filtro = GeraFiltroSinal(vetor_entrada_sinais)
    # filtro_media_5 = filtro.cria_filtro_media(5)
    filtro = Sinal()
    m_5 = filtro.gera_filtro_media(5)
    #print("Filtro Media 5 gerado:", m_5)


    #2-b) Gerar o filtro de media 11: m_11
    m_11 = filtro.gera_filtro_media(11)
    #print("Filtro Media 11 gerado:", m_11)
    
    #2-c) Obtenha y1[n] e y2[n].
    y1 = list()
    y2 = list()
    y1 = filtro.filtra_sinal(vetor_entrada_sinais, m_5)
    #print("*********************************", len(y1))

    #Remove sinais de sobra
    y1 = filtro.remove_sinais_sobra(len(m_5), y1)

    y2 = filtro.filtra_sinal(vetor_entrada_sinais,m_11)
    #print("*********************************", len(y2))
    #Remove sinais de sobra
    y2 = filtro.remove_sinais_sobra(len(m_11), y2)


    print("Amostra dos PRIMEIROS 20 valores da saida y (sinal filtrado pela media 5):", y1[:20])
    print("Amostra dos PRIMEIROS 20 valores da saida y (sinal filtrado pela media 11):", y1[:20])
    print("Amostra dos ÚLTIMOS 20 valores da saida y (sinal filtrado pela media 5):", y1[-20:])
    print("Amostra dos ÚLTIMOS 20 valores da saida y (sinal filtrado pela media 11):", y1[-20:])


    #2-d) Plotar o gráfico de um trecho de 100 amostras dos dois sinais filtrados
    #Plotar o gráfico sem filtro
    filtro.plotar_grafico(y1, y2, vetor_entrada_sinais,**{"nome_imagem_y1":y1, "nome_imagem_y2":y2, "nome_imagem_bruto":vetor_entrada_sinais})
    #filtro.plotar_grafico(y2)


    #3 - FILTRAGEM GAUSSIANA

    #3-a) Gera Filtro Gaussiano de tamanho 5
    g_5 = filtro.gera_filtro_gaussiano(5)
    #print("Filtro Gaussiano 5 gerado:", g_5)

    #3-b) Gera Filtro Gaussiano de tamanho 11
    g_11 = filtro.gera_filtro_gaussiano(11)
    #print("Filtro Gaussiano 11 gerado:", g_11)

    #3-c) Obtenha z1[n] = x[n]*g_5[n] e z2[n] = x[n]*g_11[n]
    z1 = filtro.filtra_sinal(vetor_entrada_sinais, g_5)
    z2 = filtro.filtra_sinal(vetor_entrada_sinais, g_11)

    #Remove sinais de sobra
    z1 = filtro.remove_sinais_sobra(len(g_5), z1)
    #Remove sinais de sobra
    z2 = filtro.remove_sinais_sobra(len(g_11), z2)

    #2-d) Plotar o gráfico de um trecho de 100 amostras dos dois sinais filtrados
    #Plotar o gráfico sem filtro
    filtro.plotar_grafico(z1, z2, vetor_entrada_sinais,**{"nome_imagem_z1":z1, "nome_imagem_z2":z2,
    "nome_imagem_bruto":vetor_entrada_sinais})
    #filtro.plotar_grafico(y2)

    #4 - ANALISE DOS RESULTADOS
    filtro.plotar_grafico(y1, z1, vetor_entrada_sinais,**{"nome_imagem_y1":y1, "nome_imagem_z1":z1, 
    "nome_imagem_bruto":vetor_entrada_sinais})

    filtro.plotar_grafico(y2, z2, vetor_entrada_sinais,**{"nome_imagem_y2":y1, "nome_imagem_z2":z1, 
    "nome_imagem_bruto":vetor_entrada_sinais})








main()





# %%
