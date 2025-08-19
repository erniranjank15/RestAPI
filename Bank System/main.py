from fastapi import FastAPI, HTTPException
import sqlite3

app = FastAPI()
def init_db():
    conn = sqlite3.connect("bank.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS accounts (
        account_no INTEGER PRIMARY KEY AUTOINCREMENT,
        holder_name TEXT NOT NULL,
        account_type TEXT NOT NULL
    )
    """)
    conn.commit()
    conn.close()
init_db()  

@app.post("/accounts/")
def create_account(holder_name: str, account_type: str):
    conn = sqlite3.connect("bank.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO accounts (holder_name, account_type) VALUES (?, ?)",
                   (holder_name, account_type))
    conn.commit()
    account_no = cursor.lastrowid  # Auto-generated account number
    conn.close()
    return {"account_no": account_no, "holder_name": holder_name, "account_type": account_type}
 
@app.get("/accounts/{account_no}")
def get_account(account_no: int):
    conn = sqlite3.connect("bank.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM accounts WHERE account_no=?", (account_no,))
    account = cursor.fetchone()
    conn.close()
    if account:
        return {"account_no": account[0], "holder_name": account[1], "account_type": account[2]}
    else:
        raise HTTPException(status_code=404, detail="Account not found")
 
@app.put("/accounts/{account_no}")
def update_account(account_no: int, holder_name: str, account_type: str):
    conn = sqlite3.connect("bank.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE accounts SET holder_name=?, account_type=? WHERE account_no=?",
                   (holder_name, account_type, account_no))
    conn.commit()
    updated = cursor.rowcount
    conn.close()
    if updated == 0:
        raise HTTPException(status_code=404, detail="Account not found")
    return {"message": "Account updated successfully"}

@app.delete("/accounts/{account_no}")
def delete_account(account_no: int):
    conn = sqlite3.connect("bank.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM accounts WHERE account_no=?", (account_no,))
    conn.commit()
    deleted = cursor.rowcount
    conn.close()
    if deleted == 0:
        raise HTTPException(status_code=404, detail="Account not found")
    return {"message": "Account deleted successfully"}
