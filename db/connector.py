from sqlalchemy import create_engine
def conn():
    #Não é recomendado subir suas credenciais no repositório. O ideal é ter um arquivo local (ou o ambiente configurado) 
    #com as credenciais.
    return create_engine('mysql+mysqlconnector://psel_varos:psel_varos@localhost/psel_varos', echo=True)
