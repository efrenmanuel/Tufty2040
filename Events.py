
import _thread
import Display

#events that don't update the UI
timer_events_no_ui_update=[]
_snap_no_ui = []
_snap_no_ui_dirty = True

#background work scheduled from the UI thread
bg_events=[]

#events that ???? I forgor
timer_events=[]
_snap_timer = []
_snap_timer_dirty = True

#events that are needed to update the UI
pre_ui_events=[]
_snap_pre_ui = []
_snap_pre_ui_dirty = True

#events that draw to the UI
ui_events=[]
_snap_ui = []
_snap_ui_dirty = True

# overlay events run every frame, after UI, for high-frequency animation (e.g. sprites)
# each overlay callback handles its own partial_update
overlay_events=[]
_snap_overlay = []
_snap_overlay_dirty = True

ui_dirty = False
events_lock = _thread.allocate_lock()


def _sorted_insert_unique(event_list, event):
    if event not in event_list:
        event_list.append(event)
        event_list.sort(key=lambda queued_event: queued_event[1])
        return True
    return False


def _remove_if_present(event_list, event):
    if event in event_list:
        event_list.remove(event)
        return True
    return False


def _get_snapshot(event_list, snap, dirty):
    if dirty:
        events_lock.acquire()
        try:
            snap = list(event_list)
        finally:
            events_lock.release()
    return snap, False


def request_ui_update():
    global ui_dirty
    events_lock.acquire()
    try:
        ui_dirty = True
    finally:
        events_lock.release()


def enqueue_bg_event(event):
    events_lock.acquire()
    try:
        if event not in bg_events:
            bg_events.append(event)
    finally:
        events_lock.release()

def add_pre_ui_event(event):
    global _snap_pre_ui_dirty
    events_lock.acquire()
    try:
        if _sorted_insert_unique(pre_ui_events, event):
            _snap_pre_ui_dirty = True
    finally:
        events_lock.release()
    
def add_ui_event(event):
    global _snap_ui_dirty
    events_lock.acquire()
    try:
        if _sorted_insert_unique(ui_events, event):
            _snap_ui_dirty = True
    finally:
        events_lock.release()
    request_ui_update()
        
                
def add_timer_event_no_update(event):
    global _snap_no_ui_dirty
    events_lock.acquire()
    try:
        if _sorted_insert_unique(timer_events_no_ui_update, event):
            _snap_no_ui_dirty = True
    finally:
        events_lock.release()
    
                
def rem_timer_event_no_update(event):
    global _snap_no_ui_dirty
    events_lock.acquire()
    try:
        if _remove_if_present(timer_events_no_ui_update, event):
            _snap_no_ui_dirty = True
    finally:
        events_lock.release()
        
def remove_ui_event(event):
    global _snap_ui_dirty
    removed = False
    events_lock.acquire()
    try:
        removed = _remove_if_present(ui_events, event)
        if removed:
            _snap_ui_dirty = True
    finally:
        events_lock.release()
    if removed:
        request_ui_update()
        
def flip_ui_event(event):
    global _snap_ui_dirty
    events_lock.acquire()
    try:
        if event not in ui_events:
            _sorted_insert_unique(ui_events, event)
        else:
            ui_events.remove(event)
        _snap_ui_dirty = True
    finally:
        events_lock.release()
    request_ui_update()
        
def flip_timer_event(event):
    global _snap_timer_dirty
    events_lock.acquire()
    try:
        if event not in timer_events:
            _sorted_insert_unique(timer_events, event)
        else:
            timer_events.remove(event)
        _snap_timer_dirty = True
    finally:
        events_lock.release()
    request_ui_update()
    
def rem_timer_event(event):
    global _snap_timer_dirty
    removed = False
    events_lock.acquire()
    try:
        removed = _remove_if_present(timer_events, event)
        if removed:
            _snap_timer_dirty = True
    finally:
        events_lock.release()
    if removed:
        request_ui_update()

def add_overlay_event(event):
    global _snap_overlay_dirty
    events_lock.acquire()
    try:
        if _sorted_insert_unique(overlay_events, event):
            _snap_overlay_dirty = True
    finally:
        events_lock.release()

def remove_overlay_event(event):
    global _snap_overlay_dirty
    events_lock.acquire()
    try:
        if _remove_if_present(overlay_events, event):
            _snap_overlay_dirty = True
    finally:
        events_lock.release()
    
def update_no_ui():
    global _snap_no_ui, _snap_no_ui_dirty
    _snap_no_ui, _snap_no_ui_dirty = _get_snapshot(timer_events_no_ui_update, _snap_no_ui, _snap_no_ui_dirty)
    changed = False
    for event in _snap_no_ui:
        if event[0]():
            changed = True
    return changed

def update_needs_ui():
    global _snap_timer, _snap_timer_dirty
    _snap_timer, _snap_timer_dirty = _get_snapshot(timer_events, _snap_timer, _snap_timer_dirty)
    changed = False
    for event in _snap_timer:
        if event[0]():
            changed = True
    return changed
        
def update_pre_ui():
    global _snap_pre_ui, _snap_pre_ui_dirty
    _snap_pre_ui, _snap_pre_ui_dirty = _get_snapshot(pre_ui_events, _snap_pre_ui, _snap_pre_ui_dirty)
    changed = False
    for event in _snap_pre_ui:
        if event[0]():
            changed = True
    return changed
        
def update_ui():
    global _snap_ui, _snap_ui_dirty
    _snap_ui, _snap_ui_dirty = _get_snapshot(ui_events, _snap_ui, _snap_ui_dirty)
    for event in _snap_ui:
        event[0]()

def update_overlays():
    global _snap_overlay, _snap_overlay_dirty
    _snap_overlay, _snap_overlay_dirty = _get_snapshot(overlay_events, _snap_overlay, _snap_overlay_dirty)
    for event in _snap_overlay:
        event[0]()
        
def run_bg_queues():
    if update_no_ui():
        request_ui_update()

    while True:
        events_lock.acquire()
        try:
            if not bg_events:
                break
            event = bg_events.pop(0)
        finally:
            events_lock.release()
        event()

def run_queues(events_updated=False):
    global ui_dirty

    events_lock.acquire()
    try:
        needs_ui = ui_dirty or events_updated
        ui_dirty = False
        has_timer = bool(timer_events)
        has_overlays = bool(overlay_events)
    finally:
        events_lock.release()

    if has_timer and update_needs_ui():
        needs_ui = True

    if needs_ui:
        update_pre_ui()
        update_ui()
        update_overlays()
        Display.update()
        return True

    if has_overlays:
        update_overlays()
        # overlays handle their own partial_update calls

    return has_overlays


