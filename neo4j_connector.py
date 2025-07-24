from neo4j import GraphDatabase
from typing import Dict, List, Any
import os
from dotenv import load_dotenv

load_dotenv()

class Neo4jConnector:
    def __init__(self):
        self.uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
        self.user = os.getenv("NEO4J_USER", "neo4j")
        self.password = os.getenv("NEO4J_PASSWORD", "password")
        self.driver = None

    def connect(self):
        """Establish connection to Neo4j database"""
        try:
            self.driver = GraphDatabase.driver(
                self.uri,
                auth=(self.user, self.password)
            )
            return True
        except Exception as e:
            print(f"Failed to connect to Neo4j: {str(e)}")
            return False

    def close(self):
        """Close the database connection"""
        if self.driver:
            self.driver.close()

    def execute_query(self, query: str, params: Dict = None) -> List[Dict[str, Any]]:
        """Execute a Cypher query and return results"""
        if not self.driver:
            self.connect()
        
        try:
            with self.driver.session() as session:
                result = session.run(query, params or {})
                return [dict(record) for record in result]
        except Exception as e:
            print(f"Query execution failed: {str(e)}")
            return []

    def get_visa_free_countries(self, passport_country: str) -> List[str]:
        """Get list of visa-free countries for a given passport"""
        query = """
        MATCH (c:Country {name: $passport_country})-[:VISA_FREE]->(dest:Country)
        RETURN dest.name as country_name
        """
        results = self.execute_query(query, {"passport_country": passport_country})
        return [r["country_name"] for r in results]

    def get_flight_costs(self, origin: str, destination: str) -> List[Dict]:
        """Get flight costs between two locations"""
        query = """
        MATCH (o:City {name: $origin})-[:HAS_FLIGHT]->(f:Flight)-[:TO]->(d:City {name: $destination})
        RETURN f.airline as airline, f.cost as cost, f.duration as duration
        ORDER BY f.cost ASC
        """
        return self.execute_query(query, {"origin": origin, "destination": destination}) 