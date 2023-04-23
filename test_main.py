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

    # tentar criar uma conta com o mesmo email
    print("**Tentando criar uma conta com o mesmo email**")
    new_account2 = {
        "id": "string",
        "email": "test@example.com",
        "cpf": "12345678900",
        "name": "outra conta com mesmo email",
        "hashed_password": "password",
        "user_type": "0",
        "available": True,
        "phone_number": "1234567890"
    }

    # faz uma solicitação POST para o endpoint de criação de conta
    response = client.post("/account/create", json=new_account2)

    # verifica se a api retornou um erro
    assert response.status_code == 400
    print("A API retornou um erro, pois já existe uma conta com o mesmo email")
    print("status code = "+str(response.status_code))

    # imprimir detalhes do erro
    print("response = "+ response.json()["detail"])

    print(" ")

    print("TESTE DE CRIAÇÃO DE CONTAS FINALIZADO COM SUCESSO!!")


    print(" ---------------------------------------------- ")




def test_create_area():
    print(" ")
    print("***  TESTE DO ENDPOINT DE CRIAÇÃO DE ÁREAS  ***")

    # query para pegar o id do usuário criado no teste anterior
    db = SessionLocal()
    account = db.query(model.Account).filter(model.Account.email == "test@example.com").first()
    account_id = str(account.id)


    # dados de exemplo para criar uma nova área
    new_area = {
        "name": "Test Area",
        "description": "Test Area Description",
        "available": True,
        "account_id": account_id
    }

    # faz uma solicitação POST para o endpoint de criação de área
    response = client.post("/area/create", json=new_area)

    # verifique se a resposta da API é bem sucedida (código 200)
    assert response.status_code == 200
    print("A resposta da API foi bem sucedida")


    # verifique se a resposta contém os dados da nova área criada
    assert response.json()["name"] == new_area["name"]
    assert response.json()["description"] == new_area["description"]
    print("Os dados da nova área estão corretos na resposta da API")

    # verifique se a área foi realmente criada no banco de dados
    db = SessionLocal()
    area = db.query(model.Area).filter(model.Area.name == new_area["name"]).first()
    assert area is not None
    assert area.name == new_area["name"]
    assert area.description == new_area["description"]
    print("A área foi criada com sucesso no banco de dados")

    print(" ")

    # tentar criar uma área com o mesmo nome
    print("**Tentando criar uma área com o mesmo nome**")
    new_area2 = {
        "name": "Test Area",
        "description": "Teste de área com mesmo nome",
        "available": True,
        "account_id": "string"
    }

    # faz uma solicitação POST para o endpoint de criação de área
    response = client.post("/area/create", json=new_area2)

    # verifica se a api retornou um erro
    assert response.status_code == 400
    print("A API retornou um erro, pois já existe uma área com o mesmo nome")
    print("status code = "+str(response.status_code))

    # imprimir detalhes do erro
    print("response = "+ response.json()["detail"])

    print(" ")

    print("TESTE DE CRIAÇÃO DE ÁREAS FINALIZADO COM SUCESSO!!")
    
    print(" ---------------------------------------------- ")



