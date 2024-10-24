import csv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from alembic import script, config
import subprocess 
import re
from datetime import datetime , timezone
from dotenv import load_dotenv

load_dotenv()

def run_flask_db_revision(message="ticketnumber"):
    try:
        result = subprocess.run(["flask","db","revision","-m", message], check=True, capture_output=True, text=True)
        output = result.stdout
        match = re.search(r'Generating\s+([\S]+)', output)
        print (match.group(1))
        if match:
            migration_file=match.group(1)
            return migration_file
        print (migration_file)
        print(f"Alembic revision created")
    except subprocess.CalledProcessError as e:
        print(e)
    except Exception as e:
        print(e)

def fetch_record(engine, table_name, primary_key, key_value):
    query = text(f"SELECT * FROM {table_name} WHERE {primary_key} = :key_value")
    with engine.connect() as conn:
        result = conn.execute(query, key_value=key_value).fetchone()
    return dict(result) if result else None  
    
def fetch_column_types(engine, table_name):
    query = text(f"SELECT column_name, data_type FROM information_schema.columns WHERE table_name = :table_name")
    with engine.connect() as conn:
        result = conn.execute(query, table_name=table_name).fetchall()
    return {row['column_name']: row['data_type'] for row in result}

def to_naive_datetime(value):
    if isinstance(value, datetime):
        return value.replace(tzinfo=None)  
    try:
        return datetime.strptime(value.split('+')[0], '%Y-%m-%d %H:%M:%S')
    except ValueError:
        return value 
    
def values_are_different(db_value, csv_value, is_datetime_column=False):
    if db_value is None and (csv_value is None or csv_value == 'NULL'):
        return False
    if db_value is None or csv_value == 'NULL':
        return True
    if is_datetime_column:
        db_value = to_naive_datetime(db_value)
        csv_value = to_naive_datetime(csv_value)
        return db_value != csv_value  
    return str(db_value) != str(csv_value)

def generate_sql_commands_from_csv(csv_file, table_name, primary_key, engine):
    sql_commands = []
    rollback_commands = []
    column_types = fetch_column_types(engine, table_name)
    with open(csv_file, 'r', encoding='latin-1') as file:
        reader = csv.DictReader(file)
        sorted_rows = sorted(reader, key=lambda row: int(row[primary_key]))
        for row in sorted_rows:
            key_value = row[primary_key]
            print(key_value)

            existing_record = fetch_record(engine, table_name, primary_key, key_value)
            if existing_record:
                update_fields = []
                rollback_update_fields = []
                for col, new_value in row.items():
                    if col != primary_key:
                        db_value = existing_record[col] if existing_record[col] is not None else None
                        is_datetime_column = 'timestamp' in column_types[col].lower()
                        if values_are_different(db_value, new_value, is_datetime_column):
                            update_fields.append(f"{col} = '{new_value}'" if new_value != 'NULL' else f"{col} = NULL")
                            rollback_update_fields.append(f"{col} = '{db_value}'" if db_value is not None else f"{col} = NULL")
                if update_fields:
                    update_command = f"""op.execute(\"""UPDATE {table_name} SET {', '.join(update_fields)} WHERE {primary_key} = '{key_value}';\""")"""
                    sql_commands.append(update_command)
                    rollback_update_command = f"""op.execute(\"""UPDATE {table_name} SET {', '.join(rollback_update_fields)} WHERE {primary_key} = '{key_value}';\""")"""
                    rollback_commands.append(rollback_update_command)
            else:
                columns = ', '.join(row.keys())
                values = ', '.join([f"'{value}'" if value != 'NULL' else 'NULL' for value in row.values()])
                insert_command = f"""op.execute(\"""INSERT INTO {table_name} ({columns}) VALUES ({values});\""")"""
                sql_commands.append(insert_command)
                delete_command = f"""op.execute(\"""DELETE FROM {table_name} WHERE {primary_key} = '{key_value}';\""")"""
                rollback_commands.append(delete_command)
    return sql_commands, rollback_commands

def write_sql_to_migration(alembic_file, sql_commands, rollback_commands):
    with open(alembic_file, 'r+') as migration_file:
        lines = migration_file.readlines()
        migration_file.seek(0)
        for index, line in enumerate(lines):
            if line.strip().startswith('def upgrade'):
                lines.insert(index + 1, "\n    # Generated SQL commands for upgrade\n")
                for command in reversed(sql_commands):
                    lines.insert(index + 2, f"    {command}\n")
                break
        for index, line in enumerate(lines):
            if line.strip().startswith('def downgrade'):
                lines.insert(index + 1, "\n    # Generated SQL commands for downgrade (rollback)\n")
                for command in rollback_commands:
                    lines.insert(index + 2, f"    {command}\n")
                break
        migration_file.writelines(lines)

def seed_database(csv_file, table_name, primary_key, db_url):
    engine = create_engine(db_url)
    sql_commands, rollback_commands = generate_sql_commands_from_csv(csv_file, table_name, primary_key, engine)
    alembic_file = run_flask_db_revision() 
    write_sql_to_migration(alembic_file, sql_commands, rollback_commands)
    
    print(f"SQL commands written to {alembic_file}")

if __name__ == '__main__':
    
    csv_file = os.getenv('CSV_FILE')  
    table_name = os.getenv('TABLE_NAME')  
    primary_key = os.getenv('PRIMARY_KEY')  
    db_engine = os.getenv('DATABASE_ENGINE')  
    db_username = os.getenv('DATABASE_USERNAME')  
    db_password = os.getenv('DATABASE_PASSWORD')  
    db_name = os.getenv('DATABASE_NAME')  
    
    db_url = f"{db_engine}://{db_username}:{db_password}@localhost/{db_name}"

    seed_database(csv_file, table_name, primary_key, db_url)