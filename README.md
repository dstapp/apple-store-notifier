# Apple Store Notifier

Quick and dirty tool I used to get notified when the Apple Studio Display becomes available.
Queries Apple Store availability for given stores and notifies via Pushover when the product becomes available.

## Usage

Exchange `MONITORED_STORES` in the `docker-compose.yml` with a list of the Stores that you want to watch,
then adjust `PUSHOVER_TOKEN` and `PUSHOVER_USER` to get notified.

1 minute polling delay seems to be fine and I don't get blocked with three Apple Stores being queried.