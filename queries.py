from mysql import connector
from config import database


class MySQL:
    def __init__(self):
        self.params = database['mysql']
        self.connection = None

    def create(self, table: str, **values):
        if table is None:
            raise Exception('table key not found')
        columns = ", ".join(f"{column} {c_type}" for column, c_type in values.items())
        return self.execute(command=f"CREATE TABLE IF NOT EXISTS `{table}` ({columns})")

    def select(self, table, **params):
        args = []
        if "what" not in params.keys():
            what = "*"
        else:
            if isinstance(params['what'], str):
                params['what'] = [params['what']]
            if not any([column in params['what'] for column in ['AS', 'COUNT(*) as count', 'SUM']]):
                what = ", ".join(f"`{column}`" for column in params['what'])
            else:
                what = ", ".join(f"{column}" for column in params['what'])

        command = f"SELECT {what} FROM `{table}` "
        if "condition" in params.keys():
            command += f" WHERE "
            for item, value in params['condition'].items():
                if not any([operator in str(value) for operator in ['<','>','<>','!']]):
                    command += f" `{item}` = %s AND"
                    args.append(value)
                else:
                    command += f" `{item}` {value}"

            command = command[:-3] if command.endswith('AND') else command

        if "order" in params.keys():
            command += f" ORDER {params['order']}"

        if "limit" in params.keys():
            command += f" LIMIT {params['limit']}"

        if "one" in params.keys():
            return self.execute(command, args, select=False, one=True)
        else:
            return self.execute(command, args, select=True)

    def insert(self, **kwargs):
        table = kwargs['table']
        columns = ", ".join(f"`{column}`" for column in kwargs['columns'])
        values = ", ".join("%s" for _ in kwargs['values'])
        command = f"INSERT INTO `{table}` ({columns}) VALUES ({values});"
        return self.execute(command, arguments=[argument for argument in kwargs['values']])

    def update(self, **kwargs):
        table = kwargs['table']
        columns = ", ".join(f'`{column}` = "{value}"' for column, value in kwargs['params']['columns'].items())
        condition = " AND ".join(f'`{column}` = "{value}"' for column, value in kwargs['params']['condition'].items())
        command = f"UPDATE `{table}` SET {columns} WHERE {condition};"
        return self.execute(command)

    def insertOrUpdate(self, **kwargs):
        isExist = self.select(table=kwargs['table'], **kwargs['params']['columns'], condition=kwargs['params']['condition'])
        if isExist:
            self.update(table=kwargs['table'], params=kwargs['params'])
        else:
            self.insert(table=kwargs['table'], columns=list(kwargs['params']['columns'].keys()), values=list(kwargs['params']['columns'].values()))

    def connect(self):
        self.connection = connector.connect(**self.params)
        return self.connection

    def execute(self, command, arguments: tuple or list = (), select=False, one=False):
        self.connection = self.connect()
        with self.connection.cursor(buffered=True, dictionary=True) as cursor:
            cursor.execute(command, (*arguments,))
            self.connection.commit()
            self.connection.close()
        if select:
            data = cursor.fetchall()
            self.connection.close()
            return data
        elif one:
            data = cursor.fetchone()
            self.connection.close()
            return data


db = MySQL()
