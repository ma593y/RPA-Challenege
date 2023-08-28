from robocorp.tasks import task
from Libraries.NewYorkTimes import NewYorkTimes

@task
def new_york_times_automation():
    try:
        new_york_times = NewYorkTimes()
        new_york_times.open_website_and_search()
        new_york_times.sort_by_newest()
        new_york_times.select_news_sections()
        new_york_times.select_date_range()
        new_york_times.extract_searched_results()
    except Exception as e:
        print(f"Exception: {e}")
    finally:
        new_york_times.close_all()
