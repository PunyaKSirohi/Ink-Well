# Person Document Gemma

A comprehensive document processing pipeline that analyzes PDFs based on personas and jobs-to-be-done, extracting the most relevant content using the Gemma 3 LLM.

## Overview

Person Document Gemma is a RAG (Retrieval-Augmented Generation) based system that intelligently processes collections of PDF documents. It extracts and ranks relevant sections tailored to specific personas and their tasks, generating structured insights using a local Gemma 3 LLM.

### Key Features

- **Persona-based Document Analysis**: Processes documents from the perspective of different professional roles
- **Task-Oriented Extraction**: Focuses on extracting content relevant to specific jobs-to-be-done
- **Multi-Collection Support**: Processes multiple document collections independently
- **Local LLM Integration**: Uses Gemma 3 (1B parameter model) through Ollama
- **Vector Database**: Stores document embeddings using Qdrant
- **Structured Output**: Generates JSON files with ranked document sections and refined content

## Installation

### Prerequisites

- Python 3.8+
- Docker (for Qdrant vector database)
- Ollama with Gemma 3 model installed

### Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd person_document_gemma
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Download the embedding model**:
   ```bash
   # The model will be stored in ./bge-small
   python -c "from transformers import AutoTokenizer, AutoModel; tokenizer = AutoTokenizer.from_pretrained('BAAI/bge-small-en'); model = AutoModel.from_pretrained('BAAI/bge-small-en'); tokenizer.save_pretrained('./bge-small'); model.save_pretrained('./bge-small')"
   ```

5. **Start Qdrant vector database**:
   ```bash
   docker compose -f docker-compose.db.yml up -d
   ```

6. **Ensure Ollama is running with Gemma 3**:
   ```bash
   # Check if model is available
   ollama list
   
   # Pull the model if needed
   ollama pull gemma3:1b
   ```

## Directory Structure

```
.
├── data/
│   ├── collection_1/               # Example collection
│   │   ├── pdfs/                   # PDF documents
│   │   ├── input.json              # Collection configuration
│   │   └── output.json             # Generated analysis
│   ├── collection_2/
│   └── collection_3/
├── bge-small/                      # Local embedding model
├── collection_manager.py           # Collection handling utilities
├── llm_utils.py                    # LLM and embedding functions
├── main.py                         # Main pipeline orchestration
├── process_collections.py          # Command-line processing utility
├── rag_pipeline.py                 # RAG pipeline implementation
├── vector_db_setup.py              # Vector database management
├── README.md                       # This file
├── README_COLLECTIONS.md           # Detailed collection documentation
└── LOGGING.md                      # Logging documentation
```

## Usage

### Quick Start

1. **Process all collections**:
   ```bash
   python main.py
   ```

2. **Process a specific collection**:
   ```bash
   python main.py --collection collection_1
   ```

3. **Using the utility script with options**:
   ```bash
   # List all available collections
   python process_collections.py --list

   # Validate collection structure
   python process_collections.py --validate

   # Process with verbose output
   python process_collections.py --verbose

   # Process specific collection
   python process_collections.py --collection collection_1
   ```

### Creating a New Collection

1. **Create collection directory structure**:
   ```bash
   mkdir -p data/my_collection/pdfs
   ```

2. **Add PDF files to the collection**:
   ```bash
   cp path/to/documents/*.pdf data/my_collection/pdfs/
   ```

3. **Create input.json file**:
   ```json
   {
       "challenge_info": {
           "challenge_id": "unique_id",
           "test_case_name": "descriptive_name",
           "description": "Brief description"
       },
       "documents": [
           {"filename": "document1.pdf", "title": "Document Title 1"},
           {"filename": "document2.pdf", "title": "Document Title 2"}
       ],
       "persona": {
           "role": "Travel Planner"
       },
       "job_to_be_done": {
           "task": "Plan a trip of 4 days for a group of 10 college friends."
       }
   }
   ```

4. **Process the collection**:
   ```bash
   python main.py --collection my_collection
   ```

## System Architecture

### Core Components

1. **Collection Manager**: Handles collection discovery, input parsing, and output saving
2. **LLM Utils**: Manages embedding generation and LLM query processing
3. **Vector DB Setup**: Handles document ingestion and vector database operations
4. **RAG Pipeline**: Implements the retrieval and generation workflow
5. **Main Pipeline**: Orchestrates the overall processing flow

### Processing Flow

1. **Discovery**: System scans data directory for collections
2. **Validation**: Checks each collection has required structure
3. **Input Parsing**: Reads input.json to extract persona and job
4. **Document Ingestion**: Loads PDFs into vector database
5. **Query Processing**: Uses LLM to analyze documents based on persona/job
6. **Output Generation**: Formats results and saves to output.json

## Configuration

### Environment Variables

- `LOG_LEVEL`: Set logging verbosity (ERROR, WARN, INFO, VERBOSE)
- `LOG_FILE`: Path for file logging (optional)
- `LOG_FORMAT`: Format style (default, detailed, simple)
- `LOCAL_EMBEDDING_MODEL_PATH`: Path to local embedding model (default: "./bge-small")

