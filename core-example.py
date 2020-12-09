from urllib.parse import quote_plus

import pyodbc
from sqlalchemy import create_engine

parametros = (
    # Driver que será utilizado na conexão
    'DRIVER={ODBC Driver 17 for SQL Server};'
    # IP ou nome do servidor.
    'SERVER=ip;'
    # Porta
    'PORT=1433;'
    # Banco que será utilizado.
    'DATABASE=banco;'
    # Nome de usuário.
    'UID=user;'
    # Senha/Token.
    'PWD=password')

url_db = quote_plus(parametros)

db = create_engine("mssql+pyodbc:///?odbc_connect=%s" % url_db)

conexao = db.connect()

def isCpfValid(cpf):
    """ If cpf in the Brazilian format is valid, it returns True, otherwise, it returns False. """

    # Check if type is str
    if not isinstance(cpf,str):
        return False

    # Remove some unwanted characters
    cpf = re.sub("[^0-9]",'',cpf)

    # Verify if CPF number is equal
    if cpf=='00000000000' or cpf=='11111111111' or cpf=='22222222222' or cpf=='33333333333' or cpf=='44444444444' or cpf=='55555555555' or cpf=='66666666666' or cpf=='77777777777' or cpf=='88888888888' or cpf=='99999999999':
        return False

    # Checks if string has 11 characters
    if len(cpf) != 11:
        return False

    sum = 0
    weight = 10

    """ Calculating the first cpf check digit. """
    for n in range(9):
        sum = sum + int(cpf[n]) * weight

        # Decrement weight
        weight = weight - 1

    verifyingDigit = 11 -  sum % 11

    if verifyingDigit > 9 :
        firstVerifyingDigit = 0
    else:
        firstVerifyingDigit = verifyingDigit

    """ Calculating the second check digit of cpf. """
    sum = 0
    weight = 11
    for n in range(10):
        sum = sum + int(cpf[n]) * weight

        # Decrement weight
        weight = weight - 1

    verifyingDigit = 11 -  sum % 11

    if verifyingDigit > 9 :
        secondVerifyingDigit = 0
    else:
        secondVerifyingDigit = verifyingDigit

    if cpf[-2:] == "%s%s" % (firstVerifyingDigit,secondVerifyingDigit):
        return True
    return False


def isCnpjValid(cnpj):
    """ If cnpf in the Brazilian format is valid, it returns True, otherwise, it returns False. """

    # Check if type is str
    if not isinstance(cnpj,str):
        return False

    # Remove some unwanted characters
    cpf = re.sub("[^0-9]",'',cnpj)

    # Checks if string has 11 characters
    if len(cpf) != 14:
        return False

    sum = 0
    weight = [5,4,3,2,9,8,7,6,5,4,3,2]

    """ Calculating the first cpf check digit. """
    for n in range(12):
        value =  int(cpf[n]) * weight[n]
        sum = sum + value


    verifyingDigit = sum % 11

    if verifyingDigit < 2 :
        firstVerifyingDigit = 0
    else:
        firstVerifyingDigit = 11 - verifyingDigit

    """ Calculating the second check digit of cpf. """
    sum = 0
    weight = [6,5,4,3,2,9,8,7,6,5,4,3,2]
    for n in range(13):
        sum = sum + int(cpf[n]) * weight[n]

    verifyingDigit = sum % 11

    if verifyingDigit < 2 :
        secondVerifyingDigit = 0
    else:
        secondVerifyingDigit = 11 - verifyingDigit

    if cpf[-2:] == "%s%s" % (firstVerifyingDigit,secondVerifyingDigit):
        return True
    return False

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
