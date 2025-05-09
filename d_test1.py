from Dashboard.ui import set_bg_pic, set_sidebar, sidebar_choices

df = None
# using None just to try out the dashboard
set_bg_pic('./Media/test1.webp') 
choicr, detail = set_sidebar(df)
sidebar_choices(detail)