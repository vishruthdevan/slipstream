import pandas as pd
from sqlalchemy import create_engine, text

# Load the updated CSV
df = pd.read_csv("updated_data.csv")

# Set up your PostgreSQL connection
# Format: postgresql://username:password@host:port/database
engine = create_engine("postgresql://vpa2112:dosa123@34.148.223.31:5432/proj1part2")

# Open a connection
with engine.begin() as conn:
    for _, row in df.iterrows():
        if pd.isna(row["description"]):
            continue  # Skip if no description to update

        # Use parameterized query to avoid SQL injection
        query = text(
            """
            UPDATE circuit
            SET description = :description
            WHERE name = :name
        """
        )
        q = conn.execute(
            query, {"description": row["description"], "name": row["name"]}
        )

        if q.rowcount == 0:
            print(f"No match found for {row['name']}")
