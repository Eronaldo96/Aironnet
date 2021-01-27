from urllib.parse import quote_plus
import pyodbc
from sqlalchemy import create_engine
from cpf_cnpj-example import isCpfValid,isCnpjValid
import pandas as pd
import re
from caracteres-example import caixa_Alta, campo_Vazio, campo_Email, campo_Email_Dominio, campo_Nulo
from config-example import parametros

url_db = quote_plus(parametros)

db = create_engine("mssql+pyodbc:///?odbc_connect=%s" % url_db)

conexao = db.connect()

resultado_totalRegistros = conexao.execute("select count(*) from Parceiro")

for row in resultado_totalRegistros:
    print("Total de Registros => ",str(row[0]))

print("\n\n")

resultado = conexao.execute("select CgcCpf from Parceiro p where TipoParceiro = 'F' and CgcCpf is not NULL")

#contadores para checar a quantidades de dados válidos
count_cnpjT = 0
count_cnpjF = 0
count_cpfT = 0
count_cpfF = 0

#arquivo = open('Registros CPF e CNPJ do SIACNet.txt','a')

#arquivo.write("DADOS CPF")
#arquivo.write("\n")

for row in resultado:

#    verifica quantos CPFs são válidos
    if isCpfValid(str(row[0])) == True:
        count_cpfT+=1
    else:
        count_cpfF+=1

#    arquivo.write(str(row[0]))
#    arquivo.write(" => ")
#    arquivo.write(str(isCpfValid(str(row[0]))))
#    arquivo.write("\n")

resultado_totalRegistros = conexao.execute("select count(*) from Parceiro")

for row in resultado_totalRegistros:
    calculo_Cpf_True = int(count_cpfT)/row[0]*100
    calculo_Cpf_False = int(count_cpfF)/row[0]*100

print("quantidade de CPFs válidos => ",count_cpfT)
print("Porcentagem dos CPFs válidos => ",round(calculo_Cpf_True,3),"%")
print("\n")
print("quantidade de CPFs inválidos => ",count_cpfF)
print("Porcentagem dos CPFs inválidos => ",round(calculo_Cpf_False,3),"%")

print("\n\n")

resultado_2 = conexao.execute("select CgcCpf from Parceiro p where TipoParceiro = 'J' and CgcCpf is not NULL")

#arquivo.write("DADOS CNPJ")
#arquivo.write("\n")

for row in resultado_2:
#    verifica quantos cnpjs são válidos
    if isCnpjValid(str(row[0])) == True:
        count_cnpjT+=1
    else:
        count_cnpjF+=1

#    arquivo.write(str(row[0]))
#    arquivo.write(" => ")
#    arquivo.write(str(isCnpjValid(str(row[0]))))
#    arquivo.write("\n")

resultado_totalRegistros = conexao.execute("select count(*) from Parceiro")
for row in resultado_totalRegistros:
    calculo_Cnpj_True = int(count_cnpjT)/row[0]*100
    calculo_Cnpj_False = int(count_cnpjF)/row[0]*100

print("quantidade de CNPJs válidos => ",count_cnpjT)
print("Porcentagem dos CNPJS válidos => ",round(calculo_Cnpj_True,3),"%")
print("\n")
print("quantidade de CNPJs inválidos => ",count_cnpjF)
print("Porcentagem dos CNPJS inválidos => ",round(calculo_Cnpj_False,3),"%")

print("\n\n")

resultado_CnpjsNull = conexao.execute("select count(codParceiro) from Parceiro p where TipoParceiro = 'J' and CgcCpf is NULL")
for row in resultado_CnpjsNull:
    x = int(str(row[0]))
    print("Total de CNPJs Nulos => ",str(row[0]))
    resultado_totalRegistros = conexao.execute("select count(*) from Parceiro")
    for row in resultado_totalRegistros:
        calculo = x/row[0]*100
        print("Porcentagem dos CNPJs Nulos => ",round(calculo,3),"%")


print("\n")

resultado_CPFsNull = conexao.execute("select count(codParceiro) from Parceiro p where TipoParceiro = 'F' and CgcCpf is NULL")
for row in resultado_CPFsNull:
    x = int(str(row[0]))
    print("Total de CPFs Nulos => ",str(row[0]))
    resultado_totalRegistros = conexao.execute("select count(*) from Parceiro")
    for row in resultado_totalRegistros:
        calculo = x/row[0]*100
        print("Porcentagem dos CPFs Nulos => ",round(calculo,3),"%")

print("\n")


resultado_NomeAbrevFantasia = conexao.execute("select NomeAbrevFantasia from Parceiro")

