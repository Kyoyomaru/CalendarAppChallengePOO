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

