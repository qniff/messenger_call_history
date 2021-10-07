import json
import csv
import datetime
from types import SimpleNamespace


def get_calls(filename):
    with open(filename, 'r') as file:
        data = file.read()

    # Parse JSON into an object with attributes corresponding to dict keys.
    x = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
    messages = x.messages

    calls = []
    for message in messages:
        if message.type == "Call":
            calls.append(message)

    return calls

def remove_missed_calls(calls):
    updated_calls = []
    for call in calls:
        if not 'missed' in call.content:
            updated_calls.append(call)
    return updated_calls

def main():
    # collect all the calls
    calls = get_calls('message_1.json')
    calls = calls + get_calls('message_2.json')
    calls = calls + get_calls('message_3.json')
    calls = calls + get_calls('message_4.json')

    # remove missed calls
    calls = remove_missed_calls(calls)

    # create csv file and writer
    f = open('call_history.csv', 'w', newline='')
    writer = csv.writer(f)

    # set up a header
    header = ['Date', 'Time', 'Content', 'Duration']
    writer.writerow(header)

    for call in calls:

        # get datetime
        datetimeobj = datetime.datetime.fromtimestamp(call.timestamp_ms/1000.0)
        # get date
        date = str(datetimeobj.day).zfill(2) + '/' + str(datetimeobj.month).zfill(2) + '/' + str(datetimeobj.year)
        # get time
        time = str(datetimeobj.hour).zfill(2) + ':' + str(datetimeobj.minute).zfill(2) + ':' + str(datetimeobj.second).zfill(2)

        # get content
        content = call.content

        # get duration
        duration = conversion = datetime.timedelta(seconds=call.call_duration)

        # build row
        row = [date, time, content, duration]
        writer.writerow(row)



main()

