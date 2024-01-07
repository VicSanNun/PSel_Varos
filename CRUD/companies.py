from db.connector import conn
from sqlalchemy.orm import sessionmaker
from db.model import Company

class Companies_CRUD:
    def __init__(self, conn) -> None:
        try:
            self.conn = conn
            self.Session = sessionmaker(bind=self.conn)
            self.session = self.Session()
        except Exception as e:
            print('A Classe não foi inicializada corretamente: ', e)
    
    def get_company_data(self, company_id):
        stock = self.session.query(Company).filter(Company.company_id == company_id).all()
        return stock
    
        