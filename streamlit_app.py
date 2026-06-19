import streamlit as st
import sqlite3

# =========================================
# KONFIGURASI
# =========================================
st.set_page_config(page_title="Premium Store", layout="wide")

# =========================================
# DATABASE
# =========================================
conn = sqlite3.connect("database.db", check_same_thread=False)
c = conn.cursor()

# Tabel user
c.execute("""
CREATE TABLE IF NOT EXISTS users(
id INTEGER PRIMARY KEY AUTOINCREMENT,
username TEXT UNIQUE,
password TEXT,
role TEXT
)
""")

# Tabel produk
c.execute("""
CREATE TABLE IF NOT EXISTS products(
id INTEGER PRIMARY KEY AUTOINCREMENT,
nama TEXT,
kategori TEXT,
durasi TEXT,
harga INTEGER
)
""")

# Tabel pesanan
c.execute("""
CREATE TABLE IF NOT EXISTS orders(
id INTEGER PRIMARY KEY AUTOINCREMENT,
username TEXT,
produk TEXT,
harga INTEGER,
status TEXT
)
""")

conn.commit()

# =========================================
# ADMIN DEFAULT
# =========================================
c.execute("SELECT * FROM users WHERE username=?", ("admin",))
admin = c.fetchone()

if admin is None:
    c.execute(
        "INSERT INTO users(username,password,role) VALUES(?,?,?)",
        ("admin", "admin123", "admin")
    )
    conn.commit()

# =========================================
# SESSION
# =========================================
if "login" not in st.session_state:
    st.session_state.login = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "role" not in st.session_state:
    st.session_state.role = ""

# =========================================
# MENU
# =========================================
menu = st.sidebar.selectbox(
    "Menu",
    ["Beranda", "Login", "Registrasi"]
)

# =========================================
# BERANDA
# =========================================
if menu == "Beranda":
    st.title("PREMIUM STORE")
    st.write("Selamat datang di layanan aplikasi premium.")

# =========================================
# REGISTRASI
# =========================================
elif menu == "Registrasi":

    st.title("Registrasi")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Daftar"):
        try:
            c.execute(
                "INSERT INTO users(username,password,role) VALUES(?,?,?)",
                (username, password, "user")
            )
            conn.commit()
            st.success("Registrasi berhasil")
        except:
            st.error("Username sudah digunakan")

# =========================================
# LOGIN
# =========================================
elif menu == "Login":

    st.title("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Masuk"):

        c.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, password)
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

# =========================================
# DASHBOARD SETELAH LOGIN
# =========================================
if st.session_state.login:

    st.sidebar.success(
        f"Login sebagai {st.session_state.username}"
    )

    if st.sidebar.button("Logout"):
        st.session_state.login = False
        st.session_state.username = ""
        st.session_state.role = ""
        st.rerun()

    # ======================
    # MENU USER
    # ======================
    if st.session_state.role == "user":

        pilih = st.sidebar.selectbox(
            "Menu User",
            ["Beranda User", "History Pembelian"]
        )

        if pilih == "Beranda User":

    st.header("Layanan Premium")

    c.execute("SELECT * FROM products")
    products = c.fetchall()

    if len(products) == 0:
        st.info("Belum ada produk.")
    else:

        col1, col2, col3 = st.columns(3)

        for i, p in enumerate(products):

            id_produk = p[0]
            nama = p[1]
            kategori = p[2]
            durasi = p[3]
            harga = p[4]

            with [col1, col2, col3][i % 3]:

                st.subheader(nama)
                st.write("Kategori :", kategori)
                st.write("Durasi :", durasi)
                st.write(f"Harga : Rp {harga:,}")

                if st.button(
                    f"Beli {nama}",
                    key=f"beli_{id_produk}"
                ):

                    c.execute(
                        """
                        INSERT INTO orders(username,produk,harga,status)
                        VALUES(?,?,?,?)
                        """,
                        (
                            st.session_state.username,
                            nama,
                            harga,
                            "Pending"
                        )
                    )

                    conn.commit()

                    st.success("Pesanan berhasil dibuat")

       elif pilih == "History Pembelian":

    st.header("History Pembelian")

    c.execute(
        "SELECT * FROM orders WHERE username=?",
        (st.session_state.username,)
    )

    orders = c.fetchall()

    if len(orders) == 0:
        st.info("Belum ada pembelian.")

    else:

        for o in orders:

            st.container(border=True)

            st.write("Produk :", o[2])
            st.write(f"Harga : Rp {o[3]:,}")
            st.write("Status :", o[4])

            st.divider()
    # ======================
    # MENU ADMIN
    # ======================
    elif st.session_state.role == "admin":

        pilih_admin = st.sidebar.selectbox(
            "Menu Admin",
            [
                "Dashboard",
                "Kelola Produk",
                "Kelola Pesanan"
            ]
        )

        if pilih_admin == "Dashboard":
            st.header("Dashboard Admin")

        elif pilih_admin == "Kelola Produk":

    st.header("Kelola Produk")

    tab1, tab2 = st.tabs(
        ["Tambah Produk", "Daftar Produk"]
    )

    # ====================
    # TAMBAH PRODUK
    # ====================
    with tab1:

        nama = st.text_input("Nama Produk")

        kategori = st.selectbox(
            "Kategori",
            [
                "Streaming",
                "Musik",
                "Editing",
                "AI",
                "Sosmed"
            ]
        )

        durasi = st.selectbox(
            "Durasi",
            [
                "1 Minggu",
                "1 Bulan",
                "3 Bulan",
                "6 Bulan",
                "1 Tahun"
            ]
        )

        harga = st.number_input(
            "Harga",
            min_value=0
        )

        if st.button("Tambah Produk"):

            c.execute(
                """
                INSERT INTO products(
                nama,kategori,durasi,harga)
                VALUES(?,?,?,?)
                """,
                (
                    nama,
                    kategori,
                    durasi,
                    harga
                )
            )

            conn.commit()

            st.success("Produk berhasil ditambahkan")

    # ====================
    # DAFTAR PRODUK
    # ====================
    with tab2:

        c.execute("SELECT * FROM products")
        data_produk = c.fetchall()

        for p in data_produk:

            with st.container(border=True):

                st.subheader(p[1])

                st.write("Kategori :", p[2])
                st.write("Durasi :", p[3])
                st.write(f"Harga : Rp {p[4]:,}")

                if st.button(
                    "Hapus",
                    key=f"hapus{p[0]}"
                ):

                    c.execute(
                        "DELETE FROM products WHERE id=?",
                        (p[0],)
                    )

                    conn.commit()

                    st.rerun()

        elif pilih_admin == "Kelola Pesanan":
            st.header("Kelola Pesanan")
