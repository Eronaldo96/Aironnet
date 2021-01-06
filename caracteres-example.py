import re

def caixa_Alta(a):

    if not isinstance(a,str):
        return False

    #a = re.sub("[a-z]",'',a)


    if a.lower() != a:
        return True

    return False

def campo_Vazio(a):

    if len(str(a)) > 0:
        return True
    else:
        return False

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
