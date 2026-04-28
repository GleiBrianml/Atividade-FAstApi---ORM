from fastapi import FastAPI, Depends, HTTPException, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import get_db
from models import Curso, Aluno
#pip install jinja2 python-multipart

#INicializar o fastapi

app = FastAPI(title="Gestão escolar")

templates = Jinja2Templates(directory="templates")