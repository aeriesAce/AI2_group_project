import duckdb

# I fetch the occupation categories so that we can use them for all functions
occupation_map = {
    "Pedagogik": "marts.mart_pedagogik",
    "Säkerhet och bevakning": "marts.mart_sakr_bevak",
    "Transport och lager": "marts.mart_tran_lager"
}
# I put the marts into a function so that I can create and use for all kpis and charts
def load_mart(marts):
    con = duckdb.connect(database='jobs.duckdb')
    df = con.execute(f"SELECT * FROM {marts}").fetchdf()
    con.close()
    return df

