from neo4j import GraphDatabase

# -----------------------------
# Step 1 — Connection details
# -----------------------------
uri = "bolt://127.0.0.1:7687"
username = "neo4j"
password = "*****"  # 🔁 replace with your password

# -----------------------------
# Step 2 — Create driver
# -----------------------------
driver = GraphDatabase.driver(uri, auth=(username, password))

# -----------------------------
# Step 3 — Test connection
# -----------------------------
try:
    with driver.session() as session:
        session.run("RETURN 1")
    print("✅ Neo4j connection successful")
except Exception as e:
    print("❌ Neo4j connection failed:", e)


# -----------------------------
# Step 4 — Query Functions
# -----------------------------
def find_dashboards(table_name):
    print(f"🔍 Finding dashboards for: {table_name}")

    query = """
    MATCH (t:Table {name:$table})-[:USED_IN]->(d:Dashboard)
    RETURN DISTINCT d.name AS result
    """

    with driver.session() as session:
        result = session.run(query, table=table_name)
        return [r["result"] for r in result]


def find_dependencies(table_name):
    print(f"🔍 Finding dependencies for: {table_name}")

    query = """
    MATCH (t:Table {name:$table})-[:DEPENDS_ON]->(d:Table)
    RETURN DISTINCT d.name AS result
    """

    with driver.session() as session:
        result = session.run(query, table=table_name)
        return [r["result"] for r in result]


def find_source_system(table_name):
    print(f"🔍 Finding source system for: {table_name}")

    query = """
    MATCH (s:System)-[:FEEDS]->(t:Table {name:$table})
    RETURN DISTINCT s.name AS result
    """

    with driver.session() as session:
        result = session.run(query, table=table_name)
        return [r["result"] for r in result]