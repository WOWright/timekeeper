import datetime as dt
import json 
import pathlib
from collections import defaultdict
import tkinter as tk

def calendar_info():
    today = dt.datetime.date(dt.datetime.now())
    today_list = today.strftime('%Y, %m, %d, %B').split(', ')
    month_name = today_list.pop()
    record_file_name = month_name+'_'+today_list[0]+'.json'

    return today_list, month_name, record_file_name


def get_to_work():
    """Grab the sessions information and record to this month's JSON
    """
    starting_time = ent_start_time.get()
    ending_time = ent_end_time.get()
    project_of_day = ent_proj.get()
    
    #Deal with today's information
    today_list, _, record_file_name = calendar_info()
    
    #Load this month's data from JSON
    file = pathlib.Path(record_file_name)
    if file.exists():
        record_file = file.open('r')
        data = json.load(record_file)
        record_file.close()
    else:
        data = {'1':{}}

    #Initialize data into defaultdict of defaultdicts
    data = defaultdict(defaultdict, data)
    
    #Append new time information to given project
    todays_info = defaultdict(list,data[today_list[-1]])
    todays_info[project_of_day].append([starting_time.zfill(4), ending_time.zfill(4)])
    
    #Update today's information
    data[today_list[-1]] = todays_info
    
    #Save new info back to JSON
    json_object = json.dumps(data, indent = 4)
    with open(record_file_name, "w") as outfile: 
        outfile.write(json_object) 
        
    ent_start_time.delete(0, tk.END)
    ent_end_time.delete(0, tk.END)
    ent_proj.delete(0, tk.END)
    
    
def yabba_dabba_do():
    #Deal with today's information
    today_list, month_name, record_file_name = calendar_info()
    
    with open(record_file_name, "r") as infile:
        record_data = json.load(infile)
    
    record_data = dict(record_data)
    

    start_date = start_rpt_ent.get()
    end_date = end_rpt_ent.get()
    if len(start_date) == 0:
        requested_date_range = [today_list[-1]]
    elif len(end_date) == 0:
        requested_date_range = [str(x) for x in range(int(start_date),int(today_list[-1])+1)]
    else:
        requested_date_range = [str(x) for x in range(int(start_date),int(end_date)+1)]
    
    report_body = ''
    for date in requested_date_range:
        if date in record_data.keys():
            work_day = record_data[date]
            for proj in work_day.keys():
                proj_daily_time = 0
                duration_list = [dt.datetime.strptime(x[1].zfill(4),'%H%M')-dt.datetime.strptime(x[0].zfill(4),'%H%M')for x in work_day[proj]]
                duration = sum([x.total_seconds() for x in duration_list])
                proj_daily_time += round(duration/3600,2)
                report_body = report_body + f'{proj} Total Time for {date}-{month_name}: {proj_daily_time}\n'
        else:
            report_body += f'No Record Available for {date}\n'
        tps_report['text'] =report_body
    
    start_rpt_ent.delete(0, tk.END)
    end_rpt_ent.delete(0, tk.END)

#Stolen from Real Python's temperature converter example
window = tk.Tk()
window.title('Time Recorder')

#Frame for the time entry info
time_entry = tk.Frame(master=window)

#Time entry widgets creation
ent_start_time = tk.Entry(master=time_entry, width=10)
lbl_start = tk.Label(master=time_entry, text="Session Start Time")

ent_end_time = tk.Entry(master=time_entry, width=10)
lbl_end = tk.Label(master=time_entry, text="Session End Time")

ent_proj = tk.Entry(master=time_entry, width=10)
lbl_proj = tk.Label(master=time_entry, text="Session Project")

#Time entry widgets placement within frame
lbl_start.grid(row=0, column=0)
ent_start_time.grid(row=1, column=0)

lbl_end.grid(row=2, column=0)
ent_end_time.grid(row=3, column=0)

lbl_proj.grid(row=4, column=0)
ent_proj.grid(row=5, column=0)

#Time recording button
btn_record = tk.Button(
    master=time_entry,
    text="Record Session",
    command=get_to_work  # <--- Add this line
)
btn_record.grid(row=6, column=0, pady=5)


report_frame = tk.Frame(master=window)

range_frame = tk.Frame(master=report_frame)
range_frame.grid(row=0,column=0)

start_rpt_lbl = tk.Label(master=range_frame, text="Report\n Start")
start_rpt_ent = tk.Entry(master=range_frame, width=5)

end_rpt_lbl = tk.Label(master=range_frame, text="Report\n End")
end_rpt_ent = tk.Entry(master=range_frame, width=5)

start_rpt_lbl.grid(row=0, column=0)
start_rpt_ent.grid(row=1, column=0)

end_rpt_lbl.grid(row=0,column=1)
end_rpt_ent.grid(row=1,column=1)

#button to display today's time report
btn_report = tk.Button(
    master=report_frame,
    text="Generate Report",
    command=yabba_dabba_do  # <--- Add this line
)

btn_report.grid(row=1, column=0, pady=10)

#Text field to display todays report
printout_frame = tk.Frame(master=window)
tps_report = tk.Label(master=printout_frame)

time_entry.grid(row=0, column=0, padx=10)
report_frame.grid(row=0, column=1, padx=10)
printout_frame.grid(row=0, column=2, padx=10)

tps_report.grid(row=0, column=0, padx=10)

window.mainloop()