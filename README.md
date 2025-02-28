# 📦 Backup My SQLite

Simple Python Script to **Backup** your SQLite3 Database.

This Script probably **works for other filetypes** too, however, it's made for SQLite Databases

Use [`crontab`](https://crontab.guru) for scheduling.

> **Note**: On 💠 Windows, there is no Crontab. Here is a [different approach](https://docs.active-directory-wp.com/Usage/How_to_add_a_cron_job_on_Windows/Scheduled_tasks_and_cron_jobs_on_Windows/index.html)

_Tested on Python **3.12.2**_

## ⚙️ Config

Stored in the same directory as the script. It's called `config.yaml`

| Key         | Default       | Explanation                                                                 |
|-------------|---------------|-----------------------------------------------------------------------------|
| `db`        | `- sqlite.db`   | Stores the path where the databases to be backed up is located (List!).              |
| `backup_dir`| `./backups/`  | Sets the directory where backups are stored.                                |
| `max_backups`| `5`          | Sets the maximum number of backups. Set to `-1` for no automatic deletion.  |
| `compression`| `-1`         | Sets the compression level. `-1` to disable compression, `1-9` for levels.  |
| `silent`    | `false`       | If set to `true`, suppresses output messages.                               |
