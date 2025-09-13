import json
import os

# Arquivo JSON para armazenar sleepcoins
SLEEPCOINS_FILE = "sleepcoins.json"

# Carregar ou criar dados iniciais
if os.path.exists(SLEEPCOINS_FILE):
    with open(SLEEPCOINS_FILE, "r") as file:
        sleepcoins = json.load(file)
else:
    sleepcoins = {"users": {}, "total_sleepcoins": 0, "total_users": 0}
    with open(SLEEPCOINS_FILE, "w") as file:
        json.dump(sleepcoins, file, indent=4)


# Salvar dados
def save_sleepcoins_file():
    with open(SLEEPCOINS_FILE, "w") as file:
        json.dump(sleepcoins, file, indent=4)


# Função para criar usuário se não existir
def ensure_user(user_id):
    user_id = str(user_id)
    if user_id not in sleepcoins["users"]:
        sleepcoins["users"][user_id] = 0
        sleepcoins["total_users"] += 1


# Adicionar sleepcoins
def add_sleepcoins(user_id, amount):
    ensure_user(user_id)
    user_id = str(user_id)
    sleepcoins["users"][user_id] += amount
    sleepcoins["total_sleepcoins"] += amount
    save_sleepcoins_file()


# Obter sleepcoins
def get_sleepcoins(user_id):
    user_id = str(user_id)
    ensure_user(user_id)
    return sleepcoins["users"].get(user_id, 0)
