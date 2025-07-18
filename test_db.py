import sqlalchemy
from app.db.database import engine

try:
    # Attempt to connect to the database
    connection = engine.connect()
    print("Database connection successful!")
    
    # Optional: run a simple query to verify
    result = connection.execute(sqlalchemy.text("SELECT 1"))
    print("Test query successful. Result:", result.scalar())

    connection.close()
except Exception as e:
    print("Database connection failed.")
    print(f"Error: {e}")
