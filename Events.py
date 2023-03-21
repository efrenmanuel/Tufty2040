
timer_events_no_ui_update=[]
timer_events=[]
pre_ui_events=[]
ui_events=[]


def add_pre_ui_event(event):
    if event not in pre_ui_events:
        pre_ui_events.append(event)
    
    pre_ui_events.sort(key=lambda event: event[1])
    
def add_ui_event(event):
    if event not in ui_events:
        ui_events.append(event)
    ui_events.sort(key=lambda event: event[1])
    print(ui_events)
        
                
def add_timer_event_no_update(event):
    if event not in timer_events_no_ui_update:
        timer_events_no_ui_update.append(event)
    
    timer_events_no_ui_update.sort(key=lambda event: event[1])
    
                
def rem_timer_event_no_update(event):
    if event in timer_events_no_ui_update:
        timer_events_no_ui_update.remove(event)
        
def remove_ui_event(event):
    if event in ui_events:
        ui_events.remove(event)
    
    print(ui_events)
        
def flip_ui_event(event):
    if event not in ui_events:
        ui_events.append(event)
    else:
        ui_events.remove(event)
    ui_events.sort(key=lambda event: event[1])
    print(ui_events)
        
def flip_timer_event(event):
    if event not in timer_events:
        timer_events.append(event)
    else:
        timer_events.remove(event)
    timer_events.sort(key=lambda event: event[1])
        #print(timer_events)
    
def rem_timer_event(event):
    if event in timer_events:
        timer_events.remove(event)
    
def update_no_ui():
    for event in timer_events_no_ui_update:
        event[0]()


def update_needs_ui():
    for event in timer_events:
        event[0]()
        
def update_pre_ui():
    for event in pre_ui_events:
        event[0]()
        
def update_ui():
    for event in ui_events:
        event[0]()

def run_queues(events_updated):
    for event in timer_events_no_ui_update:
        update_no_ui()
    
    if len(timer_events):
        update_needs_ui()
        
    if len(timer_events) or events_updated:
        update_pre_ui()
        print(ui_events)
        update_ui()
