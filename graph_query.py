from neo4j import GraphDatabase

uri = "bolt://localhost:7687"
username = "neo4j"
password = "your_neo4j_password"

driver = GraphDatabase.driver(uri, auth=(username, password))


def find_dashboards(table_name):
    query = """
    MATCH (t:Table {name:$table})-[:USED_IN]->(d:Dashboard)
    RETURN DISTINCT d.name AS result
    """
    with driver.session() as session:
        result = session.run(query, table=table_name)
        return [r["result"] for r in result]


def find_dependencies(table_name):
    query = """
    MATCH (t:Table {name:$table})-[:DEPENDS_ON]->(d:Table)
    RETURN DISTINCT d.name AS result
    """
    with driver.session() as session:
        result = session.run(query, table=table_name)
        return [r["result"] for r in result]


def find_source_system(table_name):
    query = """
    MATCH (s:System)-[:FEEDS]->(t:Table {name:$table})
    RETURN DISTINCT s.name AS result
    """
    with driver.session() as session:
        result = session.run(query, table=table_name)
        return [r["result"] for r in result]
