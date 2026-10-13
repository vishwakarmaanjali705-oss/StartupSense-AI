import sqlite3
import hashlib
from datetime import datetime


# ============================================================
# DATABASE FILE
# ============================================================

DATABASE = "app.db"


# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_connection():
    return sqlite3.connect(DATABASE)


# ============================================================
# CREATE DATABASE TABLES
# ============================================================

def create_tables():

    conn = get_connection()
    cursor = conn.cursor()

    # --------------------------------------------------------
    # USERS TABLE
    # --------------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    # --------------------------------------------------------
    # ANALYSES TABLE
    # --------------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS analyses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_email TEXT NOT NULL,
            startup_name TEXT NOT NULL,
            description TEXT NOT NULL,
            industry TEXT,
            business_model TEXT,
            target_market TEXT,
            budget INTEGER,
            competition INTEGER,
            score INTEGER,
            potential TEXT,
            recommendation TEXT,
            recommendations TEXT,
            created_at TEXT
        )
    """)

    conn.commit()
    conn.close()


# ============================================================
# PASSWORD HASHING
# ============================================================

def hash_password(password):

    return hashlib.sha256(
        password.encode("utf-8")
    ).hexdigest()


# ============================================================
# CREATE ACCOUNT
# ============================================================

def create_account(username, email, password):

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute("""
            INSERT INTO users (
                username,
                email,
                password
            )
            VALUES (?, ?, ?)
        """, (
            username,
            email,
            hash_password(password)
        ))

        conn.commit()

        success = True

    except sqlite3.IntegrityError:

        success = False

    conn.close()

    return success


# ============================================================
# CHECK LOGIN
# ============================================================

def check_login(email, password):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT username
        FROM users
        WHERE email = ?
        AND password = ?
    """, (
        email,
        hash_password(password)
    ))

    user = cursor.fetchone()

    conn.close()

    return user


# ============================================================
# GET USER
# ============================================================

def get_user(email):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT username, email
        FROM users
        WHERE email = ?
    """, (email,))

    user = cursor.fetchone()

    conn.close()

    return user


# ============================================================
# UPDATE USERNAME
# ============================================================

def update_username(email, new_username):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE users
        SET username = ?
        WHERE email = ?
    """, (
        new_username,
        email
    ))

    conn.commit()
    conn.close()


# ============================================================
# CHANGE PASSWORD
# ============================================================

def change_password(
    email,
    old_password,
    new_password
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id
        FROM users
        WHERE email = ?
        AND password = ?
    """, (
        email,
        hash_password(old_password)
    ))

    user = cursor.fetchone()

    if not user:

        conn.close()
        return False

    cursor.execute("""
        UPDATE users
        SET password = ?
        WHERE email = ?
    """, (
        hash_password(new_password),
        email
    ))

    conn.commit()
    conn.close()

    return True


# ============================================================
# SAVE STARTUP ANALYSIS
# ============================================================

def save_analysis(
    email,
    startup_name,
    description,
    industry,
    business_model,
    target_market,
    budget,
    competition,
    score,
    potential,
    recommendation,
    recommendations
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO analyses (
            user_email,
            startup_name,
            description,
            industry,
            business_model,
            target_market,
            budget,
            competition,
            score,
            potential,
            recommendation,
            recommendations,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        email,
        startup_name,
        description,
        industry,
        business_model,
        target_market,
        budget,
        competition,
        score,
        potential,
        recommendation,
        "\n".join(recommendations),
        datetime.now().strftime(
            "%d %B %Y, %I:%M %p"
        )
    ))

    conn.commit()
    conn.close()


# ============================================================
# GET USER'S ANALYSIS HISTORY
# ============================================================

def get_history(email):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            startup_name,
            description,
            industry,
            business_model,
            target_market,
            budget,
            competition,
            score,
            potential,
            recommendation,
            recommendations,
            created_at
        FROM analyses
        WHERE user_email = ?
        ORDER BY id DESC
    """, (email,))

    history = cursor.fetchall()

    conn.close()

    return history


# ============================================================
# CREATE TABLES WHEN THIS FILE IS RUN
# ============================================================

create_tables()
