from sqlalchemy import create_engine
def conn():
    return create_engine('mysql+mysqlconnector://psel_varos:psel_varos@localhost/psel_varos', echo=True)