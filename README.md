
## Setup the table In Clikhouse

Now we need to setup a table named `user_messages` to store our messages which will store
the `username`, `message`, and `received_at`!

❓ Workout how to connect to the db and create the table
- Connect to a db with clikhouse is similarly like postgres connecion and the `psql` command, but here we use this one ``clickhouse-client``.

````
clickhouse-client --host localhost --port 9000 -u "$CLICKHOUSE_USER" --password "$CLICKHOUSE_PASSWORD" --database "$CLICKHOUSE_DB"
````
- Create table of user

A good starting point for creating table are the [docs](https://clickhouse.com/docs/en/sql-reference/statements/create/table) we can find.

<details>
<summary markdown='span'>💡 Solution </summary>

```sql
CREATE TABLE IF NOT EXISTS chat.user_messages (
    username String,
    message String,
    received_at DateTime
) ENGINE = MergeTree() ORDER BY received_at
```

</details>

Now we are ready to begin using rabbitmq to automate the insertions!


## Visualize Analytic Data in real-time with either ``Streamlit`` or ``Taipy``.

We should use ``Taipy`` because of its capabilities to manage ``multithreads`` tasks.

Here a break down [documentation link](https://docs.taipy.io/en/latest/userman/run-deploy/deploy/docker/) to learn how to deploy taipy app.

But we'll use ``Sreamlit`` for this demo.
There is the [streamlit real-time data](https://blog.streamlit.io/how-to-build-a-real-time-live-dashboard-with-streamlit/) visualization version.