def test_create_reservation():
    print(" ")
    print("***  TESTE DO ENDPOINT DE CRIAÇÃO DE RESERVAS  ***")

    # query no banco de dados para pegar o id da conta criada no teste anterior
    db = SessionLocal()
    account = db.query(model.Account).filter(model.Account.email == "test@example.com").first()
    account_id = str(account.id)

    # query no banco de dados para pegar o id da área criada no teste anterior
    area = db.query(model.Area).filter(model.Area.name == "Test Area").first()
    area_id = str(area.id)


    # dados de exemplo para criar uma nova reserva
    
    new_reservation = {
        "value": 0,
        "reservation_date": "04-08-2023",
        "time_start": "12:00",
        "time_end": "13:00",
        "justification": "Pq sim",
        "reservation_type": "Reserva",
        "status": "Arquivado",
        "area_id": account_id,
        "account_id": area_id
    }

    # faz uma solicitação POST para o endpoint de criação de reserva
    response = client.post("/reservation/create", json=new_reservation)

    # verifique se a resposta da API é bem sucedida (código 200)
    assert response.status_code == 200
    print("A resposta da API foi bem sucedida")


    # verifique se a resposta contém os dados da nova reserva criada
    
    assert response.json()["reservation_date"] == new_reservation["reservation_date"]
    assert response.json()["time_start"] == new_reservation["time_start"]
    assert response.json()["time_end"] == new_reservation["time_end"]
    assert response.json()["justification"] == new_reservation["justification"]
    assert response.json()["reservation_type"] == new_reservation["reservation_type"]
    assert response.json()["status"] == new_reservation["status"]
    assert response.json()["area_id"] == new_reservation["area_id"]
    assert response.json()["account_id"] == new_reservation["account_id"]
    print("Os dados da nova reserva estão corretos na resposta da API")

    # query para pegar o id da reserva pela data, hora de início e fim da reserva
    db = SessionLocal()
    reservation_id = db.query(model.Reservation.id).filter(model.Reservation.reservation_date == "04-08-2023").filter(model.Reservation.time_start == "12:00").filter(model.Reservation.time_end == "13:00").first()
    reservation_id = str(reservation_id[0])

    # verifique se a reserva foi realmente criada no banco de dados
    db = SessionLocal()
    reservation = db.query(model.Reservation).filter(model.Reservation.id == reservation_id).first()
    assert reservation is not None
    assert reservation.reservation_date == new_reservation["reservation_date"]
    assert reservation.time_start == new_reservation["time_start"]
    assert reservation.time_end == new_reservation["time_end"]
    assert reservation.justification == new_reservation["justification"]
    assert reservation.reservation_type == new_reservation["reservation_type"]
    assert reservation.status == new_reservation["status"]
    assert reservation.area_id == new_reservation["area_id"]
    assert reservation.account_id == new_reservation["account_id"]
    print("A reserva foi criada com sucesso no banco de dados")

    print(" ")


    # tentar criar uma outra reserva com o mesmo horário
    print("**Tentando criar uma reserva com a mesma data e o mesmo horário**")

    another_reservation = {
        "value": 0,
        "reservation_date": "04-08-2023",
        "time_start": "12:00",
        "time_end": "13:00",
        "justification": "Reserva conflito",
        "reservation_type": "Reserva",
        "status": "Arquivado",
        "area_id": account_id,
        "account_id": area_id
    }

    # faz uma solicitação POST para o endpoint de criação da nova reserva
    response = client.post("/reservation/create", json=another_reservation)

    # verificar se a api não aceita a reserva (código 400)
    assert response.status_code == 400
    print("A API retornou um erro, pois já existe uma reserva com a mesma data e o mesmo horário")
    print("status code = "+str(response.status_code))

    # imprimir detalhes do erro
    print("response = "+ response.json()["detail"])

    print(" ")


    # tentar criar uma reserva com horário de início maior que o horário de término
    print("**Tentando criar uma reserva com horário de início maior que o horário de término**")

    another_reservation2 = {
        "value": 0,
        "reservation_date": "04-08-2023",
        "time_start": "13:00",
        "time_end": "12:00",
        "justification": "Reserva falha",
        "reservation_type": "Reserva",
        "status": "Arquivado",
        "area_id": account_id,
        "account_id": area_id
    }

    # faz uma solicitação POST para o endpoint de criação da nova reserva
    response = client.post("/reservation/create", json=another_reservation2)

    # verificar se a api não aceita a reserva (código 400)
    assert response.status_code == 400
    print("A API retornou um erro, pois o horário de início é maior que o horário de término")
    print("status code = "+str(response.status_code))

    # imprimir detalhes do erro
    print("response = "+ response.json()["detail"])

    print(" ")

    print ("TESTE DE CRIAÇÃO DE RESERVA CONCLUÍDO COM SUCESSO!!")

    print(" ---------------------------------------------- ")



