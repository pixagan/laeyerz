class DataConnections:

    def __init__(self, node_id):
        self.node = node_id
        self.connections = []

    def add_connection(self, connection):
        self.connections.append(connection)

    def get_connections(self):
        return self.connections

    def get_connection(self, id):
        return self.connections[id]