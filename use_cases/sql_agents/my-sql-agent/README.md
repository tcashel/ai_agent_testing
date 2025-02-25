# AI Query Assistant

An AI-powered data query and analysis tool that helps users generate database queries, analyze data, and visualize results.

## Setup Instructions

1. Create and setup the conda environment:
```bash
conda env create -f environment.yml
conda activate ai_query_assistant
```
to update an env afer changing the environment.yml file, run:

```bash
conda env update -f environment.yml
```

or

```bash
conda env update -f environment.yml --prune
```

2. Set up the database:
```bash
# Make scripts executable
cd scripts
chmod +x setup_db.sh

# Initialize database and load test data
./setup_db.sh

# To reset the database (drops everything and starts fresh):
./setup_db.sh --clean
```

3. Ensure Ollama is running locally with a model like mistral:
```bash
ollama run mistral
```

## Project Structure

```
.
├── README.md
├── environment.yml
├── sql/
│   ├── init.sql        # Database schema
│   └── test_data.sql   # Sample data
├── scripts/
│   └── setup_db.sh     # Database setup and initialization
└── src/
    ├── agent/          # Query processing agents
    ├── config/         # Application configuration
    └── utils/          # Helper utilities
```

## Development

This project is being developed incrementally with a focus on testing and validation at each step.

Current Phase:
- Basic LangChain + Ollama integration
- PostgreSQL database setup
- Query processing and generation

Future Phases:
- Enhanced query validation
- Data analysis and visualization
- Frontend integration 