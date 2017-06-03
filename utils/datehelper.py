from datetime import datetime, date, timedelta
from calendar import monthrange


def from_str_to_date(datestr, strpattern):
    date_result = datetime.strptime(datestr, strpattern)
    return date_result


def from_date_to_str(date, strpattern):
    date_result = datetime.strftime(date, strpattern)
    return date_result


def today():
    return date.today()


def prev_next_day(date):
    result = {}
    result['prev_day'] = date - timedelta(days=1)
    result['next_day'] = date + timedelta(days=1)
    return result


def start_end_current_week():
    result = {}
    result['start_week'] = datetime.today() - timedelta(
            days=datetime.today().weekday())
    result['end_week'] = result['start_week'] + timedelta(days=6)
    return result


def prev_week_start_end(start_current_week):
    result = {}
    result['prev_week_end'] = start_current_week - timedelta(days=1)
    result['prev_week_start'] = start_current_week - timedelta(days=7)
    return result


def next_week_start_end(end_current_week):
    result = {}
    result['next_week_start'] = end_current_week + timedelta(days=1)
    result['next_week_end'] = end_current_week + timedelta(days=7)
    return result


def start_end_current_month():
    result = {}
    monthdays = monthrange(datetime.today().year, datetime.today().month)
    result['start_month'] = date(
            datetime.today().year,
            datetime.today().month,
            1)
    result['end_month'] = date(
            datetime.today().year,
            datetime.today().month,
            monthdays[1])
    return result


def prev_month_start_end(start_current_month):
    result = {}
    result['prev_month_end'] = start_current_month - timedelta(days=1)
    result['prev_month_start'] = date(
            result['prev_month_end'].year,
            result['prev_month_end'].month,
            1)
    return result


def next_month_start_end(end_current_month):
    result = {}
    result['next_month_start'] = end_current_month + timedelta(days=1)
    next_month_days = monthrange(
            result['next_month_start'].year,
            result['next_month_start'].month)
    result['next_month_end'] = end_current_month + timedelta(
            days=next_month_days[1])
    return result


def start_end_current_year():
    result = {}
    result['start_year'] = date(datetime.today().year, 1, 1)
    result['end_year'] = date(datetime.today().year, 12, 31)
    return result


def prev_year_start_end(start_current_year):
    result = {}
    result['prev_year_end'] = start_current_year - timedelta(days=1)
    result['prev_year_start'] = date(result['prev_year_end'].year, 1, 1)
    return result


def next_year_start_end(end_current_year):
    result = {}
    result['next_year_start'] = end_current_year + timedelta(days=1)
    result['next_year_end'] = date(result['next_year_start'].year, 12, 31)
    return result


def days_income_expense_view():
    days = {}
    days['today'] = from_date_to_str(today(), '%Y-%m-%d')
    start_end_week = start_end_current_week()
    days['start_week'] = from_date_to_str(
            start_end_week['start_week'], '%Y-%m-%d')
    days['end_week'] = from_date_to_str(
            start_end_week['end_week'], '%Y-%m-%d')
    start_end_month = start_end_current_month()
    days['start_month'] = from_date_to_str(
            start_end_month['start_month'], '%Y-%m-%d')
    days['end_month'] = from_date_to_str(
            start_end_month['end_month'], '%Y-%m-%d')
    start_end_year = start_end_current_year()
    days['start_year'] = from_date_to_str(
            start_end_year['start_year'], '%Y-%m-%d')
    days['end_year'] = from_date_to_str(
            start_end_year['end_year'], '%Y-%m-%d')
    return days


def days_income_expense_daily_view(current_day):
    current_day = datetime.strptime(current_day, '%Y-%m-%d')
    days = {}
    days['current_day'] = from_date_to_str(current_day, '%d %b %Y')
    prev_next_days = prev_next_day(current_day)
    days['prev_day'] = from_date_to_str(
            prev_next_days['prev_day'], '%Y-%m-%d')
    days['next_day'] = from_date_to_str(prev_next_days['next_day'], '%Y-%m-%d')
    return days


def days_income_expense_weekly_view(start_current_week, end_current_week):
    start_date = from_str_to_date(start_current_week, '%Y-%m-%d')
    end_date = from_str_to_date(end_current_week, '%Y-%m-%d')
    days = {}

    days['current_week_start'] = from_date_to_str(
            start_date, '%d %b %Y'
    )
    days['current_week_end'] = from_date_to_str(
            end_date, '%d %b %Y'
    )
    prev_week_start_end_days = prev_week_start_end(start_date)
    days['prev_week_end'] = from_date_to_str(
            prev_week_start_end_days['prev_week_end'], '%Y-%m-%d'
    )
    days['prev_week_start'] = datetime.strftime(
            prev_week_start_end_days['prev_week_start'], '%Y-%m-%d'
    )
    next_week_start_end_days = next_week_start_end(end_date)
    days['next_week_start'] = from_date_to_str(
            next_week_start_end_days['next_week_start'], '%Y-%m-%d'
    )
    days['next_week_end'] = from_date_to_str(
            next_week_start_end_days['next_week_end'], '%Y-%m-%d'
    )
    return days


def days_income_expense_monthly_view(start_current_month, end_current_month):
    start_date = from_str_to_date(start_current_month, '%Y-%m-%d')
    end_date = from_str_to_date(end_current_month, '%Y-%m-%d')
    days = {}

    days['current_month_start'] = from_date_to_str(
            start_date, '%d %b %Y'
    )
    days['current_month_end'] = from_date_to_str(
            end_date, '%d %b %Y'
    )
    prev_month_start_end_dates = prev_month_start_end(start_date)
    days['prev_month_end'] = from_date_to_str(
            prev_month_start_end_dates['prev_month_end'], '%Y-%m-%d'
    )
    days['prev_month_start'] = from_date_to_str(
            prev_month_start_end_dates['prev_month_start'], '%Y-%m-%d'
    )
    next_month_start_end_dates = next_month_start_end(end_date)
    days['next_month_start'] = from_date_to_str(
            next_month_start_end_dates['next_month_start'], '%Y-%m-%d'
    )
    days['next_month_end'] = from_date_to_str(
            next_month_start_end_dates['next_month_end'], '%Y-%m-%d'
    )
    return days


def days_income_expense_yearly_view(start_current_year, end_current_year):
    start_date = from_str_to_date(start_current_year, '%Y-%m-%d')
    end_date = from_str_to_date(end_current_year, '%Y-%m-%d')
    days = {}

    days['current_year_start'] = from_date_to_str(
            start_date, '%d %b %Y'
    )
    days['current_year_end'] = from_date_to_str(
            end_date, '%d %b %Y'
    )
    prev_year_start_end_dates = prev_year_start_end(start_date)
    days['prev_year_end'] = from_date_to_str(
            prev_year_start_end_dates['prev_year_end'], '%Y-%m-%d'
    )
    days['prev_year_start'] = from_date_to_str(
            prev_year_start_end_dates['prev_year_start'], '%Y-%m-%d'
    )
    next_year_start_end_dates = next_year_start_end(end_date)
    days['next_year_start'] = from_date_to_str(
            next_year_start_end_dates['next_year_start'], '%Y-%m-%d'
    )
    days['next_year_end'] = from_date_to_str(
            next_year_start_end_dates['next_year_end'], '%Y-%m-%d'
    )
    return days
