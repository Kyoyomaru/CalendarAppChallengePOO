from dataclasses import dataclass, field
from datetime import datetime, date, time
from typing import ClassVar, Dict, Optional

from app.services.util import generate_unique_id, date_lower_than_today_error, event_not_found_error, \
    reminder_not_found_error, slot_not_available_error
#el commit aparece hecho por otra persona pero el codigo es mio
# TODO: Implement Reminder class here
@dataclass()
class Reminder:
    EMAIL: ClassVar[str] = "email"
    SYSTEM: ClassVar[str] = "system"
    date_time : datetime
    type: str = EMAIL
 #se cumple que regresa una cadena de texto
    def __str__(self) -> str:
        return f"Reminder on {self.date_time} of type {self.type}"


# TODO: Implement Event class here
@dataclass()
class Event:
    title:str
    description: str
    date_: date
    start_at:time
    end_at:time
    reminders:list[Reminder]=field(default_factory=list,init=False)
    id: str= field(default_factory=generate_unique_id)
    def add_reminder (self,date_time:datetime,type:str =Reminder.EMAIL):
            new_reminder=Reminder(date_time=date_time,type=type)
 #Recordar indentar bien
            self.reminders.append(new_reminder)
    def delete_reminder (self, reminder_index: int):
       if 0 <= reminder_index < len(self.reminders):
           del self.reminders[reminder_index]
       else:
            reminder_not_found_error()


def __str__ (self) -> str:
        return (
        f"ID: {self.id}\n"
        f"Event title: {self.title}\n"
        f"Description: {self.description}\n"
        f"Time: ({self.start_at}) - ({self.end_at})"
        )
# TODO: Implement Day class here

class Day:
    def __init__(self, date_: date):
        self.date_ = date_
        self.slots: Dict[time, Optional[str]] = {}
        self._init_slots()

    def _init_slots(self):
        for hour in range(24):
            for minute in range(0, 60, 15):
                slot_time = time(hour, minute)
                self.slots[slot_time] = None

    def add_event(self, event_id: str, start_at: time, end_at: time):
        slots_to_book = []
        for slot_time in self.slots:
            if start_at <= slot_time < end_at:
                if self.slots[slot_time] is not None:
                    slot_not_available_error()
                slots_to_book.append(slot_time)

        for slot_time in slots_to_book:
            self.slots[slot_time] = event_id

    def delete_event(self, event_id: str):
        deleted = False
        for slot, saved_id in self.slots.items():
            if saved_id == event_id:
                self.slots[slot] = None
                deleted = True
        if not deleted:
            event_not_found_error()

    def update_event(self, event_id: str, start_at: time, end_at: time):
        for slot in self.slots:
            if self.slots[slot] == event_id:
                self.slots[slot] = None
        for slot in self.slots:
            if start_at <= slot < end_at:
                if self.slots[slot]:
                    slot_not_available_error()
                else:
                    self.slots[slot] = event_id


class Calendar:
    def __init__(self):
        self.days: Dict[date, Day] = {}
        self.events: Dict[str, Event] = {}

    def add_event(self, title: str, description: str, date_: date, start_at: time, end_at: time) -> str:
        if date_ < datetime.now().date():
            date_lower_than_today_error()
        if date_ not in self.days:
            self.days[date_] = Day(date_)
        day = self.days[date_]
        new_event = Event(
            title=title,
            description=description,
            date_=date_,
            start_at=start_at,
            end_at=end_at,
        )
        day.add_event(new_event.id, start_at, end_at)
        self.events[new_event.id] = new_event
        return new_event.id

    def add_reminder(self, event_id: str, date_time: datetime, type_: str):
        if event_id not in self.events:
            event_not_found_error()
        event = self.events[event_id]
        event.add_reminder(date_time, type_)
# El metodo find_available_slots recibe un parámetro date_ de tipo date y retorna una lista
 #de objetos de tipo time. Un espacio disponible es un objeto de la clase time que no tiene
    def find_available_slots(self, date_: date) -> list[time]:
        if date_ not in self.days:
            return [time(h, m) for h in range(24) for m in range(0, 60, 15)]
        day = self.days[date_]
        return [slot_time for slot_time, event_id in day.slots.items() if event_id is None]

    def update_event(self, event_id: str, title: str, description: str, date_: date, start_at: time, end_at: time):
        if event_id not in self.events:
            event_not_found_error()
        event = self.events[event_id]
        is_new_date = event.date_ != date_
        if is_new_date:
            old_day = self.days.get(event.date_)
            if old_day:
                old_day.delete_event(event_id)
        else:
            old_day = self.days.get(event.date_)
            if old_day:
                old_day.delete_event(event_id)
        event.title, event.description, event.date_, event.start_at, event.end_at = title, description, date_, start_at, end_at
        if date_ not in self.days:
            self.days[date_] = Day(date_)
        new_day = self.days[date_]
        new_day.add_event(event_id, start_at, end_at)

    def delete_event(self, event_id: str):
        if event_id not in self.events:
            event_not_found_error()
        event_to_delete = self.events.pop(event_id)
        day = self.days.get(event_to_delete.date_)
        if day:
            day.delete_event(event_id)

    def find_events(self, start_at: date, end_at: date) -> dict[date, list[Event]]:
        events: dict[date, list[Event]] = {}
        for event in self.events.values():
            if start_at <= event.date_ <= end_at:
                if event.date_ not in events:
                    events[event.date_] = []
                events[event.date_].append(event)
        return events

    def delete_reminder(self, event_id: str, reminder_index: int):
        event = self.events.get(event_id)
        if not event:
            event_not_found_error()
        event.delete_reminder(reminder_index)

    def list_reminders(self, event_id: str) -> list[Reminder]:
        event = self.events.get(event_id)
        if not event:
            event_not_found_error()
        return event.reminders