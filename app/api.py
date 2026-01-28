import os
from flask import Flask, request, jsonify
from src.account_registry import AccountRegistry
from src.personal_account import PersonalAccount
from src.mongo_accounts_repository import MongoAccountsRepository

app = Flask(__name__)
registry = AccountRegistry()

# MongoDB configuration
MONGO_CONNECTION_STRING = os.getenv("MONGO_CONNECTION_STRING", "mongodb://localhost:27017")
MONGO_DATABASE_NAME = os.getenv("MONGO_DATABASE_NAME", "bank_app")
MONGO_COLLECTION_NAME = os.getenv("MONGO_COLLECTION_NAME", "accounts")

@app.route("/api/accounts", methods=['POST'])
def create_account():
    data = request.get_json()
    print(f"Create account request: {data}")
    if get_account_by_pesel(data["pesel"])[1] == 200:
        return jsonify({"error": "Account with this PESEL already exists"}), 409
    else:
        account = PersonalAccount(data["name"], data["surname"], data["pesel"])
        registry.add_account(account)
        return jsonify({"message": "Account created"}), 201

@app.route("/api/accounts", methods=['GET'])
def get_all_accounts():
    print("Get all accounts request received")
    accounts = registry.return_all_accounts()
    accounts_data = [{"name": acc.first_name, "surname": acc.last_name, "pesel":
    acc.pesel, "balance": acc.balance} for acc in accounts]
    return jsonify(accounts_data), 200

@app.route("/api/accounts/count", methods=['GET'])
def get_account_count():
    print("Get account count request received")
    count = registry.return_amount_of_accounts()
    return jsonify({"count": count}), 200

@app.route("/api/accounts/<pesel>", methods=['GET'])
def get_account_by_pesel(pesel):
    print(f"Get account by PESEL request received: {pesel}")
    account = registry.find_account_by_pesel(pesel)
    if account is None:
        return jsonify({"error": "Account not found"}), 404
    return jsonify({
        "name": account.first_name,
        "surname": account.last_name,
        "pesel": account.pesel,
        "balance": account.balance
    }), 200

@app.route("/api/accounts/<pesel>", methods=['PATCH'])
def update_account(pesel):
    account = registry.find_account_by_pesel(pesel)
    if account is None:
        return jsonify({"error": "Account not found"}), 404
    data = request.get_json()
    if "name" in data:
        account.first_name = data["name"]
    if "surname" in data:
        account.last_name = data["surname"]
    return jsonify({"message": "Account updated"}), 200
    
@app.route("/api/accounts/<pesel>", methods=['DELETE'])
def delete_account(pesel):
    account = registry.find_account_by_pesel(pesel)
    if account is None:
        return jsonify({"error": "Account not found"}), 404
    registry.remove_account(account)
    return jsonify({"message": "Account deleted"}), 200

@app.route("/api/accounts/<pesel>/transfer", methods=['POST'])
def transfer_money(pesel):
    account = registry.find_account_by_pesel(pesel)
    if account is None:
        return jsonify({"error": "Account not found"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid body"}), 400
        
    amount = data.get("amount")
    transfer_type = data.get("type")

    if not isinstance(amount, (int, float)) or amount <= 0:
         return jsonify({"error": "Invalid amount"}), 400

    if transfer_type == "incoming":
        account.incoming_transfer(amount)
        return jsonify({"message": "Zlecenie przyjęto do realizacji"}), 200
    
    elif transfer_type == "outgoing":
        old_balance = account.balance
        account.outgoing_transfer(amount)
        if account.balance == old_balance:
            return jsonify({"error": "Transfer failed"}), 422
        return jsonify({"message": "Zlecenie przyjęto do realizacji"}), 200

    elif transfer_type == "express":
        old_balance = account.balance
        account.express_outgoing_transfer(amount)
        if account.balance == old_balance:
             return jsonify({"error": "Transfer failed"}), 422
        return jsonify({"message": "Zlecenie przyjęto do realizacji"}), 200
    
    else:
        return jsonify({"error": "Invalid transfer type"}), 400

@app.route("/api/accounts/save", methods=['POST'])
def save_accounts_to_db():
    try:
        repo = MongoAccountsRepository(
            connection_string=MONGO_CONNECTION_STRING,
            database_name=MONGO_DATABASE_NAME,
            collection_name=MONGO_COLLECTION_NAME
        )
        accounts = registry.return_all_accounts()
        repo.save_all(accounts)
        repo.close()
        return jsonify({
            "message": "Accounts saved to database",
            "count": len(accounts)
        }), 200
    except Exception as e:
        return jsonify({"error": f"Failed to save accounts: {str(e)}"}), 500


@app.route("/api/accounts/load", methods=['POST'])
def load_accounts_from_db():
    try:
        repo = MongoAccountsRepository(
            connection_string=MONGO_CONNECTION_STRING,
            database_name=MONGO_DATABASE_NAME,
            collection_name=MONGO_COLLECTION_NAME
        )
        loaded_accounts = repo.load_all()
        repo.close()
        
        registry.accounts.clear()
        
        for account in loaded_accounts:
            registry.add_account(account)
        
        return jsonify({
            "message": "Accounts loaded from database",
            "count": len(loaded_accounts)
        }), 200
    except Exception as e:
        return jsonify({"error": f"Failed to load accounts: {str(e)}"}), 500