def test_update_account():

    print(" ")
    print("***  TESTE DO ENDPOINT DE ATUALIZAÇÃO DE CONTA  ***")
    # dados de exemplo para atualizar uma conta
    update_account = {
        "name": "Test User Updated",
        "email": "updated@example.com",
        "hashed_password": "newpassword",
        "phone_number": "new1234567890"
    }

    # query para pegar o id da conta pelo cpf
    db = SessionLocal()
    account_id = db.query(model.Account.id).filter(model.Account.cpf == "12345678900").first()
    account_id = account_id[0]

    # faz uma solicitação PUT para o endpoint de atualização de conta
    response = client.put("/account/update/"+account_id, json=update_account)

    # verifique se a resposta da API é bem sucedida (código 200)
    assert response.status_code == 200
    print("A resposta da API foi bem sucedida")

    # verifique se a resposta contém os dados da conta atualizada
    assert response.json()["name"] == update_account["name"]
    assert response.json()["email"] == update_account["email"]
    assert response.json()["phone_number"] == update_account["phone_number"]
    print("Os dados da conta atualizados estão corretos na resposta da API")

    # verifique se a conta foi realmente atualizada no banco de dados
    db = SessionLocal()
    account = db.query(model.Account).filter(model.Account.id == account_id).first()
    assert account is not None
    assert account.name == update_account["name"]
    assert account.email == update_account["email"]
    assert account.phone_number == update_account["phone_number"]
    print("A conta foi atualizada com sucesso no banco de dados")

    print(" ")

    # tentar atualizar uma conta inexistente
    print("**Tentando atualizar uma conta inexistente**")

    # faz uma solicitação PUT para o endpoint de atualização de conta
    response = client.put("/account/update/999", json=update_account)

    # verificar se a api não aceita a atualização (código 404)
    assert response.status_code == 404
    print("A API retornou um erro, pois a conta não existe")
    print("status code = "+str(response.status_code))

    # imprimir detalhes do erro
    print("response = "+ response.json()["detail"])

    print(" ")

    print("TESTE DE ATUALIZAÇÃO DE CONTA FINALIZADO COM SUCESSO!!")

    print(" ---------------------------------------------- ")


