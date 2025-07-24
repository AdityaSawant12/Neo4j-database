import os
import sys
from dotenv import load_dotenv
from init_graph import KnowledgeGraphInitializer

def main():
    # Load environment variables
    load_dotenv()
    
    # Check if Neo4j credentials are set
    required_env_vars = ['NEO4J_URI', 'NEO4J_USER', 'NEO4J_PASSWORD']
    missing_vars = [var for var in required_env_vars if not os.getenv(var)]
    
    if missing_vars:
        print("Error: Missing required environment variables:")
        for var in missing_vars:
            print(f"- {var}")
        print("\nPlease set these variables in your .env file")
        sys.exit(1)
    
    try:
        # Initialize the knowledge graph
        initializer = KnowledgeGraphInitializer()
        initializer.initialize()
        
        print("\nKnowledge graph has been successfully initialized!")
        print("You can now use the travel planning system.")
        
    except Exception as e:
        print(f"Error during initialization: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 