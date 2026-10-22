import logging

from fastapi import FastAPI, HTTPException, Path, Query, Request, Response
from fastapi.responses import JSONResponse
from mysql.connector import Error as mysql_error

from database import executar_sql

app = FastAPI(title="API REST 2INFO3")


@app.exception_handler(mysql_error)
def erro_de_banco_de_dados(request: Request, exc: mysql_error):
    logging.getLogger("uvicorn.error").error("Erro de BD: %s", exc)
    return JSONResponse(
        status_code=500,
        content={
            "message": "Erro de banco de dados. Por favor, tente novamente mais tarde."
        },
    )


def representar_produtos(produto):
    return {
        "id": produto["id"],
        "nome": produto["nome"],
        "categoria": produto["categoria"],
        "preco": round(float(produto["preco"]), 2),
    }


@app.get("/produtos")
def listar_produtos():
    sql = "SELECT * FROM produtos"
    produtos = executar_sql(sql)
    return {
        "dados": [representar_produtos(produto) for produto in produtos],
        "instrucaosql": {"sql": sql, "parametros": []},
    }
