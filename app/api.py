from flask import Flask, request, jsonify
from src.account_registry import AccountRegistry
from src.personal_account import PersonalAccount

app = Flask(__name__)
registry = AccountRegistry()

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