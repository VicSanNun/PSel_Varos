from sqlalchemy.orm import sessionmaker
if __name__ == "__main__":
    from connector import conn
    from model import Company
else:
    from db.connector import conn
    from db.model import Company

engine = conn()

Session = sessionmaker(bind=engine)
session = Session()

PETR = Company(company_id = 1, company_name='Petrobrás', cod_search="petr4", ticker="PETR4.SA")
WEG = Company(company_id = 2, company_name='WEG', cod_search="weg", ticker="WEGE3.SA")
CEA = Company(company_id = 3, company_name='C&A', cod_search="c%26a", ticker="CEAB3.SA")

session.add(PETR)
session.add(WEG)
session.add(CEA)

session.commit()

session.close()