def test_update_area():

    print(" ")
    print("***  TESTE DO ENDPOINT DE ATUALIZAÇÃO DE ÁREA  ***")

    # query para pegar o account_id da área criada no teste anterior
    db = SessionLocal()
    account_id = db.query(model.Area).filter(model.Area.name == "Test Area").first()
    account_id = account_id.account_id

    # dados de exemplo para atualizar uma área
    update_area = {
        "name": "Test Area Updated",
        "description": "Test Area Description Updated",
        "available": True,
        "account_id": account_id
    }

    # query para pegar o id da área pelo nome
    db = SessionLocal()
    area_id = db.query(model.Area.id).filter(model.Area.name == "Test Area").first()
    area_id = str(area_id[0])


    # faz uma solicitação PUT para o endpoint de atualização de área
    response = client.put("/area/update/"+area_id, json=update_area)

    # verifique se a resposta da API é bem sucedida (código 200)
    assert response.status_code == 200
    print("A resposta da API foi bem sucedida")

    # verifique se a resposta contém os dados da área atualizada
    assert response.json()["name"] == update_area["name"]
    assert response.json()["description"] == update_area["description"]
    assert response.json()["available"] == update_area["available"]
    print("Os dados da área atualizados estão corretos na resposta da API")

    # verifique se a área foi realmente atualizada no banco de dados
    db = SessionLocal()
    area = db.query(model.Area).filter(model.Area.id == area_id).first()
    assert area is not None
    assert area.name == update_area["name"]
    assert area.description == update_area["description"]
    assert area.available == update_area["available"]
    print("A área foi atualizada com sucesso no banco de dados")

    print(" ")

    # tentar atualizar uma área inexistente
    print("**Tentando atualizar uma área inexistente**")

    # faz uma solicitação PUT para o endpoint de atualização de área com id inexistente
    response = client.put("/area/update/999", json=update_area)

    # verificar se a api não aceita a atualização (código 404)
    assert response.status_code == 404
    print("A API retornou um erro, pois a área não existe")

    # imprimir detalhes do erro
    print("response = "+ response.json()["detail"])


    print(" ")

    # tentar atualizar uma área com um usuário que não é um administrador
    print("**Tentando atualizar uma área com um usuário que não é um administrador**")

    # criar um novo usuário com permissão de usuário comum
    new_account = {
        "id": "string",
        "email": "testupdatearea@example.com",
        "cpf": "41234123412",
        "name": "NEW Test User",
        "hashed_password": "password",
        "user_type": "regular",
        "available": True,
        "phone_number": "1234567890"
    }


    # faz uma solicitação POST para o endpoint de criação de conta
    response = client.post("/account/create", json=new_account)

    # query para pegar o id do novo usuário
    db = SessionLocal()
    account_id = db.query(model.Account.id).filter(model.Account.email == "testupdatearea@example.com").first()
    account_id = str(account_id[0])

    # atualizar novamente a área com o novo usuário
    update_area2 = {
        "name": "Test Area Updated NEW",
        "description": "Test Area Description Updated",
        "available": True,
        "account_id": account_id
    }

    # query para pegar o id da área pelo nome
    db = SessionLocal()
    area_id = db.query(model.Area.id).filter(model.Area.name == "Test Area Updated").first()
    area_id = str(area_id[0])


    # faz uma solicitação PUT para o endpoint de atualização de área
    response = client.put("/area/update/"+area_id, json=update_area2)
    

    # verificar se a api não aceita a atualização (código 404)
    assert response.status_code == 404
    print("A API retornou um erro, pois o usuário não é um administrador ou não está cadastrado no banco de dados.")

    # imprimir detalhes do erro
    print("response = "+ response.json()["detail"])

    print(" ")


   # tebtar atualizar uma área com um usuário que não existe
    print("**Tentando atualizar uma área com um usuário que não existe**")

    # tentar atualizar novamente a área com um usuário que não existe
    update_area3 = {
        "name": "Test Area Updated NEW AGAIN",
        "description": "Test Area Description Updated AGAIN",
        "available": True,
        "account_id": "999"
    }

    # query para pegar o id da área pelo nome
    db = SessionLocal()
    area_id = db.query(model.Area.id).filter(model.Area.name == "Test Area Updated").first()
    area_id = str(area_id[0])


    # faz uma solicitação PUT para o endpoint de atualização de área
    response = client.put("/area/update/"+area_id, json=update_area3)   

    # verificar se a api não aceita a atualização (código 404)
    assert response.status_code == 404
    print("A API retornou um erro, pois o usuário não existe")

    # imprimir detalhes do erro
    print("response = "+ response.json()["detail"])

    print(" ")

    print("TESTE DE ATUALIZAÇÃO DE ÁREA FINALIZADO COM SUCESSO!!")

    print(" ---------------------------------------------- ")



