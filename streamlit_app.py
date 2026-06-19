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
# ======================================================
# FITUR USER
# ======================================================
if st.session_state.login and st.session_state.role == "user":

    # ======================================
    # BERANDA USER
    # ======================================
    if menu_user == "Beranda User":

        st.title("👑 Layanan Premium")

        cari = st.text_input("Cari Produk")

        kategori_filter = st.selectbox(
            "Kategori",
            [
                "Semua",
                "Streaming",
                "Musik",
                "Editing",
                "AI",
                "Sosmed"
            ]
        )

        c.execute("SELECT * FROM products")
        products = c.fetchall()

        hasil = []

        for p in products:

            nama = p[1]
            kategori = p[2]

            cocok_nama = cari.lower() in nama.lower()

            cocok_kategori = (
                kategori_filter == "Semua"
                or kategori_filter == kategori
            )

            if cocok_nama and cocok_kategori:
                hasil.append(p)

        col1, col2, col3 = st.columns(3)

        for i, p in enumerate(hasil):

            with [col1, col2, col3][i % 3]:

                with st.container(border=True):

                    st.subheader(p[1])

                    if p[5] != "":

                        lokasi = "uploads/" + p[5]

                        if os.path.exists(lokasi):
                            st.image(lokasi)

                    st.write("Kategori :", p[2])
                    st.write("Durasi :", p[3])
                    st.write(f"Harga : Rp {p[4]:,}")

                    bukti = st.file_uploader(
                        "Upload Bukti Transfer",
                        type=["jpg", "png", "jpeg"],
                        key=f"file{i}"
                    )

                    if st.button(
                            "Beli",
                            key=f"beli{i}"):

                        nama_bukti = ""

                        if bukti is not None:

                            nama_bukti = (
                                st.session_state.username
                                + "_"
                                + bukti.name
                            )

                            with open(
                                    os.path.join(
                                        "uploads",
                                        nama_bukti),
                                    "wb"
                            ) as f:
                                f.write(
                                    bukti.getbuffer()
                                )

                        c.execute(
                            """
                            INSERT INTO orders
                            (
                            username,
                            produk,
                            harga,
                            status,
                            bukti
                            )
                            VALUES(?,?,?,?,?)
                            """,
                            (
                                st.session_state.username,
                                p[1],
                                p[4],
                                "Pending",
                                nama_bukti
                            )
                        )

                        conn.commit()

                        st.success(
                            "Pesanan berhasil dibuat"
                        )

    # ======================================
    # HISTORY PEMBELIAN
    # ======================================
    elif menu_user == "History Pembelian":

        st.title("History Pembelian")

        c.execute(
            """
            SELECT * FROM orders
            WHERE username=?
            """,
            (
                st.session_state.username,
            )
        )

        data_order = c.fetchall()

        if len(data_order) == 0:

            st.info("Belum ada pembelian")

        else:

            for o in data_order:

                with st.container(border=True):

                    st.subheader(o[2])

                    st.write(
                        f"Harga : Rp {o[3]:,}"
                    )

                    st.write(
                        "Status :", o[4]
                    )

# ======================================================
# FITUR ADMIN
# ======================================================
if st.session_state.login and st.session_state.role == "admin":

    # ======================================
    # KELOLA PRODUK
    # ======================================
    if menu_admin == "Kelola Produk":

        st.title("Kelola Produk")

        tab1, tab2 = st.tabs(
            [
                "Tambah Produk",
                "Daftar Produk"
            ]
        )

        # ==================================
        # TAMBAH PRODUK
        # ==================================
        with tab1:

            nama = st.text_input(
                "Nama Produk"
            )

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

            gambar = st.file_uploader(
                "Upload Gambar",
                type=["jpg", "png", "jpeg"]
            )

            if st.button("Tambah Produk"):

                nama_file = ""

                if gambar is not None:

                    nama_file = gambar.name

                    with open(
                            os.path.join(
                                "uploads",
                                nama_file),
                            "wb"
                    ) as f:
                        f.write(
                            gambar.getbuffer()
                        )

                c.execute(
                    """
                    INSERT INTO products
                    (
                    nama,
                    kategori,
                    durasi,
                    harga,
                    gambar
                    )
                    VALUES(?,?,?,?,?)
                    """,
                    (
                        nama,
                        kategori,
                        durasi,
                        harga,
                        nama_file
                    )
                )

                conn.commit()

                st.success(
                    "Produk berhasil ditambahkan"
                )

        # ==================================
        # DAFTAR PRODUK
        # ==================================
        with tab2:

            c.execute(
                "SELECT * FROM products"
            )

            produk = c.fetchall()

            for p in produk:

                with st.container(border=True):

                    st.subheader(p[1])

                    if p[5] != "":

                        lokasi = "uploads/" + p[5]

                        if os.path.exists(lokasi):
                            st.image(
                                lokasi,
                                width=200
                            )

                    st.write("Kategori :", p[2])
                    st.write("Durasi :", p[3])
                    st.write(
                        f"Harga : Rp {p[4]:,}"
                    )

                    if st.button(
                            "Hapus",
                            key=f"hapus{p[0]}"):

                        c.execute(
                            """
                            DELETE FROM products
                            WHERE id=?
                            """,
                            (
                                p[0],
                            )
                        )

                        conn.commit()

                        st.rerun()

    # ======================================
    # KELOLA PESANAN
    # ======================================
    elif menu_admin == "Kelola Pesanan":

        st.title("Kelola Pesanan")

        c.execute(
            "SELECT * FROM orders"
        )

        semua_order = c.fetchall()

        for o in semua_order:

            with st.container(border=True):

                st.subheader(o[2])

                st.write(
                    "Pembeli :",
                    o[1]
                )

                st.write(
                    f"Harga : Rp {o[3]:,}"
                )

                if o[5] != "":

                    lokasi = "uploads/" + o[5]

                    if os.path.exists(lokasi):

                        st.image(
                            lokasi,
                            width=250
                        )

                status = st.selectbox(
                    "Status",
                    [
                        "Pending",
                        "Diproses",
                        "Selesai"
                    ],
                    index=[
                        "Pending",
                        "Diproses",
                        "Selesai"
                    ].index(o[4]),
                    key=f"status{o[0]}"
                )

                if st.button(
                        "Update Status",
                        key=f"update{o[0]}"):

                    c.execute(
                        """
                        UPDATE orders
                        SET status=?
                        WHERE id=?
                        """,
                        (
                            status,
                            o[0]
                        )
                    )

                    conn.commit()

                    st.success(
                        "Status berhasil diubah"
                    )
