import csv
from datetime import datetime, timedelta

YEAR = 2022
MONDAY_LOCATION = 'Woodley Village Hall, Romsey'
THURSDAY_LOCATION = 'Romsey Sports Centre, Southampton Road, Romsey'
TRACK_LOCATION = 'The Mountbatten School, Whitenap Lane, Romsey'
FRITHAM_LOCATION = 'The Royal Oak, Fritham, Lyndhurst'


def guess_location(description, day):
    if 'track' in description.lower():
        return TRACK_LOCATION
    elif 'fritham' in description.lower():
        return FRITHAM_LOCATION
    elif day == 'Monday':
        return MONDAY_LOCATION
    else:
        return THURSDAY_LOCATION


def debs_replacer(session_leader):
    return session_leader.replace('Debs', 'Deborah')


with open('planner.csv', newline='') as csvfile:
    reader = csv.reader(csvfile)
    counter = 0
    session_dict = {}
    monday_date = None
    thursday_date = None
    for row in reader:
        counter += 1
        if counter <= 2:
            continue
        elif counter % 2 != 0:
            monday_date = (datetime.strptime(row[0], f'%d %b').date()).replace(year=YEAR)
            thursday_date = monday_date + timedelta(days=3)
            groups_12_session = row[1]
            groups_34_session = row[2]
            thursday_session = row[3]
            session_dict[monday_date] = {
                '12': {'session': groups_12_session, 'location': guess_location(groups_12_session, 'Monday')},
                '34': {'session': groups_34_session, 'location': guess_location(groups_34_session, 'Monday')}
            }
            session_dict[thursday_date] = {
                'all': {'session': thursday_session, 'location': guess_location(thursday_session, 'Thursday')}
            }
        else:
            groups_12_leader = debs_replacer(row[1])
            groups_34_leader = debs_replacer(row[2])
            thursday_leader = debs_replacer(row[3])
            session_dict[monday_date]['12']['leader'] = groups_12_leader
            session_dict[monday_date]['34']['leader'] = groups_34_leader
            session_dict[thursday_date]['all']['leader'] = thursday_leader

    with open('gcal.csv', 'w', newline='') as csvfile:
        fieldnames = ['Subject', 'Start Date', 'Start Time', 'End Date', 'End Time', 'Description', 'Location']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for session_date, session_details_dict in session_dict.items():
            for session_group, session_details in session_details_dict.items():
                if session_details['leader'].lower() == 'no club':
                    continue

                if session_group == 'all':
                    session_prefix = 'All Groups'
                if session_group == '12':
                    session_prefix = 'Groups 1&2'
                if session_group == '34':
                    session_prefix = 'Groups 3&4'

                writer.writerow(
                    {
                        'Subject': f'{session_prefix}: {session_details["session"]}',
                        'Start Date': session_date.strftime("%d/%m/%y"),
                        'Start Time': '6:30 PM',
                        'End Date': session_date.strftime("%d/%m/%y"),
                        'End Time': '7:30 PM',
                        'Description': f'Session Leader: {session_details["leader"]}',
                        'Location': session_details['location']
                    }
                )
