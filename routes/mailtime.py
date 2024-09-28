from flask import Flask, request, jsonify
from datetime import datetime, timedelta, time
from zoneinfo import ZoneInfo
import re

from routes import app

def parse_iso_datetime(dt_str):
    try:
        return datetime.fromisoformat(dt_str)
    except ValueError:
        raise ValueError(f"Invalid datetime format: {dt_str}")

def get_base_subject(subject):
    # Remove all leading "RE: " prefixes, case-insensitive
    return re.sub(r'^(?i)(RE:\s)+', '', subject).strip()

def is_working_day(dt, user):
    # Monday is 0 and Sunday is 6
    return dt.weekday() < 5  # 0-4 are Monday to Friday

def get_working_hours_for_day(dt, user):
    # Returns the start and end datetime objects for the working hours on the given day
    work_start = time(user['officeHours']['start'], 0, 0)
    work_end = time(user['officeHours']['end'], 0, 0)
    work_start_dt = datetime.combine(dt.date(), work_start).replace(tzinfo=dt.tzinfo)
    work_end_dt = datetime.combine(dt.date(), work_end).replace(tzinfo=dt.tzinfo)
    return work_start_dt, work_end_dt

def compute_response_time(user, received_time, response_time):
    """
    Computes the total working time in seconds between received_time and response_time
    considering the user's working hours and weekends.
    Both received_time and response_time are timezone-aware datetime objects
    in the user's local timezone.
    """
    if received_time >= response_time:
        return 0

    total_seconds = 0
    current_day = received_time.date()
    end_day = response_time.date()
    one_day = timedelta(days=1)

    while current_day <= end_day:
        current_datetime = datetime.combine(current_day, time(0, 0, 0)).replace(tzinfo=received_time.tzinfo)
        if is_working_day(current_datetime, user):
            work_start_dt, work_end_dt = get_working_hours_for_day(current_datetime, user)

            # Determine the start of the working period on this day
            if current_day == received_time.date():
                period_start = max(received_time, work_start_dt)
            else:
                period_start = work_start_dt

            # Determine the end of the working period on this day
            if current_day == response_time.date():
                period_end = min(response_time, work_end_dt)
            else:
                period_end = work_end_dt

            if period_start < period_end:
                seconds = (period_end - period_start).total_seconds()
                total_seconds += seconds

        current_day += one_day

    return int(total_seconds)

@app.route('/mailtime', methods=['POST'])
def mailtime():
    data = request.get_json()

    emails = data.get('emails', [])
    users = data.get('users', [])

    # Validate input data
    if not isinstance(emails, list) or not isinstance(users, list):
        return jsonify({"error": "Invalid input format. 'emails' and 'users' should be lists."}), 400

    # Create a user lookup dictionary
    user_dict = {}
    for user in users:
        name = user.get('name')
        office_hours = user.get('officeHours')
        if not name or not office_hours:
            return jsonify({"error": f"User entry missing 'name' or 'officeHours': {user}"}), 400
        timezone = office_hours.get('timeZone')
        start = office_hours.get('start')
        end = office_hours.get('end')
        if timezone is None or start is None or end is None:
            return jsonify({"error": f"User's officeHours missing 'timeZone', 'start', or 'end': {user}"}), 400
        try:
            ZoneInfo(timezone)  # Validate timezone
        except Exception:
            return jsonify({"error": f"Invalid timezone: {timezone} for user: {name}"}), 400
        user_dict[name] = user

    # Group emails into threads based on base subject
    threads = {}
    for email in emails:
        subject = email.get('subject')
        sender = email.get('sender')
        receiver = email.get('receiver')
        time_sent_str = email.get('timeSent')

        if not subject or not sender or not receiver or not time_sent_str:
            return jsonify({"error": f"Email entry missing required fields: {email}"}), 400

        base_subject = get_base_subject(subject)
        if base_subject not in threads:
            threads[base_subject] = []
        threads[base_subject].append(email)

    response_times = {}
    response_counts = {}

    for thread_subject, thread_emails in threads.items():
        # Sort emails in the thread by timeSent
        try:
            sorted_emails = sorted(thread_emails, key=lambda x: parse_iso_datetime(x['timeSent']))
        except ValueError as ve:
            return jsonify({"error": str(ve)}), 400

        # Iterate through the thread to find replies
        for i in range(1, len(sorted_emails)):
            prev_email = sorted_emails[i-1]
            current_email = sorted_emails[i]

            sender = current_email['sender']
            receiver = current_email['receiver']

            # Ensure sender exists in user_dict
            if sender not in user_dict:
                return jsonify({"error": f"Sender '{sender}' not found in users list."}), 400

            user = user_dict[sender]

            # Parse the received time (time when sender received the email)
            try:
                received_time_utc = parse_iso_datetime(prev_email['timeSent'])
            except ValueError as ve:
                return jsonify({"error": str(ve)}), 400

            received_time = received_time_utc.astimezone(ZoneInfo(user['officeHours']['timeZone']))

            # Parse the response time (time when sender sent the reply)
            try:
                response_time_utc = parse_iso_datetime(current_email['timeSent'])
            except ValueError as ve:
                return jsonify({"error": str(ve)}), 400

            response_time = response_time_utc.astimezone(ZoneInfo(user['officeHours']['timeZone']))

            # Compute response time in seconds
            resp_time_sec = compute_response_time(user, received_time, response_time)

            if sender not in response_times:
                response_times[sender] = 0
                response_counts[sender] = 0

            response_times[sender] += resp_time_sec
            response_counts[sender] += 1

    # Compute average response time
    average_response = {}
    for user in response_times:
        avg = response_times[user] // response_counts[user]
        average_response[user] = avg

    return jsonify({"response": average_response})

