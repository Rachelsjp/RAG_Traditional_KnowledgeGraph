from neo4j import GraphDatabase

# Connection details
uri = "bolt://127.0.0.1:7687"
username = "neo4j"
password = "your_neo4j_password"  # your password here

# Create driver
driver = GraphDatabase.driver(uri, auth=(username, password))

# Function to load graph data safely
def load_graph(tx):
    # Create Systems
    tx.run("MERGE (crm:System {name:'CRM System'})")
    tx.run("MERGE (erp:System {name:'ERP System'})")

    # Create Tables
    tx.run("MERGE (cust:Table {name:'dim_customer'})")
    tx.run("MERGE (orders:Table {name:'fact_orders'})")
    tx.run("MERGE (prod:Table {name:'dim_product'})")

    # Create Dashboards
    tx.run("MERGE (sales:Dashboard {name:'Sales Dashboard'})")
    tx.run("MERGE (rev:Dashboard {name:'Revenue Dashboard'})")
    tx.run("MERGE (inventory:Dashboard {name:'Inventory Dashboard'})")

    # Connect Systems → Tables
    tx.run("MATCH (crm:System {name:'CRM System'}), (cust:Table {name:'dim_customer'}) "
           "MERGE (crm)-[:FEEDS]->(cust)")
    tx.run("MATCH (erp:System {name:'ERP System'}), (orders:Table {name:'fact_orders'}) "
           "MERGE (erp)-[:FEEDS]->(orders)")

    # Connect Tables → Tables (dependencies)
    tx.run("MATCH (orders:Table {name:'fact_orders'}), (cust:Table {name:'dim_customer'}) "
           "MERGE (orders)-[:DEPENDS_ON]->(cust)")

    # Connect Tables → Dashboards
    tx.run("MATCH (orders:Table {name:'fact_orders'}), (sales:Dashboard {name:'Sales Dashboard'}) "
           "MERGE (orders)-[:USED_IN]->(sales)")
    tx.run("MATCH (orders:Table {name:'fact_orders'}), (rev:Dashboard {name:'Revenue Dashboard'}) "
           "MERGE (orders)-[:USED_IN]->(rev)")
    tx.run("MATCH (prod:Table {name:'dim_product'}), (inventory:Dashboard {name:'Inventory Dashboard'}) "
           "MERGE (prod)-[:USED_IN]->(inventory)")

# Execute graph loading
with driver.session() as session:
    session.execute_write(load_graph)

print("Graph data loaded successfully! ✅")

#Delete all existing nodes and relationships
#MATCH (n)
#DETACH DELETE n

#VISUALIZATION QUERY
#MATCH (n)-[r]->(m)
#RETURN DISTINCT n, r, m

#See all nodes with labels and properties
#MATCH (n)
#RETURN n, labels(n)

#See all relationships
#MATCH (a)-[r]->(b)
#RETURN a.name AS From, type(r) AS Relationship, b.name AS To

#to connect neo4j in browser
#RETURN 'Neo4j connected!' AS message