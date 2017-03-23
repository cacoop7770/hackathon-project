# import pygame as pg

class FutureEvent:
    def __init__(self, time_to_occur, event_to_occur):
        """
        an event that will happen in the future

        :param: time_to_occur: when the event should happen
        :type: time_to_occur: float
        :param: event_to_occur: the event that will happen
        :type: event_to_occur: pygame.event object
        """
        self.time = time_to_occur
        self.event = event_to_occur

    def __str__(self):
        return "Event( time={}, event={})".format(self.time, self.event)


class DelayedJoystick:
    def __init__(self):
        '''
        keep track of the buttons to be pressed in the future.
        Or keep track of the events to happen in the future
        '''
        self.events = []# future events
        self._queued_events = []# events queued to be deleted

    def add_event(self, event):
        '''
        Add an event to be occur in the future

        :param: event: the event to be added
        '''
        self.events.append(event)
        #print "Added event: ", str(event)

    def queue_event(self, event_time):
        """
        Queue events to be deleted (generally occurs if the event "expires"

        :param: event_time: queue all events that occur before this time by saving the event index
        :type: event_time: float
        
        :return: List of events that were queued
        :rtype: List
        """
        self.events = sorted(self.events, key = lambda x: x.time)
        for num in range(len(self.events)):
            event = self.events[num]
            print "Checking event: ", event, event_time
            if event.time < event_time:
                self._queued_events.append(num)
                print "queued event number: ", num
                print "queued event: ", event

        # having trouble with multiple numbers being duplicated in self._queued_events
        self._queued_events = list(set(self._queued_events))

        '''
        print "Queued events:"
        for event in self._queued_events:
            print str(event)

        print "Events:"
        for i in range(len(self.events)):
            event = self.events[i]
            print "*****" if i in self._queued_events else "", str(event)

        '''
        events_to_remove = []
        for num in self._queued_events:
            try:
                events_to_remove.append(self.events[num].event)
            except:
                #print "Event couldn't be added: ", num
                pass

        return events_to_remove

    def delete_queued_events(self):
        """
        Delete the queued events from the list of events
        """
        for event_num in self._queued_events:
            try:
                self.events.pop(event_num)
            except:
                #print "Couldn't delete event number: ", event_num
                pass

        

