from dataclasses import dataclass, field
from datetime import datetime, date, time
from typing import ClassVar

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
#el date_ inicia con un parametro en el constructor obligatoriamente
    def __init__(self, date_:date):
        self.date_ = date_
    pass


# TODO: Implement Calendar class here
class Calendar:
    days: dict[date, Day]
    events: dict[str, Event]
    def add_event(self, title:str, description:str,date_:date,start_at:time,end_at:time):
      if date_<date.now():
          date_lower_than_today_error()
      if date_ not in self.days:
          self.days[date_] = Day(date_)
          new_event = Event(title, description, date_, start_at, end_at)
          self.days[date_].add_event(new_event)

