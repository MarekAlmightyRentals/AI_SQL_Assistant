from db import get_engine, reflect_db

def test_connection():
    try:
        engine = get_engine()
        conn = engine.connect()
        print("✅ Connected to MSSQL database successfully!")
        conn.close()
    except Exception as e:
        print(f"❌ Failed to connect to database: {e}")

def test_schema_reflection():
    try:
        tables = reflect_db()
        print(f"✅ Tables found: {list(tables)}")
    except Exception as e:
        print(f"❌ Schema reflection failed: {e}")

if __name__ == "__main__":
    test_connection()
    test_schema_reflection()
