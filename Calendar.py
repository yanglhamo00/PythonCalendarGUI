import tkinter as tk
from tkcalendar import Calendar, DateEntry
from datetime import datetime, date

# Define recurring significant events with month-day keys (e.g., "12-25" for Christmas)
recurring_events = {
    "01-01": "New Year's Day",
    "01-15": "Martin Luther King Jr. Day",
    "02-02": "Groundhog Day",
    "02-14": "Valentine's Day",
    "02-19": "Presidents' Day",
    "03-17": "St. Patrick's Day",
    "03-20": "First Day of Spring!",
    "04-01": "April Fool's Day",
    "04-22": "Earth Day",
    "05-05": "Cinco de Mayo",
    "05-12": "Mother's Day",
    "05-27": "Memorial Day",
    "06-14": "Flag Day",
    "06-16": "Father's Day",
    "06-20": "First Day of Summer!",
    "07-04": "Independence Day",
    "09-02": "Labor Day",
    "09-11": "Patriot Day",
    "09-22": "First Day of Fall!",
    "10-14": "Columbus Day",
    "10-31": "Halloween",
    "11-03": "Daylight Saving Time Ends",
    "11-11": "Veterans Day",
    "11-28": "Thanksgiving",
    "12-21": "First Day of Winter!",
    "12-25": "Christmas",
    "12-31": "New Year's Eve",
}

# Global dictionary to store events
events = {}

def generate_recurring_events(year):
    for md, name in recurring_events.items():
        month, day = map(int, md.split('-'))
        event_date = date(year, month, day)
        if event_date not in events:
            events[event_date] = []
        events[event_date].append(name)

def highlight_events(cal):
    cal.tag_config('event', background='#FF1493', foreground='white')
    for event_date, event_list in events.items():
        for event in event_list:
            cal.calevent_create(event_date, event, 'event')

def on_date_selected(event):
    selected_date = calendar.get_date()
    selected_date_obj = datetime.strptime(selected_date, '%Y-%m-%d').date()
    event_info = "\n".join(events.get(selected_date_obj, ["No events"]))
    event_label.config(text=f"Events:\n{event_info}")

def add_appointment():
    event_date = date_entry.get_date()
    event_name = event_name_entry.get()
    if event_date and event_name:
        if event_date not in events:
            events[event_date] = []
        events[event_date].append(event_name)
        update_calendar()
        update_events_list()
        events_list.see(tk.END)  # Ensure the newly added event is visible

def edit_appointment():
    selected_date = date_entry.get_date()
    new_event_name = event_name_entry.get()
    if selected_date in events and new_event_name:
        # Replace all events with the new event name
        events[selected_date] = [new_event_name]
        update_calendar()
        update_events_list()

def delete_appointment():
    selected_index = events_list.curselection()
    if selected_index:
        event_info = events_list.get(selected_index)
        event_date_str, event_name = event_info.split(": ")
        event_date = datetime.strptime(event_date_str, '%Y-%m-%d').date()
        if event_date in events:
            events[event_date].remove(event_name)
            if not events[event_date]:  # Remove the date entry if no events are left
                del events[event_date]
            update_calendar()
            update_events_list()

def update_calendar():
    calendar.calevent_remove('event')
    current_year = calendar.get_date().year
    generate_recurring_events(current_year)
    highlight_events(calendar)

def update_events_list():
    current_scroll_pos = events_list.yview()
    events_list.delete(0, tk.END)
    for event_date, event_names in events.items():
        for event_name in event_names:
            events_list.insert(tk.END, f"{event_date}: {event_name}")
    events_list.yview_moveto(current_scroll_pos[0])

app = tk.Tk()
app.title("Yang's Calendar")

calendar = Calendar(
    app,
    selectmode="day",
    date_pattern="yyyy-mm-dd",
    font="Arial 12",
    foreground="black",
    background="#FFB6C1",
    headersbackground="#FF69B4",
    headersforeground="white",
    selectforeground="white",
    selectbackground="#FF1493",
    weekendforeground="#FF1493",
    weekendbackground="#FFB6C1",
    othermonthforeground="#DC143C",
    othermonthbackground="#FFB6C1",
    disabledforeground="#FFA07A"
)
calendar.pack(padx=10, pady=10)

# Generate and highlight recurring events for the current year
current_year = datetime.now().year
generate_recurring_events(current_year)
highlight_events(calendar)

event_label = tk.Label(app, text="", font=("Arial", 12), pady=10)
event_label.pack()

calendar.bind("<<CalendarSelected>>", on_date_selected)

# Widgets for adding/editing/deleting appointments
control_frame = tk.Frame(app)
control_frame.pack(pady=10)

date_label = tk.Label(control_frame, text="Date:")
date_label.grid(row=0, column=0, padx=5)

date_entry = DateEntry(control_frame, date_pattern="yyyy-mm-dd")
date_entry.grid(row=0, column=1, padx=5)

event_name_label = tk.Label(control_frame, text="Event Name:")
event_name_label.grid(row=1, column=0, padx=5)

event_name_entry = tk.Entry(control_frame)
event_name_entry.grid(row=1, column=1, padx=5)

add_button = tk.Button(control_frame, text="Add", command=add_appointment)
add_button.grid(row=2, column=0, pady=5)

edit_button = tk.Button(control_frame, text="Edit", command=edit_appointment)
edit_button.grid(row=2, column=1, pady=5)

delete_button = tk.Button(control_frame, text="Delete", command=delete_appointment)
delete_button.grid(row=2, column=2, pady=5)

events_list = tk.Listbox(app, width=50, height=10)
events_list.pack(pady=10)

update_events_list()

app.mainloop()
