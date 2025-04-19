# Legal Database System

A system for importing and managing legal texts in a database. The system supports importing various legal codes and storing them in a PostgreSQL database.

## Supported Codes

- Civil Service Code
- Penal Code
- Traffic Code
- Bankruptcy Code
- Police Law
- Sports Law
- Tax Procedure Code
- Public Maritime Law Code
- Aviation Law Code

## Prerequisites

- Python 3.8+
- PostgreSQL 12+
- psycopg2
- pandas

## Installation

1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Unix/MacOS: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Create a `database.py` file with your database connection settings

## Usage

Each legal code has its own import script:

- `ypalilikos.py`: Civil Service Code Import
- `poinikos.py`: Penal Code Import
- `kyk.py`: Traffic Code Import
- `ptoxeutikos.py`: Bankruptcy Code Import
- `astynomikos.py`: Police Law Import
- `athlitikos.py`: Sports Law Import
- `forologiki_dikonomia.py`: Tax Procedure Code Import
- `naytiko.py`: Public Maritime Law Code Import
- `aeroporiko.py`: Aviation Law Code Import

Each code also has its corresponding duplicate removal script (e.g. `remove_duplicates_ypalilikos.py`).

## Database Structure

The database consists of two main tables:

1. `laws`: Contains the laws/codes
   - `id`: Unique identifier
   - `name`: Law/code name

2. `articles`: Contains the articles
   - `id`: Unique identifier
   - `law_id`: Reference to law
   - `number`: Article number
   - `title`: Article title
   - `content`: Article content

## Security

- All scripts include error handling
- Use of transactions for safe data insertion
- Protection against SQL injection via parameterized queries
- Preservation of existing data integrity 