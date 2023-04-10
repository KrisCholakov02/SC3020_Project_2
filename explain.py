import psycopg2


class Node:
    def __init__(self, node_type, cost, rows, width):
        self.node_type = node_type
        self.cost = cost
        self.rows = rows
        self.width = width
        self.children = []

    def add_child(self, child_node):
        self.children.append(child_node)


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

    def queryDB(self, query):
        self.cursor.execute(
            f"EXPLAIN (FORMAT JSON) {'''{}'''}".format(query))
        return self.cursor.fetchall()[0][0][0]

    def split_query(query, clause_names):
        clause_positions = {}
        start_pos = 0

        # Find the position of each clause in the query string
        for clause_name in clause_names:
            clause_pos = query.lower().find(clause_name.lower(), start_pos)
            if clause_pos != -1:
                clause_positions[clause_name] = clause_pos
                start_pos = clause_pos

        # Extract each clause from the query string
        clause_values = {}
        for clause_name in clause_names:
            if clause_name in clause_positions:
                start_pos = clause_positions[clause_name] + len(clause_name)
                end_pos = len(query)
                for next_clause_name in clause_names:
                    if next_clause_name in clause_positions and clause_positions[next_clause_name] > start_pos:
                        end_pos = clause_positions[next_clause_name]
                        break
                clause_values[clause_name] = query[start_pos:end_pos].strip()

        return clause_values

    def queryDifference(self, query1, query2):
        # Use difflib to compare the queries

        query1_list = []
        query2_list = []
        clause_names = ["EXPLAIN SELECT", "FROM", "WHERE", "GROUP BY", "HAVING", "ORDER BY", "LIMIT"]
        query1_list = PostgresDB.split_query(query1, clause_names)
        # print(query1_list)
        query2_list = PostgresDB.split_query(query2, clause_names)
        # print(query2_list)
        counter = 1

        result = ""

        for clause_name in clause_names:
            if clause_name in query1_list and clause_name in query2_list:
                if query1_list[clause_name] != query2_list[clause_name]:
                    result += f"{counter}. Difference in {clause_name} clause: {query1_list[clause_name]} modified to {query2_list[clause_name]}\n"
                    counter = counter + 1
            if clause_name in query1_list and clause_name not in query2_list:
                result += f"{counter}. Clause {clause_name} removed in query2\n"
                counter = counter + 1
            if clause_name in query2_list and clause_name not in query1_list:
                result += f"{counter}. Clause {clause_name} added in query2: {query2_list[clause_name]}\n"
                counter = counter + 1
        return result

    def qepDifference(self, query1, query2):
        queryresult1 = self.queryDB(query1)
        queryresult2 = self.queryDB(query2)
        differences = []
        differences = self.compare_qep_trees(queryresult1["Plan"], queryresult2["Plan"])
        if len(differences) == 0:
            return "No change in qep"
        return differences

    def qepTreeGenerator(self, query1):
        queryresult1 = self.queryDB(query1)
        graph = {}
        graph = PostgresDB.create_graph(queryresult1["Plan"])
        return graph

    def create_graph(qep_json):
        graph = {}
        graph["name"] = qep_json["Node Type"]
        if "Plans" in qep_json:
            graph["children"] = [PostgresDB.create_graph(plan) for plan in qep_json["Plans"]]
        return graph

    def get_node_types(plan):
        node_types = [plan['Node Type']]
        if 'Plans' in plan:
            for subplan in plan['Plans']:
                node_types += PostgresDB.get_node_types(subplan)
        return node_types

    def compare_qep_trees(self, qep_tree1, qep_tree2):
        output = []

        # Define a DFS traversal function to traverse the QEP trees
        def dfs_traversal(node1, node2, path, counter):
            # Check if the nodes have the same node type
            if (node1['Node Type'] != node2['Node Type'] or node1.get('Join Type') != node2.get(
                    'Join Type') or node1.get('Hash Cond') != node2.get('Hash Cond')
                    or node1.get('Startup Cost') != node2.get('Startup Cost') or node1.get('Total Cost') != node2.get(
                        'Total Cost')):
                output.append(f"Difference {counter}\n")
            if node1['Node Type'] != node2['Node Type']:
                output.append(
                    f"Node Type: {node1['Node Type']} transitions to {node2['Node Type']}")

            # Check for other differences in the nodes
            if node1.get('Join Type') != node2.get('Join Type'):
                output.append(f"Join Type: {node1.get('Join Type')} tansitions to {node2.get('Join Type')}")
            if node1.get('Hash Cond') != node2.get('Hash Cond'):
                output.append(f"Hash Condition: {node1.get('Hash Cond')} transitions to {node2.get('Hash Cond')}")
            if node1.get('Startup Cost') != node2.get('Startup Cost'):
                output.append(f"Startup Cost: {node1.get('Startup Cost')} transitions to {node2.get('Startup Cost')}")
            if node1.get('Total Cost') != node2.get('Total Cost'):
                output.append(f"Total Cost: {node1.get('Total Cost')} transitions to {node2.get('Total Cost')}\n\n")
            # if node1.get('Plan Rows') != node2.get('Plan Rows'):
            #     output.append(f"{path}: Difference: Plan Rows ({node1.get('Plan Rows')} vs {node2.get('Plan Rows')})")
            # if node1.get('Plan Width') != node2.get('Plan Width'):
            #     output.append(f"{path}: Difference: Plan Width ({node1.get('Plan Width')} vs {node2.get('Plan Width')})")
            # if node1.get('Relation Name') != node2.get('Relation Name'):
            #     output.append(f"{path}: Difference: Relation Name ({node1.get('Relation Name')} vs {node2.get('Relation Name')})")
            # if node1.get('Alias') != node2.get('Alias'):
            #     output.append(f"{path}: Difference: Alias ({node1.get('Alias')} vs {node2.get('Alias')})")

            # Recursively traverse the child nodes
            if 'Plans' in node1 and 'Plans' in node2:
                for i in range(min(len(node1['Plans']), len(node2['Plans']))):
                    counter = counter + 1
                    dfs_traversal(node1['Plans'][i], node2['Plans'][i], f"{path} -> Plans[{i}]", counter)

        # Start the DFS traversal from the root nodes
        dfs_traversal(qep_tree1, qep_tree2, "Node Type: Root", 1)

        # Return the output
        return "\n".join(output)

    def explain_differences(self, query1, query2):
        if query1 == query2:
            return "Queries are same"
        string = "From the above dictionary, comparing the corresponding nodes, we conclude the below differences:\n"
        string += self.qepDifference(query1, query2)
        string += "\nThese differences in the qep were made because of: \n"
        string += self.queryDifference(query1, query2)
        return string
