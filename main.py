from fastapi import FastAPI, Depends, HTTPException, Request, Form, responses, status
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import get_db
from models import Categoria, Produto

app = FastAPI(title="StockManager")
templates = Jinja2Templates(directory="templates")


# --- HOME ---

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(request, "index.html", {"request": request})


# --- CATEGORIAS ---

@app.get("/categorias")
def listar_categorias(request: Request, db: Session = Depends(get_db)):
    categorias = db.query(Categoria).all()
    return templates.TemplateResponse(
        request, "categorias.html", {"request": request, "categorias": categorias}
    )

@app.get("/categorias/cadastro")
def exibir_cadastro_categoria(request: Request):
    return templates.TemplateResponse(request, "cadastrar_categoria.html", {"request": request})



@app.get("/categorias/excluir/{categoria_id}")
def excluir_categoria(categoria_id: int, db: Session = Depends(get_db)):
    categoria = db.query(Categoria).filter(Categoria.id == categoria_id).first()
    if categoria:
        db.delete(categoria)
        db.commit()
    return responses.RedirectResponse(url="/categorias", status_code=status.HTTP_303_SEE_OTHER)

@app.get("/produtos")
def listar_produtos(request: Request, db: Session = Depends(get_db)):
    produtos = db.query(Produto).all()
    return templates.TemplateResponse(
        request, "produtos.html", {"request": request, "produtos": produtos}
    )
# --- PRODUTOS ---

@app.get("/produtos/cadastro")
def exibir_cadastro_produto(request: Request, db: Session = Depends(get_db)):
    categorias = db.query(Categoria).all()
    return templates.TemplateResponse(
        request, "cadastrar_produto.html", {"request": request, "categorias": categorias}
    )

@app.get("/produtos/excluir/{produto_id}")
def excluir_produto(produto_id: int, db: Session = Depends(get_db)):
    produto = db.query(Produto).filter(Produto.id == produto_id).first()
    if produto:
        db.delete(produto)
        db.commit()
    return responses.RedirectResponse(url="/produtos", status_code=status.HTTP_303_SEE_OTHER)


@app.post("/categorias/salvar")
def salvar_categoria(
    nome: str = Form(...),
    descricao: str = Form(None),
    db: Session = Depends(get_db)
):
    nova_categoria = Categoria(nome=nome, descricao=descricao)
    db.add(nova_categoria)
    db.commit()
    db.refresh(nova_categoria)
    return responses.RedirectResponse(url="/categorias", status_code=status.HTTP_303_SEE_OTHER)


@app.post("/produtos/salvar")
def salvar_produto(
    nome: str = Form(...),
    preco: float = Form(...),
    categoria_id: int = Form(...),
    descricao: str = Form(None),  # ✅ Campo que estava faltando
    estoque: int = Form(0),
    db: Session = Depends(get_db)
):
    categoria = db.query(Categoria).filter(Categoria.id == categoria_id).first()
    if not categoria:
        raise HTTPException(status_code=400, detail="Categoria não encontrada")

    novo_produto = Produto(
        nome=nome,
        preco=preco,
        descricao=descricao,
        estoque=estoque,
        categoria_id=categoria_id
    )
    db.add(novo_produto)
    db.commit()
    db.refresh(novo_produto)
    return responses.RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)  # ✅ Redireciona para home