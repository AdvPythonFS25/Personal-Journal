## Where Exception handling was added
I added a try-except block in the `entry_stats` view in `views.py`. This function groups journal entries by month and generates labels and counts for a Chart.js graph.

## Why 
The view relies on date fields and data aggregation, which can fail if the data is irregular or incomplete. For example:
- `date_created` might be `None`
- The database query could fail
- Formatting `None` as a date using `strftime` will raise an exception

By handling exceptions, a site crash can be avoided.

## Future Improvements
User friendly UI could be added at a later date.