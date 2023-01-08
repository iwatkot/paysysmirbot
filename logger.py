from datetime_handler import get_now


def write_log(log_file, event, user_id=None, user_name=None, result=None):
    log_entry = f"--{get_now()}--[{event}]--"
    if user_id is not None and user_name is not None:
        log_entry += f"id({user_id})--name({user_name})--\n"
    elif result is not None:
        log_entry += f"result({result})--\n"
    with open(log_file, 'a') as lf:
        lf.write(log_entry)
