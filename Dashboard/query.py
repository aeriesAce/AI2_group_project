from config import occupation_map
import duckdb

# making a generic sql query as a option as well? test
def build_sql_query(filters: dict) -> str:
    clauses = []
    for col, selected_values in filters.items():
        if not selected_values:
            continue
        if isinstance(selected_values[0], bool):
            bool_values = ", ".join(["TRUE" if v else "FALSE" for v in selected_values])
            clauses.append(f"{col} IN ({bool_values})")
        else:
            quoted_values = ", ".join([f"'{str(v)}'" for v in selected_values])
            clauses.append(f"{col} IN ({quoted_values})")
    if clauses:
        return "WHERE " + " AND ".join(clauses)
    else:
        return ""
    
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
    """
    return query

def get_ads_region(occupation):
    table = occupation_map.get(occupation)
    query = f"""
        SELECT region, SUM(vacancies) AS Annonser
        FROM {table}
        GROUP BY region
        ORDER BY Annonser DESC
    """
    return query

def get_experience_distribution(category_choice): 
    
    table_map = {
        "Pedagogik": "marts.mart_pedagogik",
        "Säkerhet och bevakning": "marts.mart_sakr_bevak",
        "Transport och lager": "marts.mart_tran_lager"
    }
    table = table_map.get(category_choice)
    query = f"""
    SELECT experience_required, COUNT(*) AS count 
    FROM {table}
    GROUP BY experience_required
    """
    con = duckdb.connect('jobs.duckdb')
    df = con.execute(query).fetch_df()
    con.close()
    return df

def get_driving_license_requierd(category_choice): 

    table_map = {
        "Pedagogik": "marts.mart_pedagogik",
        "Säkerhet och bevakning": "marts.mart_sakr_bevak",
        "Transport och lager": "marts.mart_tran_lager"
    }
    table = table_map.get(category_choice)
    query = f"""
    SELECT driving_license, COUNT(*) AS count 
    FROM {table}
    GROUP BY driving_license
    """
    con = duckdb.connect('jobs.duckdb')
    df = con.execute(query).fetch_df()
    con.close()
    return df
