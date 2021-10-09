from win10toast import ToastNotifier
from enum import Enum
from datetime import datetime
from threading import Thread


class Notification(object):
    def __init__(self, signature, icon):
        self.tnotif_ = ToastNotifier()
        self.signature_ = signature
        self.icon_ = icon

    def _send_msg(self, title, msg):
        print("Sending...")
        self.tnotif_.show_toast(title=self.signature_+" - "+title, msg=msg, icon_path=self.icon_, duration=10)


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
            week = set_time = check_up({0: "Monday", 1: "Tuesday", 2: "Wednesday", 3: "Thursday", 4: "Friday", 5: "Saturday", 6: "Sunday"})
            print("Please enter what date this event will occur in format h:m")
            set_time = check_time(Selectors.TimeType.TIME)
            self.weekly_queue_[Holder(Event(event_name, event_des), WeekHolder(week, set_time))]

    def _remove_event(self):
        if self.weekly_queue_ == {} and self.daily_queue_ == {} and self.once_queue_ == {}:
            print("There is nothing in your schedule.")
        else:
            print("Weekly events: {}".format(conversion_list(self.weekly_queue_)))
            print("Daily events: {}".format(conversion_list(self.daily_queue_)))
            print("One time events: {}".format(conversion_list(self.once_queue_)))

            print("Please type the name of the event you want to remove:")
            remove = input()
            if remove in self.weekly_queue_:
                for i in range(len(self.weekly_queue_)):
                    if remove == str(self.weekly_queue_[i]):
                        self.weekly_queue_.remove(i)
                        break
            elif remove in self.daily_queue_:
                for i in range(len(self.daily_queue_)):
                    if remove == str(self.daily_queue_[i]):
                        self.daily_queue_.remove(i)
                        break
            elif remove in self.once_queue_:
                for i in range(len(self.once_queue_)):
                    if remove == str(self.once_queue_[i]):
                        self.once_queue_.remove(i)
                        break

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
                    print("Weekly events: {}".format(conversion_list(self.weekly_queue_)))
                    print("Daily events: {}".format(conversion_list(self.daily_queue_)))
                    print("One time events: {}".format(conversion_list(self.once_queue_)))

    def _check_events(self):
        while True:
            now = datetime.now()
            for obj in list(self.once_queue_):
                if obj.time_hold.month == now.month:
                    print("SUCCESS_Mon")
                    if obj.time_hold.day == now.day:
                        print("SUCCESS_DAY")
                        if obj.time_hold.hour == now.hour:
                            print("SUCCESS_HOUR")
                            print(obj.time_hold.minute)
                            if obj.time_hold.minute == now.minute:
                                print("SUCCESS_MIN")
                                self.notify_._send_msg(obj.obj_hold.name, obj.obj_hold.description)
                                del self.once_queue_[obj]

            for obj in self.daily_queue_.keys():
                if not self.daily_queue_[obj]:
                    if obj.time_hold.hour == now.hour:
                        if obj.time_hold.minute == now.minute:
                            self.notify_._send_msg(obj.obj_hold.name, obj.obj_hold.description)
                            self.daily_queue_ = True
                        else:
                            self.daily_queue_ = False
                    else:
                        self.daily_queue_ = True

            for obj in self.weekly_queue_.keys():
                if not self.daily_queue_[obj]:
                    if obj.time_hold.week == now.weekday():
                        if obj.time_hold.time.hour == now.hour:
                            if obj.time_hold.time.minute == now.minute:
                                self.notify_._send_msg(obj.obj_hold.name, obj.obj_hold.description)
                                self.daily_queue_ = True
                            else:
                                self.daily_queue_ = False
                        else:
                            self.daily_queue_ = True
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
    cleared = False
    error_code = ""
    converted = ""
    for key in dict_corr.keys():
        converted += ", " + str(key) + " (" + dict_corr[key] + ")"
    while not cleared:
        print("Please enter a your choice that is{}".format(converted))
        choice = input()
        if choice.isnumeric():
            choice = int(choice)
            if choice in dict_corr.keys():
                cleared = True
                error_code = ""
            else:
                error_code = "Please enter a number in {}".format(dict_corr.keys)
        else:
            error_code = "Enter a number"
        if error_code != "":
            print(error_code)
    return choice


def check_time(time_type, time=datetime(1, 1, 1, 1, 1, 1, 1)):
    now = time
    cleared = False
    error_code = ""
    if time_type == Selectors.TimeType.DATE:
        while not cleared:
            choice = input()
            if "/" in choice:
                split = choice.split("/")
                if len(split) == 2:
                    month = split[0]
                    day = split[1]
                    if month.isnumeric() and day.isnumeric():
                        month = int(month)
                        day = int(day)
                        if 0 < month < 13 and 0 < day < 32:
                            now.replace(month=month)
                            now.replace(day=day)
                            print(now)
                            error_code = ""
                            cleared = True
                        else:
                            error_code = "Enter a valid date."
                    else:
                        error_code = "Please make your characters numbers."
                else:
                    error_code = "Please enter two values"
            else:
                error_code = "Please comply with the formatting options"
            if error_code != "":
                print(error_code)
    if time_type == Selectors.TimeType.TIME:
        while not cleared:
            choice = input()
            if ":" in choice:
                split = choice.split(":")
                if len(split) == 2:
                    hour = split[0]
                    minute = split[1]
                    if hour.isnumeric() and minute.isnumeric():
                        hour = int(hour)
                        minute = int(minute)
                        if 0 < hour < 24 and 0 < minute < 60:
                            print("Setting...")
                            now.replace(hour=hour)
                            now.replace(minute=minute)
                            now.replace(second=0)
                            print(now)
                            error_code = ""
                            cleared = True
                        else:
                            error_code = "Enter a valid date."
                    else:
                        error_code = "Please make your characters numbers."
                else:
                    error_code = "Please enter two values"
            else:
                error_code = "Please comply with the formatting options"
            if error_code != "":
                print(error_code)
    return now


def conversion_list(list_thing):
    return_obj = ""
    for obj in list_thing.keys():
        return_obj += str(obj) + ", "
    return return_obj
