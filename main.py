from crawler import my_mci_summary
from bale import  send_bale_message, get_ids
from os import getenv



def notify_mci(summary):
    message = f"""
📶 MCI Package Status

📦 Total: {summary['total_gb']} GB
🟢 Remaining: {summary['remaining_gb']} GB
🔴 Used: {summary['used_gb']} GB
📅 Remaining days: {summary['remaining_days']}
📊 Remaining: {summary['remaining_percent']}%
""".strip()
    return message

def is_critical(summary:str):
    if float(getenv("INTERNET_REMAINING_PERCENT","10.00")) >= summary['remaining_percent']:
        print("for emaining_percent")
        return True
    elif int(getenv("INTERNET_DAYS_TH","10")) > summary['remaining_days']:
        print("remaining_days")
        return True
    else:
        return False


def main():
    print("starting....")
    MCI_USERNAME = getenv("MCI_USERNAME")
    MCI_PASSWORD= getenv("MCI_PASSWORD")
    print("scraping...")
    summary = my_mci_summary(MCI_USERNAME,MCI_PASSWORD)
    if is_critical(summary):
        message = notify_mci(summary)
        get_chat_ids = get_ids()
        for chat_id in list(get_chat_ids):
            send_bale_message(message,chat_id)

if __name__=="__main__":
    main()