def test_update_reservation():
    print(" ")
    print("***  TESTE DO ENDPOINT DE ATUALIZAÇÃO DE RESERVA  ***")

    # query para achar o id da área e do usuário que foram usados para criar a reserva do exemplo anterior
    db = SessionLocal()
    area_id = db.query(model.Area.id).filter(model.Area.name == "Test Area Updated").first()
    area_id = str(area_id[0])
    account_id = db.query(model.Account.id).filter(model.Account.email == "updated@example.com").first()
    account_id = str(account_id[0])


    # dados de exemplo para atualizar uma reserva
    update_reservation = {
        "value": 0,
        "reservation_date": "10-10-2023",
        "time_start": "12:00",
        "time_end": "13:00",
        "justification": "ATUALIZADO",
        "reservation_type": "Reserva",
        "status": "Arquivado",
        "area_id": area_id,
        "account_id": account_id
    }

    # query para pegar o id da reserva pela data, hora de início e fim da reserva
    db = SessionLocal()
    reservation_id = db.query(model.Reservation.id).filter(model.Reservation.reservation_date == "04-08-2023").filter(model.Reservation.time_start == "12:00").filter(model.Reservation.time_end == "13:00").first()
    reservation_id = str(reservation_id[0])


    # faz uma solicitação PUT para o endpoint de atualização de reserva
    response = client.put("/reservation/update/"+reservation_id, json=update_reservation)

    # verifique se a resposta da API é bem sucedida (código 200)
    assert response.status_code == 200
    print("A API retornou um código de sucesso")

    # verifique se a resposta contém os dados da reserva atualizada
    assert response.json()["reservation_date"] == update_reservation["reservation_date"]
    assert response.json()["time_start"] == update_reservation["time_start"]
    assert response.json()["time_end"] == update_reservation["time_end"]
    assert response.json()["justification"] == update_reservation["justification"]
    assert response.json()["reservation_type"] == update_reservation["reservation_type"]
    assert response.json()["status"] == update_reservation["status"]
    assert response.json()["area_id"] == update_reservation["area_id"]
    assert response.json()["account_id"] == update_reservation["account_id"]
    print("A API retornou os dados da reserva atualizada")

    # verifique se a reserva foi realmente atualizada no banco de dados
    db = SessionLocal()
    reservation = db.query(model.Reservation).filter(model.Reservation.id == reservation_id).first()
    assert reservation is not None
    assert reservation.reservation_date == update_reservation["reservation_date"]
    assert reservation.time_start == update_reservation["time_start"]
    assert reservation.time_end == update_reservation["time_end"]
    assert reservation.justification == update_reservation["justification"]
    assert reservation.reservation_type == update_reservation["reservation_type"]
    assert reservation.status == update_reservation["status"]
    assert reservation.area_id == update_reservation["area_id"]
    assert reservation.account_id == update_reservation["account_id"]
    print("A reserva foi realmente atualizada no banco de dados")

    print(" ")
    
    # tentar atualizar uma reserva inexistente
    print("**Tentando atualizar uma reserva inexistente**")

    # faz uma solicitação PUT para o endpoint de atualização de reserva
    response = client.put("/reservation/update/999", json=update_reservation)
    
    # verificar se a api não aceita a atualização (código 404)
    assert response.status_code == 404
    print("A API retornou um erro, pois a reserva não existe")

    # imprimir detalhes do erro
    print("response = "+ response.json()["detail"])

    print(" ")

    # tentar atualizar uma reserva com tempo de início maior que o tempo de fim
    print("**Tentando atualizar uma reserva com tempo de início maior que o tempo de fim**")

    # dados de exemplo para atualizar uma reserva
    update_reservation2 = {
        "value": 0,
        "reservation_date": "10-10-2023",
        "time_start": "13:00",
        "time_end": "12:00",
        "justification": "ATUALIZADO",
        "reservation_type": "Reserva",
        "status": "Arquivado",
        "area_id": area_id,
        "account_id": account_id
    }

    # faz uma solicitação PUT para o endpoint de atualização de reserva
    response = client.put("/reservation/update/"+reservation_id, json=update_reservation2)

    # verificar se a api não aceita a atualização (código 400)
    assert response.status_code == 400
    print("A API retornou um erro, pois o tempo de início é maior que o tempo de fim")

    # imprimir detalhes do erro
    print("response = "+ response.json()["detail"])

    print(" ")

    # tentar atualizar uma reserva para uma data e horário ja reservado
    print("**Tentando atualizar uma reserva para uma data e horário ja reservado**")

    # dados de exemplo para atualizar uma reserva
    update_reservation3 = {
        "value": 0,
        "reservation_date": "10-10-2023",
        "time_start": "12:00",
        "time_end": "13:00",
        "justification": "ATUALIZADO",
        "reservation_type": "Reserva",
        "status": "Arquivado",
        "area_id": area_id,
        "account_id": account_id
    }

    # faz uma solicitação PUT para o endpoint de atualização de reserva
    response = client.put("/reservation/update/"+reservation_id, json=update_reservation3)

    # verificar se a api não aceita a atualização (código 400)
    assert response.status_code == 400
    print("A API retornou um erro, pois a data e horário ja estão reservados")

    # imprimir detalhes do erro
    print("response = "+ response.json()["detail"])

    print(" ")

    print("TESTE DE ATUALIZAÇÃO DE RESERVA FINALIZADO COM SUCESSO!!")

    print(" ---------------------------------------------- ")




