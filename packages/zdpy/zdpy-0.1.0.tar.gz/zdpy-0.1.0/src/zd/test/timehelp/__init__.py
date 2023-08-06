
import re
import pytz
from datetime import datetime
from dateutil.parser import parse as dateutil_parser


_base_date_time_fmt = '%Y-%m-%dT%H:%M:%S.%f'
_base_date_time_fmt_no_decimals = '%Y-%m-%dT%H:%M:%S'
re_utc_format = re.compile(r'\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}.?(\d*)Z')


def slow_catchall_to_utc_parser(time_str):
    parsed_dt = dateutil_parser(time_str)
    return parsed_dt.astimezone(pytz.utc) if parsed_dt.tzinfo is not None else parsed_dt.replace(tzinfo=pytz.utc)


def _is_utc_like_format(time_str):
    return len(re_utc_format.findall(time_str)) > 0


def to_utc(time_str, fmt=None, slow_catchall=slow_catchall_to_utc_parser):
    if not time_str:
        return None

    if fmt:
        return datetime.strptime(time_str, fmt).replace(tzinfo=pytz.utc)
    elif _is_utc_like_format(time_str):
        ts_no_z = time_str.replace('Z', '').replace(' ', 'T')
        if '.' not in time_str:
            return to_utc(ts_no_z, fmt=_base_date_time_fmt_no_decimals)
        else:
            return to_utc(ts_no_z[:26], fmt=_base_date_time_fmt)
    else:
        return slow_catchall(time_str)


def to_utc_str(time_str, source_fmt=None):
    return (
        None if not time_str
        else to_utc(time_str, fmt=source_fmt).strftime(_base_date_time_fmt)[:26] + 'Z'
    )
