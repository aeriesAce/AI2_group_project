import duckdb

# here I map each occupation category to its mart table to load data dynamically
# its used to filter and load data based on the selected occupation in the dashboard
occupation_map = {
    "Pedagogik": "marts.mart_pedagogik",
    "Säkerhet och bevakning": "marts.mart_sakr_bevak",
    "Transport och lager": "marts.mart_tran_lager"
}

# a generic function to load data from any mart table
# used to retrieve data for the selected occupation categorydu
def load_mart(marts):
    con = duckdb.connect(database='jobs.duckdb')
    df = con.execute(f"SELECT * FROM {marts}").fetchdf()
    con.close()
    return df