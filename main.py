from fastapi import FastAPI, Depends, HTTPException, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import get_db
from models import Categoria, Produto
#pip install jinja2 python-multipart

#INicializar o fastapi

app = FastAPI(title="Gestão escolar")

templates = Jinja2Templates(directory="templates")

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        request,
        "index.html",
        {"request": request}
    )

@app.get("/categorias")
def listar_categorias(
    request: Request,                   
    db: Session = Depends(get_db)
    ):

    categorias = db.query(Categoria).all()
    return templates.TemplateResponse(
        request,
        "categorias.html",
        {"request": request, "categorias": categorias}
    )

@app.get("/categorias/cadastro")
def exibir_cadastro(request: Request):
    return templates.TemplateResponse(
        request,
        "cadastrar_categoria.html",
        {"request": request}
    )

@app.post("/categorias")
def criar_categoria(
    nome: str = Form(...),
    descricao: str = Form(...),
    db: Session = Depends(get_db),
):
    # Cadastrar a categoria no banco
    nova_categoria = Categoria(nome=nome, descricao=descricao)
    db.add(nova_categoria)
    db.commit()

    return RedirectResponse(url="/categorias", status_code=303)

@app.post("/produtos")
def criar_produto(
    nome: str = Form(...),
    descricao: str = Form(...),
    preco: float = Form(...),
    categoria_id: int = Form(...),
    db: Session = Depends(get_db),
):
    # Verificar se a categoria existe
    categoria = db.query(Categoria).filter(Categoria.id == categoria_id).first()
    if not categoria:
        raise HTTPException(status_code=400, detail="Categoria não encontrada")

    # Cadastrar o produto no banco com FK
    novo_produto = Produto(nome=nome, descricao=descricao, preco=preco, categoria_id=categoria_id)
    db.add(novo_produto)
    db.commit()

    return RedirectResponse(url="/produtos", status_code=303)

@app.post("/categorias/{categoria_id}/produtos")
def deletar_produtos_categoria(
    categoria_id: int,
    db: Session = Depends(get_db)
):
    # Verificar se a categoria existe
    categoria = db.query(Categoria).filter(Categoria.id == categoria_id).first()
    if not categoria:
        raise HTTPException(status_code=400, detail="Categoria não encontrada")

    # Deletar os produtos relacionados à categoria
    db.query(Produto).filter(Produto.categoria_id == categoria_id).delete()
    db.commit()

    return RedirectResponse(url="/categorias", status_code=303)