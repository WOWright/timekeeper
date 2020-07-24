import plotly.express as px
import pandas as pd
import datetime as dt

#Dummy data
projects = {'SARM':[['0800', '0935'],['1132', '1248'],['1539', '1617']],'PCKA':[['0936','1131']],'LNCH':[['1249','1538']]}
today = dt.datetime.date(dt.datetime.now())
today_list = today.strftime('%Y, %m, %d').split(', ')

#Prep for DataFrame-ing
task_list = []
for task in projects.keys():
    curr_proj = projects[task]
    for times in curr_proj:
        st_time = times[0]
        en_time = times[1]
        for thing in today_list:
            st_time += thing
            en_time += thing
        st_formatted = dt.datetime.strptime(st_time,'%H%M%Y%m%d')
        en_formatted = dt.datetime.strptime(en_time,'%H%M%Y%m%d')
        task_list.append(dict(Task=f'{task}',Start=st_formatted,Finish=en_formatted))

df = pd.DataFrame(task_list)

fig = px.timeline(df, x_start="Start", x_end="Finish", y="Task",color="Task")
fig.show()