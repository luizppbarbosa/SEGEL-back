import database.model as model
from fastapi.testclient import TestClient
from database.database import SessionLocal
from auth import manager as auth_manager

import database.model as model

import main
from database import model


client = TestClient(main.app)


def test_create_account():
    print(" ")
    print("***  TESTE DO ENDPOINT DE CRIAÇÃO DE CONTAS  ***")
    # dados de exemplo para criar uma nova conta
    new_account = {
        "id": "string",
        "email": "test@example.com",
        "cpf": "12345678900",
        "name": "Test User",
        "hashed_password": "password",
        "user_type": "0",
        "available": True,
        "phone_number": "1234567890"
    }

    # faz uma solicitação POST para o endpoint de criação de conta
    response = client.post("/account/create", json=new_account)

    # verifique se a resposta da API é bem sucedida (código 200)
    assert response.status_code == 200
    print("A resposta da API foi bem sucedida")

    # verifique se a resposta contém os dados da nova conta criada
    assert response.json()["email"] == new_account["email"]
    assert response.json()["cpf"] == new_account["cpf"]
    assert response.json()["name"] == new_account["name"]
    print("Os dados da nova conta estão corretos na resposta da API")

    # verifique se a conta foi realmente criada no banco de dados
    db = SessionLocal()
    account = db.query(model.Account).filter(model.Account.email == new_account["email"]).first()
    assert account is not None
    assert account.email == new_account["email"]
    assert account.cpf == new_account["cpf"]
    assert account.name == new_account["name"]
    print("A conta foi criada com sucesso no banco de dados")


    print(" ")




def test_create_area():
    # dados de exemplo para criar uma nova área
    new_area = {
        "name": "Test Area",
        "description": "Test Area Description",
        "available": True,
        "account_id": "string"
    }

    # faz uma solicitação POST para o endpoint de criação de área
    response = client.post("/area/create", json=new_area)

    # verifique se a resposta da API é bem sucedida (código 200)
    assert response.status_code == 200

    # verifique se a resposta contém os dados da nova área criada
    assert response.json()["name"] == new_area["name"]
    assert response.json()["description"] == new_area["description"]

    # verifique se a área foi realmente criada no banco de dados
    db = SessionLocal()
    area = db.query(model.Area).filter(model.Area.name == new_area["name"]).first()
    assert area is not None
    assert area.name == new_area["name"]
    assert area.description == new_area["description"]



def test_create_reservation():
    # dados de exemplo para criar uma nova reserva
    new_reservation = {
        "value": 0,
        "reservation_date": "04-08-2023",
        "time_start": "12:00",
        "time_end": "13:00",
        "justification": "Pq sim",
        "reservation_type": "Reserva",
        "status": "Arquivado",
        "area_id": "1",
        "account_id": "1"
    }

    # faz uma solicitação POST para o endpoint de criação de reserva
    response = client.post("/reservation/create", json=new_reservation)

    # verifique se a resposta da API é bem sucedida (código 200)
    assert response.status_code == 200

    # verifique se a resposta contém os dados da nova reserva criada
    
    assert response.json()["reservation_date"] == new_reservation["reservation_date"]
    assert response.json()["time_start"] == new_reservation["time_start"]
    assert response.json()["time_end"] == new_reservation["time_end"]
    assert response.json()["justification"] == new_reservation["justification"]
    assert response.json()["reservation_type"] == new_reservation["reservation_type"]
    assert response.json()["status"] == new_reservation["status"]
    assert response.json()["area_id"] == new_reservation["area_id"]
    assert response.json()["account_id"] == new_reservation["account_id"]


    # verifique se a reserva foi realmente criada no banco de dados
    db = SessionLocal()
    reservation = db.query(model.Reservation).filter(model.Reservation.reservation_date == new_reservation["reservation_date"]).first()
    assert reservation is not None
    assert reservation.reservation_date == new_reservation["reservation_date"]
    assert reservation.time_start == new_reservation["time_start"]
    assert reservation.time_end == new_reservation["time_end"]
    assert reservation.justification == new_reservation["justification"]
    assert reservation.reservation_type == new_reservation["reservation_type"]
    assert reservation.status == new_reservation["status"]
    assert reservation.area_id == new_reservation["area_id"]
    assert reservation.account_id == new_reservation["account_id"]

    # tentar criar uma outra reserva com o mesmo horário
    another_reservation = {
        "value": 0,
        "reservation_date": "04-08-2023",
        "time_start": "12:00",
        "time_end": "13:00",
        "justification": "Reserva conflito",
        "reservation_type": "Reserva",
        "status": "Arquivado",
        "area_id": "1",
        "account_id": "1"
    }

    # faz uma solicitação POST para o endpoint de criação da nova reserva
    response = client.post("/reservation/create", json=another_reservation)

    # verificar se a api não aceita a reserva (código 400)
    assert response.status_code == 400


    # tentar criar uma reserva com horário de início maior que o horário de término
    another_reservation2 = {
        "value": 0,
        "reservation_date": "04-08-2023",
        "time_start": "13:00",
        "time_end": "12:00",
        "justification": "Reserva falha",
        "reservation_type": "Reserva",
        "status": "Arquivado",
        "area_id": "1",
        "account_id": "1"
    }

    # faz uma solicitação POST para o endpoint de criação da nova reserva
    response = client.post("/reservation/create", json=another_reservation2)

    # verificar se a api não aceita a reserva (código 400)
    assert response.status_code == 400

    





    

