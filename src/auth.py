import os
import bcrypt
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DATABASE_URL)

def init_auth_db():
    """Create users table and update portfolio table."""
    with engine.connect() as conn:
        # Create users table
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """))

        # Add user_id to portfolio if it doesn't exist
        conn.execute(text("""
            DO $$
            BEGIN
                IF NOT EXISTS (
                    SELECT 1 FROM information_schema.columns
                    WHERE table_name='portfolio' AND column_name='user_id'
                ) THEN
                    ALTER TABLE portfolio ADD COLUMN user_id INTEGER REFERENCES users(id);
                END IF;
            END $$;
        """))

        # Update primary key to be ticker + user_id
        conn.execute(text("""
            DO $$
            BEGIN
                IF EXISTS (
                    SELECT 1 FROM information_schema.table_constraints
                    WHERE constraint_name='portfolio_pkey'
                ) THEN
                    ALTER TABLE portfolio DROP CONSTRAINT portfolio_pkey;
                    ALTER TABLE portfolio ADD PRIMARY KEY (ticker, user_id);
                END IF;
            END $$;
        """))

        conn.commit()

def register_user(username, password):
    """Register a new user. Returns (success, message)."""
    init_auth_db()
    try:
        password_hash = bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")

        with engine.connect() as conn:
            conn.execute(text("""
                INSERT INTO users (username, password_hash)
                VALUES (:username, :password_hash)
            """), {"username": username.lower().strip(), "password_hash": password_hash})
            conn.commit()
        return True, "Account created successfully!"
    except Exception as e:
        if "unique" in str(e).lower():
            return False, "Username already taken."
        return False, f"Error: {str(e)}"

def login_user(username, password):
    """Verify login credentials. Returns (success, user_id, message)."""
    init_auth_db()
    try:
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT id, password_hash FROM users
                WHERE username = :username
            """), {"username": username.lower().strip()})
            row = result.fetchone()

        if not row:
            return False, None, "Username not found."

        user_id, password_hash = row
        if bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8")):
            return True, user_id, "Login successful!"
        else:
            return False, None, "Incorrect password."
    except Exception as e:
        return False, None, f"Error: {str(e)}"