from database import get_connection

def save_history(user_id, question, answer):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO history (user_id, question, answer) VALUES (?, ?, ?)",
        (user_id, question, answer)
    )
    conn.commit()
    conn.close()