### Command Line Options

For `main.py`:
- `--data-root`: Root directory containing collections (default: "data")
- `--collection`: Process specific collection by name
- `--log-level`: Set logging level

For `process_collections.py`:
- `--list`: List all available collections
- `--validate`: Validate collection structure
- `--collection`: Process specific collection
- `--data-root`: Set data directory path
- `--verbose`: Enable verbose logging
- `--quiet`: Suppress most output

## Output Format

The system generates an output.json file for each collection with:

```json
{
    "metadata": {
        "input_documents": ["list", "of", "pdf", "files"],
        "persona": "Travel Planner",
        "job_to_be_done": "Plan a trip...",
        "processing_timestamp": "2025-07-21T19:48:21.173411"
    },
    "extracted_sections": [
        {
            "document": "filename.pdf",
            "section_title": "Section Title",
            "importance_rank": 1,
            "page_number": 5
        }
    ],
    "subsection_analysis": [
        {
            "document": "filename.pdf",
            "refined_text": "Processed content...",
            "page_number": 5
        }
    ]
}
```

## Logging

The system includes comprehensive logging capabilities with multiple log levels:

- **ERROR**: Critical errors that prevent operation
- **WARN**: Warning conditions that don't stop execution
- **INFO**: General operational information
- **VERBOSE**: Detailed debugging information

### Setting Log Level

```bash
# Set via environment variable
export LOG_LEVEL=VERBOSE
python main.py

# Or directly via command line
python main.py --log-level VERBOSE
```

### File Logging

```bash
# Log to file in addition to console
export LOG_FILE=./logs/pipeline.log
python main.py
```

For complete logging documentation, see LOGGING.md.

## Troubleshooting

### Common Issues

1. **No collections found**:
   - Check directory structure matches expected format
   - Ensure input.json files are present and valid
   - Use `--list` option to see what collections are discovered

2. **Missing PDFs**:
   - Verify PDF files are in the `pdfs/` subdirectory
   - Check file permissions
   - Ensure PDFs are readable

3. **Vector database errors**:
   - Ensure Qdrant is running: `docker ps | grep qdrant`
   - Check connection to `http://localhost:6333`
   - Restart with: `docker compose -f docker-compose.db.yml restart`

4. **LLM errors**:
   - Verify Ollama is running with: `ollama list`
   - Install model if needed: `ollama pull gemma3:1b`
   - Check Ollama logs for errors

5. **Embedding model errors**:
   - Verify `./bge-small` directory exists
   - Check model files are complete
   - Re-download the embedding model if necessary

### Validation

Use the validation feature to check collections:

```bash
python process_collections.py --validate
```

This will check:
- All required directories exist
- input.json files are valid
- PDF files are present
- Required fields are populated

## Example Use Cases

### Travel Planning

```json
{
    "persona": {
        "role": "Travel Planner"
    },
    "job_to_be_done": {
        "task": "Plan a trip of 4 days for a group of 10 college friends."
    }
}
```

### HR Documentation

```json
{
    "persona": {
        "role": "HR professional"
    },
    "job_to_be_done": {
        "task": "Create and manage fillable forms for onboarding and compliance."
    }
}
```

### Food Service

```json
{
    "persona": {
        "role": "Food Contractor"
    },
    "job_to_be_done": {
        "task": "Prepare a vegetarian buffet-style dinner menu for a corporate gathering, including gluten-free items."
    }
}
```

## Performance Tips

1. **Batch Processing**: Process multiple small collections together
2. **Resource Management**: Monitor GPU/CPU usage during processing
3. **Disk Space**: Ensure adequate space for vector database storage
4. **Memory Usage**: Larger document collections require more RAM
5. **Log Levels**: Use INFO or ERROR in production for better performance

## API Reference

### CollectionManager Class

```python
from collection_manager import CollectionManager

manager = CollectionManager("data")
collections = manager.discover_collections()
input_data = manager.load_collection_input(collection)
manager.save_collection_output(collection, output_data)
```

### Key Functions

```python
# Query documents using LLM
from llm_utils import query_documents
response, chunks = query_documents(user_query, vector_db_collection)

# Update or create vector database collection
from vector_db_setup import update_collection
update_collection(pdf_dir, collection_name)

# Format output JSON
from rag_pipeline import format_json
output_data = format_json(input_docs, persona, job, response, chunks)
```

## Quick Reference

| Task | Command |
|------|---------|
| Process all collections | `python main.py` |
| Process one collection | `python main.py --collection collection_1` |
| List collections | `python process_collections.py --list` |
| Validate structure | `python process_collections.py --validate` |
| Verbose output | `python main.py --log-level VERBOSE` |
| Quiet processing | `python process_collections.py --quiet` |

---

## License

[License information]

## Contributors

[Contributors information]

## Acknowledgments

- This project uses the Gemma 3 language model from Google
- Vector embeddings powered by BGE-small
- Qdrant vector database for efficient similarity search
```
