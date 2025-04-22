import psycopg2
from utils.consts import  SQL_DB_CONFIG_LOCAL, DATABASE_CONFIG, SSH_CONFIG
from sshtunnel import SSHTunnelForwarder


class DatabaseConnection(object):
    @staticmethod
    def create_connection():
        # Set up SSH tunnel
        with SSHTunnelForwarder(
                (SSH_CONFIG.HOST, 3307),
                ssh_username=SSH_CONFIG.USER,
                ssh_password=SSH_CONFIG.PWD,
                remote_bind_address=(SQL_DB_CONFIG_LOCAL.HOST, 5432)
        ) as tunnel:
            # Connect to PostgreSQL database
            conn = psycopg2.connect(
                database=DATABASE_CONFIG.NAME,
                user=DATABASE_CONFIG.USER,
                password=DATABASE_CONFIG.PWD,
                host=tunnel.HOST,
                port=tunnel.PORT
            )

            # Execute SQL query
            cur = conn.cursor()
            cur.execute('SELECT collection FROM transaction_stat GROUP BY 1')
            rows = cur.fetchall()
            for row in rows:
                print(row)

            # Close database connection
            conn.close()


db_ssh = DatabaseConnection()

db_ssh.create_connection()