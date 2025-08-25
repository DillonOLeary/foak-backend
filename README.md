# FOAK Backend

AI-powered site analysis for methane capture and utilization opportunities.

## Setup

### Environment Variables

Create a `.env` file in the root directory with the following variables:

```bash
# Database Configuration
DATABASE_URL=postgresql://username:password@localhost:5432/database_name

# API Keys
TAVILY_API_KEY=your_tavily_api_key_here
GOOGLE_API_KEY=your_google_api_key_here
```

### Database Setup

1. **Install dependencies:**
   ```bash
   uv sync
   ```

2. **Set up your PostgreSQL database** and update the `DATABASE_URL` in your `.env` file.

3. **Run the AI analysis:**
   ```bash
   python ai.py
   ```

## Features

- **AI-powered site analysis** using Pydantic AI agents
- **PostgreSQL integration** for data-driven insights
- **Custom database tools** for agents to query relevant data
- **Two-stage analysis process**: individual site analysis + comparative scoring

## Database Tools

The AI agents have access to the following database tools:

- `execute_database_query`: Execute custom SQL queries
- `get_table_schema`: Get table structure information
- `search_table_data`: Search for data using text terms
- `list_available_tables`: List all available tables

These tools allow the agents to draw conclusions from your database data during site analysis.