#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Plotar o gráfico com o filtro
# importing the required module 
import matplotlib.pyplot as plt
import os


# In[2]:



class Sinal():
    def __init__(self, nome_arquivo_entrada="", caminho="", reverse=False):
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
    def filtra_sinal(self):
        pass




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
    
    #1) leitura dos valores do sinal de entrada
    entrada = Sinal("dolar.txt", reverse=True)
    quant_sinais, vetor_entrada_sinais = entrada.quant_lista_arquivo()

    #print(vetor_entrada_sinais)

    #2) Gerar o filtro da media 5: m_5
    # filtro = GeraFiltroSinal(vetor_entrada_sinais)
    # filtro_media_5 = filtro.cria_filtro_media(5)
    filtro = Sinal()
    filtro_media_5 = filtro.gera_filtro_media(5)
    print("Filtro Media 5 gerado:", filtro_media_5)

    #3) Gerar o filtro de media 11: m_11
    filtro_media_11 = filtro.gera_filtro_media(11)
    print("Filtro Media 11 gerado:", filtro_media_11)


    # #3) Critério de parada: y = M + N - 1
    # y = FiltraSinal(vetor_entrada_sinais, filtro_media_5, "media")
    # dimensao_y = y.criterio_parada()
    # print("Dimensao da saida:", dimensao_y)


    # Gera Filtro Gaussiano de tamanho 5
    filtro_gaussiano_5 = filtro.gera_filtro_gaussiano(5)
    print("Filtro Gaussiano 5 gerado:", filtro_gaussiano_5)

    # Gera Filtro Gaussiano de tamanho 11
    filtro_gaussiano_11 = filtro.gera_filtro_gaussiano(11)
    print("Filtro Gaussiano 11 gerado:", filtro_gaussiano_11)













main()



