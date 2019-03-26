#!/usr/bin/python

import sys
from datetime import date
from operator import attrgetter


class Event:
    def __init__(self, name, date, action):
        self.name = name
        self.date = date
        self.action = action

    def __str__(self):
        return self.name + ' ' + str(self.date) + ' ' + self.action


class Period:
    def __init__(self, start_date, end_date, tenants):
        self.start_date = start_date
        self.end_date = end_date
        self.tenants = list(tenants)

    def __str__(self):
        return str(self.start_date) + ' ' + str(self.end_date) + ' ' + str(
            self.tenants)


def make_date(date_string):
    date_components = date_string.split('-')
    date_year = int(date_components[0])
    date_month = int(date_components[1])
    date_day = int(date_components[2])
    return date(date_year, date_month, date_day)


tenants = {
    #'tom' : [date(2012, 4, 4), None],
    #'kat' : [None, None],
    'tom': [None, date(2012, 8, 1)],
    'nathan': [date(2011, 6, 25), None],
    'rohan': [date(2011, 11, 12), None]
    #'mehdi' : [date(2011, 7, 9), date(2011, 8, 27)],
    #'houman' : [date(2011, 8, 27), date(2011, 9, 18)],
}

total_amount = float(sys.argv[1])
total_start = sys.argv[2]
total_end = sys.argv[3]

total_start_date = make_date(total_start)
total_end_date = make_date(total_end)
total_period = (total_end_date - total_start_date).days

valid_tenants = []

for k, v in tenants.iteritems():
    if ((v[1] is not None) and (v[1] < total_start_date)):
        continue
    if ((v[0] is not None) and (v[0] > total_end_date)):
        continue
    valid_tenants.append(k)

events = []
curr_tenants = []

for tenant in valid_tenants:
    tenant_start = tenants[tenant][0]
    tenant_end = tenants[tenant][1]
    if tenant_start is None or tenant_start < total_start_date:
        curr_tenants.append(tenant)
    if tenant_start is not None and tenant_start > total_start_date and tenant_start < total_end_date:
        events.append(Event(tenant, tenant_start, 'start'))
    if tenant_end is not None and tenant_end < total_end_date and tenant_end > total_start_date:
        events.append(Event(tenant, tenant_end, 'end'))

events.sort(key=attrgetter('date'))
periods = []
curr_period = Period(total_start_date, None, curr_tenants)

for event in events:
    curr_period.end_date = event.date
    periods.append(curr_period)
    if (event.action == 'end'):
        curr_tenants.remove(event.name)
    if (event.action == 'start'):
        curr_tenants.append(event.name)
    curr_period = Period(event.date, None, curr_tenants)

curr_period.end_date = total_end_date
periods.append(curr_period)

tenant_amounts = {}

for tenant in tenants.keys():
    tenant_amounts[tenant] = 0.0

for period in periods:
    period_share = ((period.end_date - period.start_date).days * total_amount
                    ) / (total_period * len(period.tenants))
    for tenant in period.tenants:
        tenant_amounts[tenant] += period_share

for k, v in tenant_amounts.iteritems():
    print '%(k)-10s %(v)6.2f' % {'k': k, 'v': round(v, 2)}
