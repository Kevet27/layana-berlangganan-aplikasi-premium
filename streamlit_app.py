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
# ====================================
# BERANDA AWAL
# ====================================
if menu == "Beranda":

    st.title("👑 PREMIUM STORE")

    st.write(
        """
        Selamat datang di Premium Store.
        
        Menyediakan berbagai layanan premium:
        
        ✅ Netflix Premium
        ✅ Spotify Premium
        ✅ Canva Pro
        ✅ YouTube Premium
        ✅ ChatGPT Plus
        ✅ CapCut Pro
        """
    )

# ====================================
# REGISTRASI
# ====================================
elif menu == "Registrasi":

    st.title("Registrasi Akun")

    username = st.text_input("Username")

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Daftar"):

        try:

            c.execute(
                """
                INSERT INTO users(
                username,password,role)
                VALUES(?,?,?)
                """,
                (
                    username,
                    password,
                    "user"
                )
            )

            conn.commit()

            st.success("Registrasi berhasil")

        except:

            st.error("Username sudah digunakan")

# ====================================
# LOGIN
# ====================================
elif menu == "Login":

    st.title("Login")

    username = st.text_input("Username")

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Masuk"):

        c.execute(
            """
            SELECT * FROM users
            WHERE username=? AND password=?
            """,
            (
                username,
                password
            )
        )

        user = c.fetchone()

        if user:

            st.session_state.login = True
            st.session_state.username = user[1]
            st.session_state.role = user[3]

            st.success("Login berhasil")

            st.rerun()

        else:

            st.error("Username atau password salah")

# ====================================
# SETELAH LOGIN
# ====================================
if st.session_state.login:

    st.sidebar.success(
        f"Login : {st.session_state.username}"
    )

    if st.sidebar.button("Logout"):

        st.session_state.login = False
        st.session_state.username = ""
        st.session_state.role = ""

        st.rerun()

    # ===============================
    # MENU USER
    # ===============================
    if st.session_state.role == "user":

        menu_user = st.sidebar.selectbox(
            "Menu User",
            [
                "Beranda User",
                "History Pembelian"
            ]
        )

        # ===========================
        # BERANDA USER
        # ===========================
        if menu_user == "Beranda User":

            st.header("Beranda User")

        # ===========================
        # HISTORY
        # ===========================
        elif menu_user == "History Pembelian":

            st.header("History Pembelian")

    # ===============================
    # MENU ADMIN
    # ===============================
    elif st.session_state.role == "admin":

        menu_admin = st.sidebar.selectbox(
            "Menu Admin",
            [
                "Dashboard",
                "Kelola Produk",
                "Kelola Pesanan"
            ]
        )

        # ===========================
        # DASHBOARD ADMIN
        # ===========================
        if menu_admin == "Dashboard":

            st.title("Dashboard Admin")

            c.execute("SELECT * FROM users")
            jumlah_user = len(c.fetchall())

            c.execute("SELECT * FROM products")
            jumlah_produk = len(c.fetchall())

            c.execute("SELECT * FROM orders")
            jumlah_order = len(c.fetchall())

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "Total User",
                    jumlah_user
                )

            with col2:
                st.metric(
                    "Total Produk",
                    jumlah_produk
                )

            with col3:
                st.metric(
                    "Total Pesanan",
                    jumlah_order
                )

        # ===========================
        # KELOLA PRODUK
        # ===========================
        elif menu_admin == "Kelola Produk":

            st.header("Kelola Produk")

        # ===========================
        # KELOLA PESANAN
        # ===========================
        elif menu_admin == "Kelola Pesanan":

            st.header("Kelola Pesanan")
