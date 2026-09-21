# MCI Crawler

The crawler starts a container that:

- Logs in to the MCI website
- Uses Playwright with Chromium
- Extracts the current internet package information
- Checks the remaining package usage
- Sends a notification through the Bale bot when needed
- Exits after the job is finished