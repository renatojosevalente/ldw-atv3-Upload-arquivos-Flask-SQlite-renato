from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Veiculo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    modelo = db.Column(db.String(25))
    marca = db.Column(db.String(25))
    ano = db.Column(db.Integer)
    cor = db.Column(db.String(25))
    combustivel = db.Column(db.String(25))
    preco = db.Column(db.Float(25))
    estoque = db.Column(db.Integer)

    def __init__(self, modelo, marca, ano, cor, combustivel, preco, estoque):
        self.modelo = modelo
        self.marca = marca
        self.ano = ano
        self.cor = cor
        self.combustivel = combustivel
        self.preco = preco
        self.estoque = estoque

#Classe para imagens
class Imagem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(120), unique=True, nullable=False)

    def __init__(self, filename):
        self.filename = filename