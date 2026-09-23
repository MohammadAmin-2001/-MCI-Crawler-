import os
import re
from playwright.sync_api import Playwright, sync_playwright, expect




def close_mci_popups(page):
    for _ in range(10):
        cancel_button = page.get_by_role("button", name="انصراف")

        if cancel_button.count() == 0:
            break

        if not cancel_button.first.is_visible():
            break

        cancel_button.first.click()
        page.wait_for_timeout(300)

def run(playwright: Playwright,MCI_PHONE, MCI_PASSWORD) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()


    response = page.goto(
    "https://my.mci.ir/auth",
    wait_until="domcontentloaded",
    timeout=60000
)

    print("HTTP:", response.status if response else None, flush=True)
    print("URL:", page.url, flush=True)
    

    page.get_by_text("ورود با رمز عبور").wait_for(state="visible")
    page.get_by_text("ورود با رمز عبور").click()

    phone_input = page.get_by_role("textbox", name="تلفن همراه")
    password_input = page.get_by_role("textbox", name="رمز عبور")

    phone_input.wait_for(state="visible")

    phone_input.fill(MCI_PHONE)
    password_input.fill(MCI_PASSWORD)

    page.get_by_role("button", name="ورود").click()

    close_mci_popups(page)
    packages_link = page.locator("a").filter(has_text="بسته‌ها")
    packages_link.wait_for(state="visible")
    packages_link.click()

    my_packages = page.get_by_role("link", name="بسته‌های من")
    my_packages.wait_for(state="visible")
    my_packages.click()


    close_mci_popups(page)
    total_package = page.locator("div.max-value").first
    current_package = page.locator("div.current-value").first
    remain_text = page.locator("div.remain-text").first

    total_package.wait_for(state="visible")
    current_package.wait_for(state="visible")
    remain_text.wait_for(state="visible")



    remaining_days = page.locator(
        "xpath=/html/body/app-root/app-main/div/div/div/div/div[2]/app-my-package/"
        "mat-card/mat-card-content/mat-tab-group/div/mat-tab-body[1]/div/div/"
        "app-package-card/div/div[3]/div[2]"
    ).first

    remaining_days.wait_for(state="visible")



    total = total_package.inner_text()
    current = current_package.inner_text()
    remaining_days_ = remaining_days.inner_text()


    context.close()
    browser.close()

    return total, current, remaining_days_

def my_mci_summary(MCI_PHONE,MCI_PASSWORD):

    data = {}

    with sync_playwright() as playwright:
        summary = run(playwright,MCI_PHONE,MCI_PASSWORD)
        total_text = summary[0]
        current_text = summary[1]
        days_text =  summary[2]
        total_gb = float(re.search(r"[\d.]+", total_text).group())
        current_gb = float(re.search(r"[\d.]+", current_text).group())
        remaining_days_value = int(re.search(r"\d+", days_text).group())
        used_gb = total_gb - current_gb
        remaining_percent = (current_gb / total_gb) * 100
        used_percent = (used_gb / total_gb) * 100
        data = {
        "total_gb": total_gb,
        "remaining_gb": current_gb,
        "used_gb": round(used_gb, 2),
        "remaining_days": remaining_days_value,
        "remaining_percent": round(remaining_percent, 2)
    }
    return data


