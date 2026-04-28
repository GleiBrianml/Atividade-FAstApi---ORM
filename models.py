from sqlalchemy import Column, Integer, String, Numeric, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

from database import Base

class Categoria(Base):
    __tablename__ = 'categorias'
    # id (PK, inteiro, auto)
    id = Column(Integer, primary_key=True, autoincrement=True)
    # nome (texto, obrigatorio)
    nome = Column(String, nullable=False)
    # descricao (texto, opcional)
    descricao = Column(String, nullable=True)
    # Relacionamento para facilitar a busca de produtos de uma categoria
    produtos = relationship("Produto", back_populates="categoria")

    def __repr__(self):
        return f"Categoria = id: {self.id} - Nome: {self.nome} - Descrição: {self.descricao} - Produtos: {self.produtos}"

class Produto(Base):
    __tablename__ = 'produtos'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False)
    preco = Column(Numeric(10, 2), nullable=False)
    estoque = Column(Integer, nullable=False)
    descricao = Column(String, nullable=True)  # ✅ Adicione esta linha
    categoria_id = Column(Integer, ForeignKey('categorias.id'), nullable=False)

    categoria = relationship("Categoria", back_populates="produtos")
    
    def __repr__(self):
        return f"Produto = id: {self.id} - Nome: {self.nome} - Preço: {self.preco} - Estoque: {self.estoque} - Categoria_id: {self.categoria_id} - Categoria: {self.categoria}"