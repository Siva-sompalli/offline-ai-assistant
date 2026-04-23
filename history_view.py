import streamlit as st
from database import get_connection

def show_history(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT question, answer FROM history WHERE user_id=?",
        (user_id,)
    )
    rows = cursor.fetchall()
    conn.close()

    st.subheader("Your History")

    if not rows:
        st.write("No history available")
    else:
        for q, a in rows:
            st.write("Q:", q)
            st.write("A:", a)
            st.markdown("---")
