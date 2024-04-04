# class VectorClock:
#     def __init__(self):
#         self.clock = {}

#     def initialize(self, services):
#         for service in services:
#             self.clock[service] = 0

#     def increment(self, service):
#         if service in self.clock:
#             self.clock[service] += 1

#     def merge(self, other_clock):
#         for service, time in other_clock.clock.items():
#             self.clock[service] = max(self.clock.get(service, 0), time)

#     def get_clock(self):
#         return self.clock

class VectorClock:
    def __init__(self, initial_data=None):
        if initial_data is not None:
            self.clock = initial_data
        else:
            self.clock = {}

    def initialize(self, services):
        for service in services:
            self.clock[service] = 0

    def increment(self, service):
        self.clock[service] = self.clock.get(service, 0) + 1

    def merge(self, other_clock):
        for service, time in other_clock.items():
            self.clock[service] = max(self.clock.get(service, 0), time)

    def get_clock(self):
        return self.clock
