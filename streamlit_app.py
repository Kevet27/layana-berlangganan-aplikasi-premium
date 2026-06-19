import streamlit as st
import sqlite3
import os
from PIL import Image

# ====================================
# KONFIGURASI
# ====================================
st.set_page_config(
    page_title="Premium Store",
    page_icon="👑",
    layout="wide"
)

# ====================================
# FOLDER UPLOAD
# ====================================
if not os.path.exists("uploads"):
    os.makedirs("uploads")

# ====================================
# KONEKSI DATABASE
# ====================================
conn = sqlite3.connect(
    "database.db",
    check_same_thread=False
)

c = conn.cursor()

# ====================================
# TABEL USER
# ====================================
c.execute("""
CREATE TABLE IF NOT EXISTS users(
id INTEGER PRIMARY KEY AUTOINCREMENT,
username TEXT UNIQUE,
password TEXT,
role TEXT
)
""")

# ====================================
# TABEL PRODUK
# ====================================
c.execute("""
CREATE TABLE IF NOT EXISTS products(
id INTEGER PRIMARY KEY AUTOINCREMENT,
nama TEXT,
kategori TEXT,
durasi TEXT,
harga INTEGER,
gambar TEXT
)
""")

# ====================================
# TABEL ORDER
# ====================================
c.execute("""
CREATE TABLE IF NOT EXISTS orders(
id INTEGER PRIMARY KEY AUTOINCREMENT,
username TEXT,
produk TEXT,
harga INTEGER,
status TEXT,
bukti TEXT
)
""")

conn.commit()

# ====================================
# ADMIN DEFAULT
# ====================================
c.execute(
    "SELECT * FROM users WHERE username=?",
    ("admin",)
)

admin = c.fetchone()

if admin is None:

    c.execute(
        """
        INSERT INTO users(
        username,password,role)
        VALUES(?,?,?)
        """,
        (
            "admin",
            "admin123",
            "admin"
        )
    )

    conn.commit()

# ====================================
# SESSION
# ====================================
if "login" not in st.session_state:
    st.session_state.login = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "role" not in st.session_state:
    st.session_state.role = ""

# ====================================
# SIDEBAR AWAL
# ====================================
menu = st.sidebar.selectbox(
    "Menu",
    [
        "Beranda",
        "Login",
        "Registrasi"
    ]
)
