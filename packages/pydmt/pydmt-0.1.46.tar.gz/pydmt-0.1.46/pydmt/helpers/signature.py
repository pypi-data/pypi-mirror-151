import datetime


def get_copyright_years(project_year_started):
    # return ", ".join(map(str, range(int(project_year_started), datetime.datetime.now().year + 1)))
    general_current_year = datetime.datetime.now().year
    if str(general_current_year) == project_year_started:
        return general_current_year
    return f"{project_year_started}-{general_current_year}"
