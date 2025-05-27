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