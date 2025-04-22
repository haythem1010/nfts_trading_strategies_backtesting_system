import psycopg2
from sshtunnel import SSHTunnelForwarder

from utils.consts import SQL_DB_CONFIG, SQL_DB_CONFIG_LOCAL, SSH_HOST
from utils.helpers import get_ip_address



def concat_addresses(addresses_list):
    strin = ''
    for a in addresses_list:
        strin += f"'{a}',"
    return strin[:-1]


class SQLUtils(object):
    @staticmethod
    def create_connection_ssh():
        try:
            server = SSHTunnelForwarder((SSH_HOST.HOST, SSH_HOST.PORT),
                                        ssh_username=SSH_HOST.USER,
                                        ssh_password=SSH_HOST.PWD,
                                        remote_bind_address=('localhost', 5432),
                                        local_bind_address=('localhost', 3307))
            server.start()

            import psycopg2
            conn = psycopg2.connect(
                database=SQL_DB_CONFIG_LOCAL.NAME,
                user=SQL_DB_CONFIG_LOCAL.USER,
                host=server.local_bind_host,
                port=server.local_bind_port,
                password=SQL_DB_CONFIG_LOCAL.PWD)
            return conn
        except Exception as e:
            print(e)

    @staticmethod
    def create_connection():
        try:
            return psycopg2.connect(
                "host=" + SQL_DB_CONFIG.HOST +
                " dbname=" + SQL_DB_CONFIG.NAME + " user=" + SQL_DB_CONFIG.USER + " password=" + SQL_DB_CONFIG.PWD
                + " port=" + SQL_DB_CONFIG.PORT)
        except Exception as e:
            print(e)

    def execute_query(self, query, ssh=False):
        try:
            if ssh:
                conn = self.create_connection_ssh()
            else:
                conn = self.create_connection()
            curr = conn.cursor()
            curr.execute(query)
            records = curr.fetchall()
            conn.close()
        except Exception as e:
            records = []
            print("Error", e)
            print("in query: ", query)
        return records

    def execute_non_select(self, query, ssh=False):
        try:
            if ssh:
                conn = self.create_connection_ssh()
            else:
                conn = self.create_connection()
            cur = conn.cursor()
            cur.execute(query)
            conn.commit()
            conn.close()
        except Exception as e:
            print("Error", e)
            print("in query: ", query)

    @staticmethod
    def set_ssh_by_ip():
        my_ip = get_ip_address()
        ssh = my_ip != "41.231.229.216"
        return ssh


