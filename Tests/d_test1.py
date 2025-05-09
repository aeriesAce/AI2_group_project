from Dashboard.ui import set_sidebar, sidebar_choices, set_bg_pic

df = None
# using None just to try out the dashboard
set_bg_pic('./Media/test1.webp') 
choicr, detail = set_sidebar(df)
sidebar_choices(detail)