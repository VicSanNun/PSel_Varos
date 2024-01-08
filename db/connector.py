from sqlalchemy import create_engine
def conn():
    #return create_engine('mysql+mysqlconnector://psel_varos:psel_varos@psel-varos.cjkicigso0nj.us-east-1.rds.amazonaws.com/psel_varos', echo=True)
    return create_engine('mysql+mysqlconnector://psel_varos:psel_varos@localhost/psel_varos', echo=True)