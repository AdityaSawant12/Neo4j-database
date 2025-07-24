from neo4j_connector import Neo4jConnector
from typing import List, Dict
import json
import os

class KnowledgeGraphInitializer:
    def __init__(self):
        self.connector = Neo4jConnector()
        
    def clear_database(self):
        """Clear all existing data from the database"""
        query = """
        MATCH (n)
        DETACH DELETE n
        """
        self.connector.execute_query(query)
        print("Database cleared successfully")

    def create_constraints(self):
        """Create database constraints"""
        constraints = [
            "CREATE CONSTRAINT country_name IF NOT EXISTS FOR (c:Country) REQUIRE c.name IS UNIQUE",
            "CREATE CONSTRAINT city_name IF NOT EXISTS FOR (c:City) REQUIRE c.name IS UNIQUE",
            "CREATE CONSTRAINT attraction_name IF NOT EXISTS FOR (a:Attraction) REQUIRE a.name IS UNIQUE"
        ]
        
        for constraint in constraints:
            try:
                self.connector.execute_query(constraint)
            except Exception as e:
                print(f"Error creating constraint: {str(e)}")

    def create_countries(self):
        """Create country nodes with basic information"""
        countries = [
            {
                "name": "India",
                "currency": "INR",
                "language": "Hindi",
                "timezone": "IST"
            },
            {
                "name": "Thailand",
                "currency": "THB",
                "language": "Thai",
                "timezone": "ICT"
            },
            {
                "name": "Singapore",
                "currency": "SGD",
                "language": "English",
                "timezone": "SGT"
            },
            {
                "name": "Malaysia",
                "currency": "MYR",
                "language": "Malay",
                "timezone": "MYT"
            }
        ]
        
        query = """
        UNWIND $countries as country
        CREATE (c:Country {
            name: country.name,
            currency: country.currency,
            language: country.language,
            timezone: country.timezone
        })
        """
        self.connector.execute_query(query, {"countries": countries})

    def create_cities(self):
        """Create city nodes and connect them to countries"""
        cities = [
            {
                "name": "Mumbai",
                "country": "India",
                "population": 12478447,
                "is_capital": False
            },
            {
                "name": "Delhi",
                "country": "India",
                "population": 16787941,
                "is_capital": True
            },
            {
                "name": "Bangkok",
                "country": "Thailand",
                "population": 8280925,
                "is_capital": True
            },
            {
                "name": "Singapore",
                "country": "Singapore",
                "population": 5685807,
                "is_capital": True
            }
        ]
        
        query = """
        UNWIND $cities as city
        MATCH (country:Country {name: city.country})
        CREATE (c:City {
            name: city.name,
            population: city.population,
            is_capital: city.is_capital
        })
        CREATE (c)-[:IN]->(country)
        """
        self.connector.execute_query(query, {"cities": cities})

    def create_visa_requirements(self):
        """Create visa requirements between countries"""
        visa_free = [
            ("India", "Thailand"),
            ("India", "Singapore"),
            ("India", "Malaysia")
        ]
        
        query = """
        UNWIND $visa_free as pair
        MATCH (c1:Country {name: pair[0]})
        MATCH (c2:Country {name: pair[1]})
        CREATE (c1)-[:VISA_FREE]->(c2)
        """
        self.connector.execute_query(query, {"visa_free": visa_free})

    def create_flights(self):
        """Create flight connections between cities"""
        flights = [
            {
                "from": "Mumbai",
                "to": "Bangkok",
                "airline": "Air India",
                "cost": 15000,
                "duration": 240  # minutes
            },
            {
                "from": "Delhi",
                "to": "Singapore",
                "airline": "Singapore Airlines",
                "cost": 20000,
                "duration": 360
            },
            {
                "from": "Mumbai",
                "to": "Singapore",
                "airline": "Air India",
                "cost": 18000,
                "duration": 300
            }
        ]
        
        query = """
        UNWIND $flights as flight
        MATCH (from:City {name: flight.from})
        MATCH (to:City {name: flight.to})
        CREATE (f:Flight {
            airline: flight.airline,
            cost: flight.cost,
            duration: flight.duration
        })
        CREATE (from)-[:HAS_FLIGHT]->(f)
        CREATE (f)-[:TO]->(to)
        """
        self.connector.execute_query(query, {"flights": flights})

    def create_attractions(self):
        """Create tourist attractions and connect them to cities"""
        attractions = [
            {
                "name": "Taj Mahal",
                "city": "Delhi",
                "type": "Historical",
                "cost": 1000,
                "rating": 4.8
            },
            {
                "name": "Marina Bay Sands",
                "city": "Singapore",
                "type": "Modern",
                "cost": 2000,
                "rating": 4.7
            },
            {
                "name": "Grand Palace",
                "city": "Bangkok",
                "type": "Historical",
                "cost": 500,
                "rating": 4.6
            }
        ]
        
        query = """
        UNWIND $attractions as attraction
        MATCH (city:City {name: attraction.city})
        CREATE (a:Attraction {
            name: attraction.name,
            type: attraction.type,
            cost: attraction.cost,
            rating: attraction.rating
        })
        CREATE (city)-[:HAS_ATTRACTION]->(a)
        """
        self.connector.execute_query(query, {"attractions": attractions})

    def initialize(self):
        """Initialize the complete knowledge graph"""
        print("Starting knowledge graph initialization...")
        
        # Clear existing data
        self.clear_database()
        
        # Create constraints
        self.create_constraints()
        
        # Create nodes and relationships
        self.create_countries()
        self.create_cities()
        self.create_visa_requirements()
        self.create_flights()
        self.create_attractions()
        
        print("Knowledge graph initialization completed successfully!")

if __name__ == "__main__":
    initializer = KnowledgeGraphInitializer()
    initializer.initialize() 