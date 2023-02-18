
import os
import requests
from discordwebhook import Discord


database_ID = "9dd2f20bdb4745fcbce08ca569e6f40a"
timestamp_file = "last_timestamp.txt"
## edited_timestamp_file = "edited_timestamp.txt"
base_URL = "https://api.notion.com/v1/databases/"
webhook = "https://discord.com/api/webhooks/1076413559459819540/jVeJE6XPJQaCVZAx35tEqD3BY1p5udBAwj8Ha4etsvfowXglVf2FMW-ztbPafIC94iB7"

headers = {
    "Notion-Version": "2021-05-13",
    "Authorization": "secret_CucoEvpLki8DGcdaJGNI692DPBt4Kv11uyodLN39VGe"
}

query = {
    "filter": {
        "property": "タグ1",
        "multi-select": {
            "equals": True
        }
    }
}

# Load the last timestamp from file
try:
    with open(timestamp_file, "r") as f:
        last_timestamp = f.read().strip()
        
except FileNotFoundError:
    # If the file does not exist, set the last timestamp to a very old date
    last_timestamp = "1970-01-01T00:00:00.000Z"


response = requests.post(base_URL + database_ID +"/query",headers=headers, data=query)
results = response.json().get("results")



if results:
    result = results[0]
    title = result["properties"]["名前"]["title"][0]["plain_text"]
    name = result["properties"]["タグ 1"]["multi_select"][0]["name"]
    date = result["properties"]["日付"]["date"]["start"]
    created_time = result["created_time"]
    edited_time = result["last_edited_time"]
    

    if created_time > last_timestamp:                 
        output_to_discord = f"{date}\n{name} {title}"
        discord = Discord(url=webhook)
        discord.post(content=output_to_discord)

        # Update the timestamp file with the new timestamp
        with open(timestamp_file, "w") as f:
            f.write(created_time)

    ##if edited_time > edited_timestamp_file:                 
       ## output_to_discord = f"{date}\n{name} {title}"
        ##discord = Discord(url=webhook)
       ## discord.post(content=f"{output_to_discord} (編集)")

    # Update the edited timestamp file with the new edited timestamp
       ## with open(edited_timestamp_file, "w") as l:
           ## l.write(edited_time)

