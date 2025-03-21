import os
from clickhouse_driver import Client
import pandas as pd
import taipy as tp
from taipy.gui import Gui
import time


def query_clickhouse(query):
    """
    Create a ClickHouse client and executes the passed query with the client.

    Returns:
    - Query results
    """

    with Client(
        host="localhost",
        port=9000,
        user=os.environ.get("CLICKHOUSE_USER"),
        password=os.environ.get("CLICKHOUSE_PASSWORD"),
        database=os.environ.get("CLICKHOUSE_DB"),
    ) as client:
        result = client.execute(query) # list of Python Tuple, We need to convert to DataFrame for analyse
    return result


def get_all_messages():
    """
    Retrieves all messages from the user_messages table in ClickHouse.

    Returns:
    - list: A list containing all messages and their associated data.
    """

    query = """
    SELECT * FROM user_messages
    """

    return query_clickhouse(query)


def get_top_active_users():
    """
    Retrieves the top 5 active users based on message count from the user_messages table.

    Returns:
    - list: A list containing the usernames and their respective message counts, ordered by message count in descending order.
    """

    query = """
    SELECT username, COUNT(*) as message_count
    FROM user_messages
    GROUP BY username
    ORDER BY message_count DESC
    LIMIT 5;
    """

    return query_clickhouse(query)


def get_average_message_gap():
    """
    Computes the average time gap (in seconds) between consecutive messages in the user_messages table.

    Returns:
    - list: A list containing the average time gap in seconds.
    """

    query = """
    WITH OrderedMessages AS (
        SELECT received_at
        FROM user_messages
        ORDER BY received_at
    )

    , TimesArray AS (
        SELECT groupArray(received_at) AS times
        FROM OrderedMessages
    )

    , Differences AS (
        SELECT
            arrayMap((x, y) -> toInt32(y - x), arraySlice(times, 1, length(times)-1), arraySlice(times, 2)) AS diffs
        FROM TimesArray
    )

    SELECT AVG(difference) AS avg_time_gap_seconds
    FROM Differences
    ARRAY JOIN diffs AS difference;
    """

    return query_clickhouse(query)


# Taipy Interface
columns1 = ["username", "message", "received_at"]
columns2 = ["username", "message_count"]
columns3 = ["avg_time_gap_seconds", ]

page_content= """
## 📊 Messages Analysis from ClickHouse Database

### 🔹 All messages
<|{all_messages_df}|table|>
---
### 🔹 Top 5 Most Active Users
<|{top_users_df}|table|>
---
<|{top_users_df}|chart|x=username|y=message_count|type=bar|>
---
### 🔹 Mean Time Between Messages
📌 Mean time between messages: **<|{avg_gap_df}|table|>** seconds
"""

# ✅ Déclaration de l'interface avec une syntaxe compatible Taipy
def get_data():
    """
    Store value in-memory
    """

    all_messages_df = pd.DataFrame(get_all_messages(), columns=columns1)
    top_users_df = pd.DataFrame(get_top_active_users(), columns=columns2)
    avg_gap_df = pd.DataFrame(get_average_message_gap(), columns=columns3)
    #avg_gap = round(avg_gap_df.iloc[0, 0], 2)
    return all_messages_df, top_users_df, avg_gap_df


# Mettre à jour le contenu de la page en fonction des nouvelles données
def update_page_content():
    all_messages_df, top_users_df, avg_gap_df = get_data()

    page_content = f"""
    ## 📊 Messages Analysis from ClickHouse Database

    ### 🔹 All messages
    <|{all_messages_df}|table|>

    ---

    ### 🔹 Top 5 Most Active Users
    <|{top_users_df}|table|>

    ---

    <|{top_users_df}|chart|x=username|y=message_count|type=bar|>

    ---

    ### 🔹 Mean Time Between Messages
    📌 Mean time between messages: **<|{avg_gap_df.iloc[0, 0]}|text|>** seconds
    """

    return page_content

# Fonction qui sera utilisée pour créer la page avec le contenu initial
def create_page():
    page_content = update_page_content()
    page = Gui(page_content)
    return page




if __name__ == "__main__":
    from pprint import pprint as print
    print(get_average_message_gap())
    tp.Core().run()
    # Démarrer l'interface utilisateur
    page = create_page()

    # Démarrer la page dans le navigateur
    page.run()

    # Rafraîchissement périodique des données (toutes les 5 secondes dans cet exemple)
    while True:
        time.sleep(5)  # Attendre 5 secondes avant de rafraîchir les données
        page_content = update_page_content()  # Mettre à jour le contenu de la page
        page.update(page_content)  # Mettre à jour la page
