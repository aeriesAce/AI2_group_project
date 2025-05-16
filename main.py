# to run the whole program from here
from Dashboard.charts import sun_chart
from Dashboard.kpis import show_kpis

# to test the data for the kpis
# a temporary static occupation
selected_occupation = 'Transport och lager'
show_kpis(selected_occupation)
sun_chart(selected_occupation)