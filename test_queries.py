from neo4j_connector import Neo4jConnector
from typing import Dict, List
import json
from tabulate import tabulate

class KnowledgeGraphTester:
    def __init__(self):
        self.connector = Neo4jConnector()
        
    def print_results(self, title: str, results: List[Dict]):
        """Print results in a formatted table"""
        if not results:
            print(f"\n{title}: No results found")
            return
            
        print(f"\n{title}:")
        headers = results[0].keys()
        rows = [list(result.values()) for result in results]
        print(tabulate(rows, headers=headers, tablefmt="grid"))

    def test_countries(self):
        """Test: List all countries with their details"""
        query = """
        MATCH (c:Country)
        RETURN c.name as Country, 
               c.currency as Currency,
               c.language as Language,
               c.timezone as Timezone
        ORDER BY c.name
        """
        results = self.connector.execute_query(query)
        self.print_results("All Countries", results)

    def test_cities(self):
        """Test: List all cities with their country information"""
        query = """
        MATCH (city:City)-[:IN]->(country:Country)
        RETURN city.name as City,
               country.name as Country,
               city.population as Population,
               city.is_capital as Is_Capital
        ORDER BY country.name, city.name
        """
        results = self.connector.execute_query(query)
        self.print_results("All Cities", results)

    def test_visa_free_countries(self):
        """Test: List visa-free countries for Indian passport"""
        query = """
        MATCH (india:Country {name: 'India'})-[:VISA_FREE]->(country:Country)
        RETURN country.name as Country,
               country.currency as Currency,
               country.language as Language
        ORDER BY country.name
        """
        results = self.connector.execute_query(query)
        self.print_results("Visa-Free Countries for Indian Passport", results)

    def test_flight_routes(self):
        """Test: List all flight routes with costs"""
        query = """
        MATCH (from:City)-[:HAS_FLIGHT]->(flight:Flight)-[:TO]->(to:City)
        RETURN from.name as From,
               to.name as To,
               flight.airline as Airline,
               flight.cost as Cost,
               flight.duration as Duration_Minutes
        ORDER BY flight.cost
        """
        results = self.connector.execute_query(query)
        self.print_results("Flight Routes", results)

    def test_attractions(self):
        """Test: List all attractions with their details"""
        query = """
        MATCH (city:City)-[:HAS_ATTRACTION]->(attraction:Attraction)
        RETURN city.name as City,
               attraction.name as Attraction,
               attraction.type as Type,
               attraction.cost as Cost,
               attraction.rating as Rating
        ORDER BY attraction.rating DESC
        """
        results = self.connector.execute_query(query)
        self.print_results("Tourist Attractions", results)

    def test_budget_travel_options(self):
        """Test: Find budget travel options from Mumbai"""
        query = """
        MATCH (mumbai:City {name: 'Mumbai'})-[:HAS_FLIGHT]->(flight:Flight)-[:TO]->(dest:City)
        MATCH (dest)-[:HAS_ATTRACTION]->(attraction:Attraction)
        WITH dest, flight, attraction,
             flight.cost as flight_cost,
             attraction.cost as attraction_cost,
             flight.cost + attraction.cost as total_cost
        WHERE total_cost <= 20000
        RETURN dest.name as Destination,
               flight.airline as Airline,
               flight.cost as Flight_Cost,
               attraction.name as Attraction,
               attraction.cost as Attraction_Cost,
               total_cost as Total_Cost
        ORDER BY total_cost
        """
        results = self.connector.execute_query(query)
        self.print_results("Budget Travel Options from Mumbai (Under ₹20,000)", results)

    def test_visa_free_attractions(self):
        """Test: Find attractions in visa-free countries"""
        query = """
        MATCH (india:Country {name: 'India'})-[:VISA_FREE]->(country:Country)
        MATCH (city:City)-[:IN]->(country)
        MATCH (city)-[:HAS_ATTRACTION]->(attraction:Attraction)
        RETURN country.name as Country,
               city.name as City,
               attraction.name as Attraction,
               attraction.type as Type,
               attraction.cost as Cost,
               attraction.rating as Rating
        ORDER BY country.name, attraction.rating DESC
        """
        results = self.connector.execute_query(query)
        self.print_results("Attractions in Visa-Free Countries", results)

    def run_all_tests(self):
        """Run all test queries"""
        print("Running Knowledge Graph Tests...")
        print("=" * 50)
        
        self.test_countries()
        self.test_cities()
        self.test_visa_free_countries()
        self.test_flight_routes()
        self.test_attractions()
        self.test_budget_travel_options()
        self.test_visa_free_attractions()
        
        print("\nAll tests completed!")

if __name__ == "__main__":
    tester = KnowledgeGraphTester()
    tester.run_all_tests() 