import re

def caixa_Alta(a):

    if not isinstance(a,str):
        return False

    #a = re.sub("[a-z]",'',a)


    if a.lower() != a:
        return True

    return False

#------------------------------------------------------------------------------
#TESTAR A FUNÇÃO VAZIO
def campo_Vazio(a):
    #correção para checar registros vazios, ainda em teste
    if not len(a):
        return True
    #if len(str(a)) > 0:
    #    return True
    #else:
    #    return False

    return False

#def simbolos(a):
#    if not isinstance(a,str):
#        return False
#    x = "123456789.,;:!#@$%*(){}[]|/*+-_"
#    if a == x:
#        return true

def campo_Nulo(a):

    if pd.isnull(a):
        return True

    return False

#-----------------------------------------------------------------------------

#funções para checar emails ainda em teste!
def campo_Email(a):

    if re.match("[^@]+@[^@]+\.[^@]+", a):
        return True
    else:
        return False

    return False

def campo_Email_Dominio(a):

    if re.match(r'[^@]+@(?:ce)+\.+[sebrae]+\.+[com]+\.+[br]{2,3}', a):
        return True
    elif re.match(r"[^@]+@(?:CE)+\.+[SEBRAE]+\.+[COM]+\.+[BR]{2,3}", a):
        return True
    else:
        return False

    return False