def test_delete_reservation():
    print(" ")
    print("***TESTE DO ENDPOINT DE EXCLUSÃO DE RESERVA***")
    # query para pegar o id da reserva pela data, hora de início e fim da reserva
    db = SessionLocal()
    reservation_id = db.query(model.Reservation.id).filter(model.Reservation.reservation_date == "10-10-2023").filter(model.Reservation.time_start == "12:00").filter(model.Reservation.time_end == "13:00").first()
    reservation_id = str(reservation_id[0])

    # faz uma solicitação DELETE para o endpoint de exclusão de reserva
    response = client.delete("/reservation/delete/"+reservation_id)

    # verifique se a resposta da API é bem sucedida (código 200)
    assert response.status_code == 200
    print("A API retornou os dados da reserva excluída")

    # verifique se a reserva foi realmente excluída do banco de dados
    db = SessionLocal()
    reservation = db.query(model.Reservation).filter(model.Reservation.id == reservation_id).first()
    assert reservation is None
    print("A reserva foi realmente excluída do banco de dados")
    
    # imprimir detalhes da exclusão
    print("response = "+ response.json()["message"])

    print(" ")

    # tentar excluir uma reserva inexistente
    print("**Tentando excluir uma reserva inexistente**")

    # faz uma solicitação DELETE para o endpoint de exclusão de reserva
    response = client.delete("/reservation/delete/999")

    # verificar se a api não aceita a exclusão (código 404)
    assert response.status_code == 404
    print("A API retornou um erro, pois a reserva não existe")

    # imprimir detalhes do erro
    print("response = "+ response.json()["detail"])

    print(" ")

    print("TESTE DE EXCLUSÃO DE RESERVA FINALIZADO COM SUCESSO!!")

    print(" ---------------------------------------------- ")


"""def test_delete_area():
    print(" ")
    print("***TESTE DO ENDPOINT DE EXCLUSÃO DE ÁREA***")
    # query para pegar o id da area pelo nome
    db = SessionLocal()
    area_id = db.query(model.Area.id).filter(model.Area.name == "Test Area Updated").first()
    area_id = str(area_id[0])


    # query para pegar o account_id da área criada no teste anterior
    db = SessionLocal()
    account_id = db.query(model.Area).filter(model.Area.name == "Test Area Updated").first()
    account_id = account_id.account_id

    # dados de exemplo para EXCLUIR uma área
    delete_area = {
        "account_id": account_id
    }

    # faz uma solicitação DELETE para o endpoint de exclusão de área
    response = client.delete("/area/delete/{area_id}")

    # verifique se a resposta da API é bem sucedida (código 200)
    assert response.status_code == 200
    print("A API retornou os dados da área excluída")

    # verifique se a área foi realmente excluída do banco de dados
    db = SessionLocal()
    area = db.query(model.Area).filter(model.Area.id == area_id).first()
    assert area is None
    print("A área foi realmente excluída do banco de dados")
    
    # imprimir detalhes da exclusão
    print("response = "+ response.json()["message"])

    print(" ")

    # tentar excluir uma área inexistente
    print("**Tentando excluir uma área inexistente**")

    # faz uma solicitação DELETE para o endpoint de exclusão de área
    response = client.delete("/area/delete/999")

    # verificar se a api não aceita a exclusão (código 404)
    assert response.status_code == 404
    print("A API retornou um erro, pois a área não existe")

    # imprimir detalhes do erro
    print("response = "+ response.json()["detail"])

    print(" ")

    print("TESTE DE EXCLUSÃO DE ÁREA FINALIZADO COM SUCESSO!!")

    print(" ---------------------------------------------- ")"""




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



    





        



    

