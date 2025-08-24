"""
Custom database tools for Pydantic AI agents.
"""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from app.database import db_manager


class DatabaseQueryInput(BaseModel):
    """Input for database query tool."""
    query: str = Field(..., description="SQL query to execute")
    description: str = Field(..., description="Description of what this query is looking for")


class TableSchemaInput(BaseModel):
    """Input for getting table schema."""
    table_name: str = Field(..., description="Name of the table to get schema for")


class TableSearchInput(BaseModel):
    """Input for searching table data."""
    table_name: str = Field(..., description="Name of the table to search")
    search_terms: List[str] = Field(..., description="List of terms to search for")
    limit: int = Field(default=50, description="Maximum number of results to return")


class DatabaseQueryResult(BaseModel):
    """Result from database query."""
    query: str = Field(..., description="The SQL query that was executed")
    results: List[Dict[str, Any]] = Field(..., description="Query results")
    row_count: int = Field(..., description="Number of rows returned")
    description: str = Field(..., description="Description of what was queried")


class TableSchemaResult(BaseModel):
    """Result from table schema query."""
    table_name: str = Field(..., description="Name of the table")
    columns: List[Dict[str, Any]] = Field(..., description="Column information")
    column_count: int = Field(..., description="Number of columns")


class TableSearchResult(BaseModel):
    """Result from table search."""
    table_name: str = Field(..., description="Name of the table searched")
    search_terms: List[str] = Field(..., description="Terms that were searched for")
    results: List[Dict[str, Any]] = Field(..., description="Search results")
    result_count: int = Field(..., description="Number of results found")


async def execute_database_query(input_data: DatabaseQueryInput) -> DatabaseQueryResult:
    """Execute a custom SQL query and return results."""
    try:
        results = await db_manager.execute_query(input_data.query)
        return DatabaseQueryResult(
            query=input_data.query,
            results=results,
            row_count=len(results),
            description=input_data.description
        )
    except Exception as e:
        return DatabaseQueryResult(
            query=input_data.query,
            results=[{"error": str(e)}],
            row_count=0,
            description=f"Error executing query: {input_data.description}"
        )


async def get_table_schema(input_data: TableSchemaInput) -> TableSchemaResult:
    """Get schema information for a specific table."""
    try:
        columns = await db_manager.get_table_schema(input_data.table_name)
        return TableSchemaResult(
            table_name=input_data.table_name,
            columns=columns,
            column_count=len(columns)
        )
    except Exception as e:
        return TableSchemaResult(
            table_name=input_data.table_name,
            columns=[{"error": str(e)}],
            column_count=0
        )


async def search_table_data(input_data: TableSearchInput) -> TableSearchResult:
    """Search for data in a table using text search terms."""
    try:
        results = await db_manager.search_data(
            input_data.table_name,
            input_data.search_terms,
            input_data.limit
        )
        return TableSearchResult(
            table_name=input_data.table_name,
            search_terms=input_data.search_terms,
            results=results,
            result_count=len(results)
        )
    except Exception as e:
        return TableSearchResult(
            table_name=input_data.table_name,
            search_terms=input_data.search_terms,
            results=[{"error": str(e)}],
            result_count=0
        )


async def list_available_tables() -> List[str]:
    """List all available tables in the database."""
    try:
        return await db_manager.list_tables()
    except Exception as e:
        return [f"Error listing tables: {str(e)}"]


# Create tool functions for Pydantic AI
def create_database_tools():
    """Create database tools for Pydantic AI agents."""
    from pydantic_ai import Tool
    
    return [
        Tool(
            name="execute_database_query",
            description="Execute a custom SQL query on the PostgreSQL database. Use this to get specific data needed for analysis.",
            input_type=DatabaseQueryInput,
            function=execute_database_query
        ),
        Tool(
            name="get_table_schema",
            description="Get the schema (column names and types) for a specific table in the database.",
            input_type=TableSchemaInput,
            function=get_table_schema
        ),
        Tool(
            name="search_table_data",
            description="Search for data in a table using text search terms. Useful for finding relevant records.",
            input_type=TableSearchInput,
            function=search_table_data
        ),
        Tool(
            name="list_available_tables",
            description="List all available tables in the database to understand what data is available.",
            input_type=None,
            function=list_available_tables
        )
    ]
