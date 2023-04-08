from project import *


# def align_lists(list1, list2):
#     if list1[-1] == list2[-1]:
#         return list1, list2

#     i = len(list1) - 1
#     j = len(list2) - 1

#     while i >= 0 and j >= 0:
#         if list1[i] == list2[j]:
#         # matching element found
#             break
#         i -= 1
#         j -= 1

#         # adjust elements of smaller list
#     if i < j:
#         list1 = [''] * (j - i) + list1
#     elif j < i:
#         list2 = [''] * (i - j) + list2

#         # return aligned lists
#     return list1, list2


def getExplanation(self, queryresult):
    i = 0
    nodeTypeList = []
    for row in queryresult:
        if (i % 2 != 0):
            i = i + 1
            continue
        row_str = row[0]
        node_type, cost = row_str.split("(")[0].strip(), row_str.split("(")[1].split(")")[0]
        cost = cost[5:]
        costt = cost.split()[0]
        rows = cost.split()[1][5:]
        width = cost.split()[2][6:]
        if (i > 0):
            node_type = node_type[4:]
        nodeTypeList.append(node_type)
        print(f"Node Type: {node_type}, Cost: {costt}, Rows:{rows}, Width:{width}")
        i = i + 1
    print(f"Nodes list = {nodeTypeList}")
    return nodeTypeList


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


def queryDifferenceNew(self, query1, query2):
    # Use difflib to compare the queries
    query1_list = []
    query2_list = []
    clause_names = ["EXPLAIN SELECT", "FROM", "WHERE", "GROUP BY", "HAVING", "ORDER BY", "LIMIT"]
    query1_list = PostgresDB.split_query(query1, clause_names)
    print(query1_list)
    query2_list = PostgresDB.split_query(query2, clause_names)
    print(query2_list)

    for clause_name in clause_names:
        if clause_name in query1_list and clause_name in query2_list:
            if query1_list[clause_name] != query2_list[clause_name]:
                print(
                    f"Difference in {clause_name} clause: {query1_list[clause_name]} modified to {query2_list[clause_name]}")
        if clause_name in query1_list and clause_name not in query2_list:
            print(f"Clause {clause_name} removed in query2")
        if clause_name in query2_list and clause_name not in query1_list:
            print(f"Clause {clause_name} added in query2: {query2_list[clause_name]}")


def qepDifference(self, query1, query2):
    queryresult1 = self.fetchQueryResult(query1)
    queryresult2 = self.fetchQueryResult(query2)
    nodeTypeList1 = self.getExplanation(queryresult1)
    nodeTypeList2 = self.getExplanation(queryresult2)
    s = self.qepDifferenceHelper(nodeTypeList1, nodeTypeList2)
    # s,t = PostgresDB.align_lists(nodeTypeList1,nodeTypeList2)
    print(s)
    # print(t)


def qepDifferenceHelper(self, nodeTypeList1, nodeTypeList2):
    # Initialize result string
    result = ""
    # nodeTypeListNew1, nodeTypeListNew2 = PostgresDB.align_lists(nodeTypeList1, nodeTypeList2)
    nodeTypeList = nodeTypeList2 if len(nodeTypeList1) > len(nodeTypeList2) else nodeTypeList1

    # Iterate through the lists and compare each element
    for i in range(len(nodeTypeList)):
        # If the elements are different, add transition string to result
        if nodeTypeList1[i] != nodeTypeList2[i]:
            result += f"{nodeTypeList1[i]} transitions to {nodeTypeList2[i]}\n"

    # Return result string
    return result