result = resultado_NomeAbrevFantasia.fetchall()
count_Vazio = 0
count_naoVazio = 0
count_None = 0
for row in result:
   if campo_Vazio(row[0]) == True:
        count_Vazio+=1
   elif(str(row[0])=="None"): #NOVO -> CHECA OS NULOS
        count_None+=1
   else:
        count_naoVazio+=1
#    else:
#        count_naoVazio+=1
#        print(str(row[0]))

resultado_totalRegistros = conexao.execute("select count(*) from Parceiro")
for row in resultado_totalRegistros:
    calculo_caracteres_vazios = int(count_Vazio)/row[0]*100
#    calculo_caracteres_naoVazios = int(count_naoVazio)/row[0]*100

print("Quantidade de campos do NomeAbrevFantasia vazios = ",count_Vazio)
print("Porcentagem de campos do NomeAbrevFantasia vazios = ",round(calculo_caracteres_vazios,3),"%")
print("\n")
print("Quantidade de campos Nulos = ",count_None)
print("\n")
#print("Quantidade de campos do NomeAbrevFantasia nao vazios = ",count_naoVazio)
#print("Porcentagem de campos do NomeAbrevFantasia nao vazios = ",round(calculo_caracteres_naoVazios,3),"%")



#arquivo = open('Registros maiusculos e minusculos do SIACNET Parte-6.txt','a')

resultado_NomeAbrevFantasia = conexao.execute("select NomeAbrevFantasia from Parceiro")
count_Mai = 0
#count_Min = 0
for row in resultado_NomeAbrevFantasia:
    a = str(row[0])
    if caixa_Alta(str(a.replace("None",""))) == True:
        count_Mai+=1
        #arquivo.write(str(a))
        #arquivo.write(" => ")
        #arquivo.write(str(caixa_Alta(a)))
        #arquivo.write("\n")
#    elif campo_Vazio(a.replace("None","")) == False:
#    if caixa_Alta(str(a.replace("None",""))) == False:
#        count_Min+=1
        #arquivo.write(str(a))
        #arquivo.write(" => ")
        #arquivo.write(str(caixa_Alta(a)))
        #arquivo.write("\n")
#       print(str(row[0]))

resultado_totalRegistros = conexao.execute("select count(*) from Parceiro")
for row in resultado_totalRegistros:
    calculo_caracteres_Mai = int(count_Mai)/row[0]*100
#    calculo_caracteres_Min = int(count_Min)/row[0]*100

print("Quantidade de strings maiusculas do NomeAbrevFantasia = ",count_Mai)
print("Porcentagem de strings maiusculas do NomeAbrevFantasia = ",round(calculo_caracteres_Mai,3),"%")
print("\n")
#print("Quantidade de strings minusculas do NomeAbrevFantasia = ",count_Min)
#print("Porcentagem de strings minusculas do NomeAbrevFantasia = ",round(calculo_caracteres_Min,3),"%")


#teste = conexao.execute("select cgccpf from Parceiro p where TipoParceiro = 'F'")
#count_1 = 0
#count_2 = 0
#for row in teste:
#    if campo_Vazio(str(row[0])) == True:
#        count_1+=1
#    elif campo_Vazio(str(row[0]).replace("None","")) == False:
#    else:
#        count_2+=1
        #print(str(row[0]))
#resultado_totalRegistros = conexao.execute("select count(*) from Parceiro")
#for row in resultado_totalRegistros:
#    calculo_1 = int(count_1)/row[0]*100
#    calculo_2 = int(count_2)/row[0]*100

#print("Quantidade de cpfs vazios = ",count_1)
#print("Porcentagem de cpfs vazios= ",round(calculo_1,3),"%")
#print("\n")
#print("Quantidade de cpfs nao vazios = ",count_2)
#print("Porcentagem de cpfs nao vazios= ",round(calculo_2,3),"%")
#print("\n")

#-----------------------------------------------------------------------------

#1º PARTE PARA ANALISAR EMAILS
#OBS: TESTAR
regex = "[^@]+@[^@]+\.[^@]+"#REGEX EMAIL
rgx = '[^@]+@(?:ce+\.)+[sebrae+\.]+[com+\.]+[br]{2,}$'#REGEX DOMINIO
rgx2 = '[^@]+@(?:CE+\.)+[SEBRAE+\.]+[COM+\.]+[BR]{2,}$'#REGEX DOMINIO

resultado_email = conexao.execute("select email from FCFO f ")
result2 = resultado_email.fetchall()

count_email_Validos = 0
count_email_Invalidos = 0

count_dominio1 = 0
count_dominio2 = 0
count_sem_dominio = 0
contador1 = 0
contador2 = 0


#arquivo1 = open('Emails validos.txt','a')
#arquivo2 = open('Emails invalidos.txt','a')
#arquivo3 = open('Email com dominio sebrae.txt','a')
#arquivo4 = open('Emails sem dominio sebrae.txt','a')

