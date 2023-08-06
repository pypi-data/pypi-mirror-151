import datetime


def get_copyright_years_long(project_year_started):
    general_current_year = datetime.datetime.now().year
    return ", ".join(map(str, range(int(project_year_started), general_current_year)))


def get_copyright_years_short(project_year_started):
    general_current_year = datetime.datetime.now().year
    if general_current_year == project_year_started:
        return general_current_year
    return f"{project_year_started}-{general_current_year}"
