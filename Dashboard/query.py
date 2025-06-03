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
    
def get_top_employers(occupation):
    table = occupation_map.get(occupation)
    query = f"""
        SELECT employer_name AS 'Företag', COUNT(job_id) AS 'Antal annonser'
        FROM {table}
        GROUP BY "Företag"
        ORDER BY "Antal annonser" DESC
        LIMIT 10
    """
    return query

def get_top_titles(occupation):
    table = occupation_map.get(occupation)
    query = f"""
        SELECT 
            occupation_label AS "Titel", 
            occupation_category AS "Kategori", 
            SUM(vacancies) AS "Lediga tjänster"
        FROM {table}
        GROUP BY occupation_label, occupation_category
        ORDER BY "Lediga tjänster" DESC
        LIMIT 10
    """
    return query


def get_experience_distribution(category_choice): 
    table = occupation_map.get(category_choice)
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
    table = occupation_map.get(category_choice)
    query = f"""
    SELECT driving_license, COUNT(*) AS count 
    FROM {table}
    GROUP BY driving_license
    """
    con = duckdb.connect('jobs.duckdb')
    df = con.execute(query).fetch_df()
    con.close()
    return df
