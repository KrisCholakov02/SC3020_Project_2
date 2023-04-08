import psycopg2
import interface

class PostgresDB:

    # Build connection between Postgres and Python
    def __init__(self, host, port, database, username, password):
        # Connect to an existing database
        self.connection = psycopg2.connect(host=host, port=port, database=database, user=username, password=password)

        # Create a cursor to perform database operations
        self.cursor = self.connection.cursor()

    def fetchQueryResult(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchall()


if __name__ == "__main__":
    # database=PostgresDB("CZ4031")
    nodeTypeList = []
    host, port, database, username, password, query, window = interface.GUI1().initialise_GUI1()
    database = PostgresDB(host, port, database, username, password)
    queryExp = "EXPLAIN " + query
    # queryresult1 = database.fetchQueryResult(queryExp)
    # nodeTypeList1 = database.getExplanation(queryresult1)
    # print(nodeTypeList1)

    query2 = queryExp
    query1 = "EXPLAIN SELECT * FROM customer, orders  WHERE c_custkey = o_custkey"

    # queryresult2 = database.fetchQueryResult(query2)
    # nodeTypeList2 = database.getExplanation(queryresult2)
    database.queryDifferenceNew(query1, query2)
    database.qepDifference(query1, query2)


