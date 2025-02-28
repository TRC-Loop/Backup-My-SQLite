# 📦 Backup My SQLite

Simple Python Script to **Backup** your SQLite3 Database.

This Script probably **works for other filetypes** too, however, it's made for SQLite Databases

Use [`crontab`](https://crontab.guru) for scheduling.

> **Note**: On 💠 Windows, there is no Crontab. Here is a [different approach](https://docs.active-directory-wp.com/Usage/How_to_add_a_cron_job_on_Windows/Scheduled_tasks_and_cron_jobs_on_Windows/index.html)

## 📋 Flags

`silent` for no output.

## ⚙️ Config

Stored in the same directory as the script. It's called `config.yaml`

| Key         | Default       | Explanation                                                                 |
|-------------|---------------|-----------------------------------------------------------------------------|
| `db`        | `sqlite.db`   | Stores the path where the database to be backed up is located.              |
| `backup_dir`| `./backups/`  | Sets the directory where backups are stored.                                |
| `max_backups`| `5`          | Sets the maximum number of backups. Set to `-1` for no automatic deletion.  |
