#!/usr/bin/env python3
import requests
import os
import time


def fetch_availability(product_number, store_id):
    payload = {
        "store": store_id,
        "little": False,
        "mt": "regular",
        "parts.0": product_number,
        "fts": True,
    }

    url = "https://www.apple.com/de/shop/fulfillment-messages"
    r = requests.get(url, params=payload)
    data = r.json()

    stores = data["body"]["content"]["pickupMessage"]["stores"]
    store = next(store for store in stores if store["storeNumber"] == store_id)
    avail = store["partsAvailability"][product_number]

    return {
        "store_name": store.get("storeName"),
        "available": avail.get("pickupDisplay") != "ineligible",
        "store_pickup_quote": avail.get("storePickupQuote"),
        "pickup_search_quote": avail.get("pickupSearchQuote"),
        "pickup_display": avail.get("pickupDisplay"),
    }


def assemble_availability_text(product_number, store_ids):
    avail_text = ""

    for store_id in store_ids:
        avail = fetch_availability(product_number, store_id)
        avail_text += f'{avail["store_name"]}: {avail["store_pickup_quote"]}\n'

    return avail_text


def create_file_if_not_exists(filepath):
    if not os.path.exists(filepath):
        with open(filepath, "w") as f:
            f.write("")


def do_it(part_no, store_ids, **kwargs):
    availability_text = assemble_availability_text(part_no, store_ids)

    create_file_if_not_exists("/tmp/cache.txt")

    with open("/tmp/cache.txt", "r+", encoding="utf-8") as f:
        if f.read() == availability_text:
            print("No Changes", flush=True)
        else:
            print("Changes detected", availability_text, flush=True)

            if kwargs["pushover_enabled"] == "1":
                requests.post(
                    "https://api.pushover.net/1/messages.json",
                    data={
                        "token": kwargs["pushover_token"],
                        "user": kwargs["pushover_user"],
                        "message": availability_text,
                        "title": "CHANGES DETECTED",
                    },
                    headers={"Content-Type": "application/x-www-form-urlencoded"},
                )

            f.write(availability_text)


if __name__ == "__main__":
    while True:
        do_it(
            os.environ["MONITORED_PART_NO"],
            os.environ["MONITORED_STORES"].split(","),
            pushover_enabled=os.environ["PUSHOVER_ENABLED"],
            pushover_token=os.environ["PUSHOVER_TOKEN"],
            pushover_user=os.environ["PUSHOVER_USER"],
        )
        time.sleep(int(os.environ["POLLING_DELAY_SECONDS"]))
