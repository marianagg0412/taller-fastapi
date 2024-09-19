import numpy as np
import pandas as pd

df = pd.read_csv('calendar.csv')
# df.head()

#Dropped column that was filled with NaNs
df = df.drop("adjusted_price", axis="columns")

#Dropped rows with NaNs
df = df.dropna()

def write_inserts_to_file(df, table_name, file_name='inserts.sql', limit=2000):
    try:
        # Open the file in write mode
        with open(file_name, 'w') as f:
            # Limit to the first 2000 rows
            for index, row in df.head(limit).iterrows():
                # Construct an SQL statement with correct data typing
                f.write(f"INSERT INTO {table_name} (listing_id, date, available, price, minimum_nights, maximum_nights) VALUES (")
                f.write(f"{row['listing_id']}, ")
                f.write(f"'{row['date']}', ")
                f.write(f"'{row['available']}', ")
                f.write(f"{row['price'].replace('$', '').replace(',', '') if pd.notna(row['price']) else 'NULL'}, ")
                f.write(f"{int(row['minimum_nights'])}, ")
                f.write(f"{int(row['maximum_nights'])});\n")
        print(f"SQL insert statements have been written to {file_name}\n")
    except Exception as e:
        print(f"An error occurred while writing the SQL file: {str(e)}")

write_inserts_to_file(df, 'calendar', 'inserts.sql', 2000)