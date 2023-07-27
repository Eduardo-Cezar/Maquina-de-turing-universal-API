from automata.tm.dtm import DTM
from fastapi import FastAPI, Request, Depends
from fastapi_mail import ConnectionConfig, MessageSchema, MessageType, FastMail
from sqlalchemy.orm import Session

from sql_app import crud, models, schemas
from sql_app.database import engine, SessionLocal
from util.email_body import EmailSchema

from prometheus_fastapi_instrumentator import Instrumentator

import json
import pika as pk

models.Base.metadata.create_all(bind=engine)

exchange_name = 'mtu'
queue_name = "fila_mtu"
mtu_routing_key = 'chave_mtu'
ip_container = 'localhost'

def connect_rabbit(request):
    conn = pk.BlockingConnection(pk.ConnectionParameters(host=ip_container))
    channel = conn.channel()
    print("Conectou ao rabbitmq")

    my_tag= mtu_routing_key #routing_key
    message= request
    channel.basic_publish(exchange=exchange_name, routing_key=my_tag, body=message)
    conn.close()

conf = ConnectionConfig(
    MAIL_USERNAME="2ba16197295077",
    MAIL_PASSWORD="0ea1e12f15bce3",
    MAIL_FROM="from@example.com",
    MAIL_PORT=587,
    MAIL_SERVER="sandbox.smtp.mailtrap.io",
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)

app = FastAPI()

Instrumentator().instrument(app).expose(app)


# Patter Singleton
# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/get_history/{id}")
async def get_history(id: int, db: Session = Depends(get_db)):
    history = crud.get_history(db=db, id=id)
    if history is None:
        return {
            "code": "404",
            "msg": "not found"
        }
    return history


@app.get("/get_all_history")
async def get_all_history(db: Session = Depends(get_db)):
    history = crud.get_all_history(db=db)
    return history

@app.post("/batch")
async def batch(info: Request):
  info = await info.json()
  requestsx = str(info)
  requestsx = requestsx.replace("'", '"')
  data = json.loads(requestsx)
  requests_list = data["requests"]
  for request in requests_list:
    print(request)
    print("\n---------------------------------------------------------------------------\n")
    connect_rabbit(request)
  print("entrou")

@app.post("/dtm")
async def dtm(info: Request, db: Session = Depends(get_db)):
    info = await info.json()
    states = set(info.get("states", []))

    if len(states) == 0:
        return {
            "code": "400",
            "msg": "states cannot be empty"
        }
    input_symbols = set(info.get("input_symbols", []))
    if len(input_symbols) == 0:
        return {
            "code": "400",
            "msg": "input_symbols cannot be empty"
        }
    tape_symbols = set(info.get("tape_symbols", []))
    if len(tape_symbols) == 0:
        return {
            "code": "400",
            "msg": "tape_symbols cannot be empty"
        }

    initial_state = info.get("initial_state", "")
    if initial_state == "":
        return {
            "code": "400",
            "msg": "initial_state cannot be empty"
        }
    blank_symbol = info.get("blank_symbol", "")
    if blank_symbol == "":
        return {
            "code": "400",
            "msg": "blank_symbol cannot be empty"
        }
    final_states = set(info.get("final_states", []))
    if len(final_states) == 0:
        return {
            "code": "400",
            "msg": "final_states cannot be empty"
        }
    transitions = dict(info.get("transitions", {}))
    if len(transitions) == 0:
        return {
            "code": "400",
            "msg": "transitions cannot be empty"
        }

    input = info.get("input", "")
    if input == "":
        return {
            "code": "400",
            "msg": "input cannot be empty"
        }

    dtm = DTM(
        states=states,
        input_symbols=input_symbols,
        tape_symbols=tape_symbols,
        transitions=transitions,
        initial_state=initial_state,
        blank_symbol=blank_symbol,
        final_states=final_states,
    )
    if dtm.accepts_input(input):
        print('accepted')
        result = "accepted"
    else:
        print('rejected')
        result = "rejected"

    history = schemas.History(query=str(info), result=result)
    crud.create_history(db=db, history=history)

    email_shema = EmailSchema(email=["to@example.com"])

    await simple_send(email_shema, result=result, configuration=str(info))

    return {
        "code": result == "accepted" and "200" or "400",
        "msg": result
    }


async def simple_send(email: EmailSchema, result: str, configuration: str):
    html = """
    <p>Thanks for using Fastapi-mail</p>
    <p> The result is: """ + result + """</p>
    <p> We have used this configuration: """ + configuration + """</p>
    """
    message = MessageSchema(
        subject="Fastapi-Mail module",
        recipients=email.dict().get("email"),
        body=html,
        subtype=MessageType.html)

    fm = FastMail(conf)
    await fm.send_message(message)
    return "OK"