for row in result2:
    if(re.search(rgx,str(row[0]))):
        #arquivo3.write(str(row))
        #arquivo3.write("\n")
        #print("Valid Email")
        count_dominio1+=1
    elif(re.search(rgx2,str(row[0]).replace("None",""))):
        #arquivo3.write(str(row))
        #arquivo3.write("\n")
        #print("Valid Email")
        count_dominio2+=1
    elif str(row[0]) == "None":
            contador2+=1
    else:
        #arquivo4.write(str(row))
        #arquivo4.write("\n")
        #print("Invalid Email")
        count_sem_dominio+=1


    if(re.search(regex,str(row[0]).replace("Null",""))):
        #arquivo1.write(str(row))
        #arquivo1.write("\n")
        #print("Valid Email")
        count_email_Validos+=1
    elif str(row[0]) == "None":
        contador1+=1
    else:
        #arquivo2.write(str(row))
        #arquivo2.write("\n")
        #print("Invalid Email")
        count_email_Invalidos+=1

resultEmailDominio = count_dominio1 + count_dominio2

print("Registros Nulos de emails =>",contador1)
print("Registros Nulos de emails com e sem dominio =>",contador2)
print("\n")
print("Emails validos => ",count_email_Validos)
print("Emails invalidos => ",count_email_Invalidos)
print("\n")
print("Emails com dominio sebrae => ",resultEmailDominio)
print("Emails sem dominio sebrae => ",count_sem_dominio)

#arquivo1.close()
#arquivo2.close()
#arquivo3.close()
#arquivo4.close()

#--------------------------------------------------------------------------------

#2º PARTE PARA ANALISAR EMAILS
#OBS: TESTAR, BANCO FCFO

resultado_email = conexao.execute("select email from FCFO f ")
result2 = resultado_email.fetchall()

count_email_Validos = 0
count_email_Invalidos = 0
count_email_Validos_Dominio = 0
count_email_Invalidos_Dominio = 0
contador1 = 0
contador2 = 0


#arquivo1 = open('Emails validos2.txt','a')
#arquivo2 = open('Emails invalidos2.txt','a')
#arquivo3 = open('Emails validos dominio2.txt','a')
#arquivo4 = open('Emails invalidos dominio2.txt','a')

for row in result2:

    if (validate_email(str(row)) == True):
#        arquivo1.write(str(row))
#        arquivo1.write("\n")
#        #print("Valid Email")
        count_email_Validos+=1
    elif str(row[0]) == "None":
        contador1+=1
    else:
#        arquivo2.write(str(row))
#        arquivo2.write("\n")
        #print("Invalid Email")
        count_email_Invalidos+=1

    if (campo_Email_Dominio(str(row)) == True):
#        arquivo3.write(str(row))
#        arquivo3.write("\n")
        #print("Valid Email")
        count_email_Validos_Dominio+=1
    elif str(row[0]) == "None":
        contador2+=1
    else:
#        arquivo4.write(str(row))
#        arquivo4.write("\n")
        #print("Invalid Email")
        count_email_Invalidos_Dominio+=1

print("Registros Nulos de emails =>",contador1)
print("Registros Nulos de emails dominio =>",contador1)
print("\n")
print("Emails validos => ",count_email_Validos)
print("Emails invalidos => ",count_email_Invalidos)
print("\n")
print("Emails dominio validos => ",count_email_Validos_Dominio)
print("Emails dominio invalidos => ",count_email_Invalidos_Dominio)


#arquivo1.close()
#arquivo2.close()
#arquivo3.close()
#arquivo4.close()

#------------------------------------------------------------------------------
#CHECAGEM DE CAMPOS NULOS, AINDA EM TESTE
#OBS TESTAR, O SELECT É REFERENTE AO BANCO FCFO
resultado_Fantasia = conexao.execute("select NomeFantasia from FCFO f ")
result = resultado_Fantasia.fetchall()

count_Nulos = 0
count_naoNulos = 0
for row in result:
    if campo_Nulo(row[0]) == True:
        count_Nulos+=1
        #arquivo.write(str(row))
        #arquivo.write("\n")
    else:
        count_naoNulos+=1
        #arquivo.write(str(row))
        #arquivo.write("\n")
#       print(str(row[0]))

print("Quantidade de campos do NomeFantasia nulos = ",count_Nulos)
#print("Porcentagem de campos do NomeFantasia nulos = ",round(calculo_caracteres_vazio,3),"%")
#print("\n")
#exit(0)
print("Quantidade de campos do NomeFantasia nao nulos = ",count_naoNulos)
#print("Porcentagem de campos do NomeAbrevFantasia nao nulos = ",round(calculo_caracteres_naoVazios,3),"%")
