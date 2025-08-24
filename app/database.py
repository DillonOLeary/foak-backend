"""
Database connection and utilities for PostgreSQL.
"""

import os
from typing import Any, Dict, List, Optional

import asyncpg
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database configuration
DATABASE_URL = os.getenv("postgresql_link/railway")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is required")

class DatabaseManager:
    """Manages PostgreSQL database connections and queries."""
    
    def __init__(self):
        self.pool: Optional[asyncpg.Pool] = None
    
    async def initialize(self):
        """Initialize the database connection pool."""
        self.pool = await asyncpg.create_pool(
            DATABASE_URL,
            min_size=1,
            max_size=10,
            command_timeout=60
        )
    
    async def close(self):
        """Close the database connection pool."""
        if self.pool:
            await self.pool.close()
    
    async def execute_query(self, query: str, *args) -> List[Dict[str, Any]]:
        """Execute a query and return results as a list of dictionaries."""
        if not self.pool:
            raise RuntimeError("Database not initialized. Call initialize() first.")
        
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(query, *args)
            return [dict(row) for row in rows]
    
    async def get_table_schema(self, table_name: str) -> List[Dict[str, Any]]:
        """Get schema information for a specific table."""
        query = """
        SELECT 
            column_name,
            data_type,
            is_nullable,
            column_default
        FROM information_schema.columns 
        WHERE table_name = $1
        ORDER BY ordinal_position
        """
        return await self.execute_query(query, table_name)
    
    async def list_tables(self) -> List[str]:
        """List all tables in the database."""
        query = """
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public'
        ORDER BY table_name
        """
        results = await self.execute_query(query)
        return [row['table_name'] for row in results]
    
    async def search_data(self, table_name: str, search_terms: List[str], limit: int = 50) -> List[Dict[str, Any]]:
        """Search for data in a table using multiple search terms."""
        # Get table schema to build dynamic query
        schema = await self.get_table_schema(table_name)
        text_columns = [col['column_name'] for col in schema if 'char' in col['data_type'] or 'text' in col['data_type']]
        
        if not text_columns:
            # If no text columns, just return first few rows
            query = f"SELECT * FROM {table_name} LIMIT $1"
            return await self.execute_query(query, limit)
        
        # Build dynamic search query
        conditions = []
        params = []
        param_count = 1
        
        for term in search_terms:
            term_conditions = []
            for col in text_columns:
                term_conditions.append(f"{col} ILIKE ${param_count}")
                params.append(f"%{term}%")
                param_count += 1
            conditions.append(f"({' OR '.join(term_conditions)})")
        
        where_clause = " OR ".join(conditions)
        query = f"SELECT * FROM {table_name} WHERE {where_clause} LIMIT ${param_count}"
        params.append(limit)
        
        return await self.execute_query(query, *params)

# Global database manager instance
db_manager = DatabaseManager()
