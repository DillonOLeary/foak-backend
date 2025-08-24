"""
Test script to verify database connection and tools.
"""

import asyncio
import os
from dotenv import load_dotenv

from app.database import db_manager
from app.db_tools import create_database_tools

# Load environment variables
load_dotenv()

async def test_database_connection():
    """Test the database connection and basic functionality."""
    
    print("🔍 Testing database connection...")
    
    try:
        # Initialize database connection
        await db_manager.initialize()
        print("✅ Database connection established!")
        
        # Test listing tables
        print("\n📋 Available tables:")
        tables = await db_manager.list_tables()
        for table in tables:
            print(f"  - {table}")
        
        # Test getting schema for first table (if any exist)
        if tables:
            first_table = tables[0]
            print(f"\n📊 Schema for table '{first_table}':")
            schema = await db_manager.get_table_schema(first_table)
            for column in schema:
                print(f"  - {column['column_name']}: {column['data_type']}")
        
        # Test database tools
        print("\n🛠️ Testing database tools...")
        tools = create_database_tools()
        print(f"✅ Created {len(tools)} database tools:")
        for tool in tools:
            print(f"  - {tool.name}: {tool.description}")
        
        print("\n🎉 All tests passed! Your database is ready for AI agents.")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n💡 Make sure:")
        print("  1. Your .env file has the correct DATABASE_URL")
        print("  2. Your Railway PostgreSQL is running")
        print("  3. The connection string is valid")
    
    finally:
        # Close database connection
        await db_manager.close()

if __name__ == "__main__":
    asyncio.run(test_database_connection())