def test_update_account():
    # dados de exemplo para atualizar uma conta
    update_account = {
        "name": "Test User Updated",
        "email": "updated@example.com",
        "hashed_password": "newpassword",
        "phone_number": "new1234567890"
    }

    # faz uma solicitação PUT para o endpoint de atualização de conta
    response = client.put("/account/update/1", json=update_account)

    # verifique se a resposta da API é bem sucedida (código 200)
    assert response.status_code == 200

    # verifique se a resposta contém os dados da conta atualizada
    assert response.json()["name"] == update_account["name"]
    assert response.json()["email"] == update_account["email"]
    assert response.json()["phone_number"] == update_account["phone_number"]

    # verifique se a conta foi realmente atualizada no banco de dados
    db = SessionLocal()
    account = db.query(model.Account).filter(model.Account.id == "1").first()
    assert account is not None
    assert account.name == update_account["name"]
    assert account.email == update_account["email"]
    assert account.phone_number == update_account["phone_number"]


def test_update_area():
    # dados de exemplo para atualizar uma área
    update_area = {
        "name": "Test Area Updated",
        "description": "Test Area Description Updated",
        "available": True,
        "account_id": "1"
    }

    # faz uma solicitação PUT para o endpoint de atualização de área
    response = client.put("/area/update/1", json=update_area)

    # verifique se a resposta da API é bem sucedida (código 200)
    assert response.status_code == 200

    # verifique se a resposta contém os dados da área atualizada
    assert response.json()["name"] == update_area["name"]
    assert response.json()["description"] == update_area["description"]
    assert response.json()["available"] == update_area["available"]

    # verifique se a área foi realmente atualizada no banco de dados
    db = SessionLocal()
    area = db.query(model.Area).filter(model.Area.id == "1").first()
    assert area is not None
    assert area.name == update_area["name"]
    assert area.description == update_area["description"]
    assert area.available == update_area["available"]


def test_update_reservation():
    # dados de exemplo para atualizar uma reserva
    update_reservation = {
        "value": 0,
        "reservation_date": "10-10-2023",
        "time_start": "12:00",
        "time_end": "13:00",
        "justification": "ATUALIZADO",
        "reservation_type": "Reserva",
        "status": "Arquivado",
        "area_id": "1",
        "account_id": "1"
    }

    # faz uma solicitação PUT para o endpoint de atualização de reserva
    response = client.put("/reservation/update/1", json=update_reservation)

    # verifique se a resposta da API é bem sucedida (código 200)
    assert response.status_code == 200

    # verifique se a resposta contém os dados da reserva atualizada
    assert response.json()["reservation_date"] == update_reservation["reservation_date"]
    assert response.json()["time_start"] == update_reservation["time_start"]
    assert response.json()["time_end"] == update_reservation["time_end"]
    assert response.json()["justification"] == update_reservation["justification"]
    assert response.json()["reservation_type"] == update_reservation["reservation_type"]
    assert response.json()["status"] == update_reservation["status"]
    assert response.json()["area_id"] == update_reservation["area_id"]
    assert response.json()["account_id"] == update_reservation["account_id"]

    # verifique se a reserva foi realmente atualizada no banco de dados
    db = SessionLocal()
    reservation = db.query(model.Reservation).filter(model.Reservation.id == "1").first()
    assert reservation is not None
    assert reservation.reservation_date == update_reservation["reservation_date"]
    assert reservation.time_start == update_reservation["time_start"]
    assert reservation.time_end == update_reservation["time_end"]
    assert reservation.justification == update_reservation["justification"]
    assert reservation.reservation_type == update_reservation["reservation_type"]
    assert reservation.status == update_reservation["status"]
    assert reservation.area_id == update_reservation["area_id"]
    assert reservation.account_id == update_reservation["account_id"]


def test_delete_reservation():
    # faz uma solicitação DELETE para o endpoint de exclusão de reserva
    response = client.delete("/reservation/delete/1")

    # verifique se a resposta da API é bem sucedida (código 200)
    assert response.status_code == 200

    # verifique se a reserva foi realmente excluída do banco de dados
    db = SessionLocal()
    reservation = db.query(model.Reservation).filter(model.Reservation.id == "1").first()
    assert reservation is None


"""def test_delete_area():
    # dados para deletar uma area
    delete_area = {
        "name": "Test Area Updated",
        "description": "Test Area Description Updated",
        "available": True,
        "account_id": "1"
    }

    # faz uma solicitação DELETE para o endpoint de exclusão de área
    response = client.delete("/area/delete/1")

    # verifique se a resposta da API é bem sucedida (código 200)
    assert response.status_code == 200

    # verifique se a área foi realmente excluída do banco de dados
    db = SessionLocal()
    area = db.query(model.Area).filter(model.Area.id == "1").first()
    assert area is None"""


"""def test_delete_account():
    # dados para deletar uma conta
    delete_account = {
        "available": True
    }
    

    # faz uma solicitação DELETE para o endpoint de exclusão de conta
    response = client.delete("/account/delete/1")

    # verifique se a resposta da API é bem sucedida (código 200)
    assert response.status_code == 200

    # verifique se a conta foi realmente excluída do banco de dados
    db = SessionLocal()
    account = db.query(model.Account).filter(model.Account.id == "1").first()
    assert account is None"""




# limpar o banco de dados após a execução dos testes
def test_clean_db():
    db = SessionLocal()
    db.query(model.Reservation).delete()
    db.query(model.Area).delete()
    db.query(model.Account).delete()
    
    db.commit()
    db.close()

    print("O banco de dados foi limpo com sucesso")



    





        



    

