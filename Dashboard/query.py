from config import occupation_map
import duckdb

con = duckdb.connect('jobs.duckdb')
def get_top_employers(occupation):
    table = occupation_map.get(occupation)
    query = f"""
        SELECT employer_name AS 'Företag', SUM(vacancies) AS 'Lediga tjänster'
        FROM {table}
        GROUP BY "Företag"
        ORDER BY "Lediga tjänster" DESC
        LIMIT 10
    """
    return query

def get_top_titles(occupation):
    table = occupation_map.get(occupation)
    query = f"""
        SELECT headline, COUNT(*) AS Titles
        FROM {table}
        GROUP BY headline
        ORDER BY  DESC
        LIMIT 10
    """
    return query

def get_ads_region(occupation):
    table = occupation_map.get(occupation)
    query = f"""
        SELECT region, SUM(vacancies) AS Annonser
        FROM {table}
        GROUP BY region
        ORDER BY Annonser DESC
        LIMIT 10
    """
    return query

def filter_categories(table, column):
    query = f"""
        SELECT DISTINCT {column}
        FROM {table}
        WHERE {column} IS NOT NULL
        ORDER BY {column}
    """
    return con.execute(query).fetchdf()[column].tolist()
    