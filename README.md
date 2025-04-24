### Store Monitoring Backend

This project provides a backend solution for monitoring restaurant uptime/downtime based on hourly status logs, store business hours, and their respective timezones. Restaurant owners can generate reports highlighting operational consistency, especially during business hours.

## Tech Stack

- Python
- Django + Django REST Framework
- PostgreSQL
- Git LFS to handle large CSV files

## API Endpoints

**1. /trigger_report/ (GET)**

Generates a new uptime/downtime report for a given store.

Request:

```
GET /api/stores/<store_id>/trigger_report/

```

Response:

```
{
  "report_id": "1"
}

```

**2. /get_report/ (POST)**

Polls for report status or downloads the CSV if ready.

Request:

```
{
  "report_id": "1"
}

```

Response:

```
{
    "report_url": "C:\\Users\\Vinod Kumar\\Desktop\\Store_Monitoring_Backend\\store\\media/reports/4.csv",
    "status": "Complete"
}
```

## Uptime/Downtime Logic

Observations

- Logs in store_status.csv contain UTC timestamps of store status (active/inactive).-
- Business hours in menu_hours.csv are in local time.-
- Timezones are provided in timezones.csv.

## Logic Breakdown

- Timezone Conversion: Convert UTC timestamp_utc to the local time of each store using pytz.

- Business Hours Mapping:

  - If business hours missing → assume 24/7.
  - Generate business hour windows for last hour, day, and week.

- Interpolation:

  - For a given business window, if status logs are sparse, fill gaps using:

    - Forward fill based on last known status.
    - Linear approximation over evenly spaced intervals (e.g., 1-min granularity).

- Calculation:

  - Iterate over every minute of the window and track whether store was active or inactive.-
  - Count total minutes/hours spent in each state.

### Example:

```
A store with:

    Business hours on Monday: 9AM to 12PM

    Logs:

        10:00 AM → active

        11:30 AM → inactive

Using forward fill:

    9:00–10:00 → no data → assume active

    10:00–11:30 → active

    11:30–12:00 → inactive

Uptime: 2.5 hours, Downtime: 0.5 hours
```

## Sample Output

.csv file output google drive link : [Link](https://drive.google.com/file/d/1JlgzUPTvT_G9VKLT2vqG5CSba83K9bI_/view?usp=sharing)

## Demo Video

🔗 [Watch 3-min demo video](https://drive.google.com/file/d/1EufdhSa5LsNt_onqz5biB3nN_fzAiWYL/view?usp=sharing)

## Improvements and Future Work

- Use Celery with Redis to handle asynchronous report generation
- Add unit and integration tests
- Support real-time ingestion of polling data (WebSockets or Kafka)
- Add filters for stores, date ranges, or time slots in the API.
