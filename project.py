import explain
import interface

if __name__ == "__main__":
    # database=PostgresDB("CZ4031")
    nodeTypeList = []
    host, port, database, username, password, query, window = interface.GUI1().initialise_GUI1()
    database = explain.PostgresDB(host, port, database, username, password)
    queryExp = query
    query2 = queryExp
    query1 = "SELECT * FROM customer, orders  WHERE c_custkey = o_custkey"
    database.explainDifferences(query1, query2)
