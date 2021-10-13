from win10toast import ToastNotifier
from enum import Enum
import datetime
from threading import Thread


class Notification(object):
    def __init__(self, signature, icon):
        self.tnotif_ = ToastNotifier()
        self.signature_ = signature
        self.icon_ = icon

    def _send_msg(self, title, msg):
        self.tnotif_.show_toast(title=self.signature_ + " - " + title, msg=msg, icon_path=self.icon_, duration=10)


class Schedule(object):
    def __init__(self):
        self.weekly_queue_ = dict()
        self.daily_queue_ = dict()
        self.once_queue_ = dict()
        self.notify_ = Notification("Calendar", "YPN.ico")

    def _add_event(self):
        print("What type of event do you want to add?")
        choice = Selectors.Time(check_up({0: "only once", 1: "daily", 2: "weekly"}))
        if choice == Selectors.Time.ONCE:
            print("Name your event:")
            event_name = input()
            print("Give your event a description:")
            event_des = input()
            print("Please enter what date this event will occur in format m/d")
            set_time = check_time(Selectors.TimeType.DATE)
            print("Please enter what time this event will occur in format h:m")
            set_time = check_time(Selectors.TimeType.TIME, set_time)
            self.once_queue_[Holder(Event(event_name, event_des), set_time)] = False
        elif choice == Selectors.Time.DAILY:
            print("Name your event:")
            event_name = input()
            print("Give your event a description:")
            event_des = input()
            print("Please enter what date this event will occur in format h:m")
            set_time = check_time(Selectors.TimeType.TIME)
            self.daily_queue_[Holder(Event(event_name, event_des), set_time)] = False
        elif choice == Selectors.Time.WEEKLY:
            print("Name your event:")
            event_name = input()
            print("Give your event a description:")
            event_des = input()
            print("Please enter the day you want this event to occur")
            week = set_time = check_up(
                {0: "Monday", 1: "Tuesday", 2: "Wednesday", 3: "Thursday", 4: "Friday", 5: "Saturday", 6: "Sunday"})
            print("Please enter what date this event will occur in format h:m")
            set_time = check_time(Selectors.TimeType.TIME)
            self.weekly_queue_[Holder(Event(event_name, event_des), WeekHolder(week, set_time))]

    def _remove_event(self):
        if self.weekly_queue_ == {} and self.daily_queue_ == {} and self.once_queue_ == {}:
            print("There is nothing in your schedule.")
        else:
            print("Weekly events: {}".format(make_list(self.weekly_queue_)))
            print("Daily events: {}".format(make_list(self.daily_queue_)))
            print("One time events: {}".format(make_list(self.once_queue_)))

            print("Please type the name of the event you want to remove:")
            remove = input()
            for keys in list(self.weekly_queue_):
                if str(keys) == remove: del self.weekly_queue_[keys]
            for keys in list(self.daily_queue_):
                if str(keys) == remove: del self.daily_queue_[keys]
            for keys in list(self.once_queue_):
                if str(keys) == remove: del self.once_queue_[keys]

    def _ask_what(self):
        while True:
            ask = check_up({0: "Add Event", 1: "Remove Event", 2: "Check Events"})
            if ask == 0:
                self._add_event()
            elif ask == 1:
                self._remove_event()
            else:
                if self.weekly_queue_ == {} and self.daily_queue_ == {} and self.once_queue_ == {}:
                    print("There is nothing in your schedule.")
                else:
                    print("Weekly events: {}".format(make_list(self.weekly_queue_)))
                    print("Daily events: {}".format(make_list(self.daily_queue_)))
                    print("One time events: {}".format(make_list(self.once_queue_)))

    def _check_events(self):
        while True:
            now = datetime.datetime.now()
            for obj in list(self.once_queue_):
                if obj.time_hold.month == now.month:
                    if obj.time_hold.day == now.day:
                        if obj.time_hold.hour == now.hour:
                            if obj.time_hold.minute == now.minute:
                                self.notify_._send_msg(obj.obj_hold.name, obj.obj_hold.description)
                                del self.once_queue_[obj]

            for obj in list(self.daily_queue_):
                if not self.daily_queue_[obj]:
                    if obj.time_hold.hour == now.hour:
                        if obj.time_hold.minute == now.minute:
                            self.notify_._send_msg(obj.obj_hold.name, obj.obj_hold.description)
                            self.daily_queue_[obj] = True
                        else:
                            self.daily_queue_[obj] = False
                    else:
                        self.daily_queue_[obj] = True

            for obj in list(self.weekly_queue_):
                if not self.weekly_queue_[obj]:
                    if obj.time_hold.week == now.weekday():
                        if obj.time_hold.time.hour == now.hour:
                            if obj.time_hold.time.minute == now.minute:
                                self.notify_._send_msg(obj.obj_hold.name, obj.obj_hold.description)
                                self.weekly_queue_[obj] = True
                            else:
                                self.weekly_queue_[obj] = False
                        else:
                            self.weekly_queue_[obj] = True
                    else:
                        self.daily_queue_ = False

    def start(self):
        thread_ask = Thread(target=self._ask_what)
        thread_check = Thread(target=self._check_events)
        thread_check.start()
        thread_ask.start()


class Holder(object):
    def __init__(self, obj_hold, time_hold):
        self.obj_hold = obj_hold
        self.time_hold = time_hold

    def __str__(self):
        return self.obj_hold.name


class Event(object):
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __str__(self):
        return self.name


class WeekHolder(object):
    def __init__(self):
        self.week
        self.time


class Selectors:
    class Time(Enum):
        ONCE = 0
        DAILY = 1
        WEEKLY = 2

    class TimeType(Enum):
        DATE = 0
        TIME = 1


def check_up(dict_corr):
    converted = ""
    for key in list(dict_corr):
        converted += ", " + str(key) + " (" + dict_corr[key] + ")"

    while True:
        print("Please enter a your choice that is{}".format(converted))
        choice = input()
        try:
            choice = int(choice)
            if choice in list(dict_corr):
                break
            else:
                int("Hi")
        except:
            print("Please enter a valid input")
    return choice


def check_time(time_type, time=datetime.datetime(1, 1, 1, 1, 1, 1, 1)):
    while True:
        choice = input()
        try:
            if time_type == Selectors.TimeType.DATE:
                split = choice.split("/")
                month = int(split[0])
                day = int(split[1])
                if 0 < month < 13 and 0 < day < 32:
                    time = time.replace(month=month, day=day)
                else:
                    int("Hi")
                break
            if time_type == Selectors.TimeType.TIME:
                split = choice.split(":")
                hour = int(split[0])
                minute = int(split[1])
                if 0 < hour < 24 and 0 < minute < 60:
                    time = time.replace(hour=hour, minute=minute)
                else:
                    int("Hi")
                break
        except:
            print("Please enter a valid input")
    return time


def make_list(list_thing):
    return_obj = ""
    for obj in list(list_thing):
        return_obj += str(obj) + " " + str(obj.time_hold) + ", "
    return return_obj
