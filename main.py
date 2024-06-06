from http.client import HTTPResponse
from fastapi import FastAPI, Request , Form
from fastapi.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles
from test import*
from fastapi.responses import HTMLResponse, RedirectResponse

# ข้อมูลผู้ใช้ที่ตั้งค่าไว้
fake_users_db = {
    "admin": "password"
}


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="static/web")


@app.get("/")
def read_pdf(request: Request):
    conn = connect_db("docs.db")
    docs = conn.execute('SELECT * FROM pdf').fetchall()
    print(docs)
    conn.close()
    return templates.TemplateResponse("test.html", {"request": request, "docs": docs})


@app.get("/docs/{token}")
async def read_index(token ,request: Request):
    name = test(token)
    context = {
        'request': request,
        'value': f'/static/document/{name}.pdf',
    }
    
    return templates.TemplateResponse("viewer.html", context)

@app.get("/login", response_class=HTMLResponse)
async def login_form(request: Request):
    return templates.TemplateResponse("signin.html", {"request": request})






