import time
import os 
from playwright.sync_api import sync_playwright

PLAY = sync_playwright().start()
BROWSER = PLAY.firefox.launch_persistent_context(
    user_data_dir="/tmp/playwright",
    headless=True,
)


PAGE = BROWSER.new_page()

def get_input_box():
    """Get the child textarea of `PromptTextarea__TextareaWrapper`"""
    print(PAGE)
    return PAGE.query_selector("textarea")

def is_logged_in():
    try:
        # See if we have a textarea with data-id="root"
        return get_input_box() is not None
    except AttributeError:
        return False

def send_message(message):
    # Send the message
    box = get_input_box()
    box.click()
    box.fill(message)
    box.press("Enter")
    while PAGE.query_selector(".result-streaming") is not None:
        time.sleep(0.1)

def get_last_message():
    """Get the latest message"""
    #page_elements = PAGE.query_selector_all("div[class*='ConversationItem__Message']")
    page_elements = PAGE.query_selector_all("div[class*='request-:']")

    last_element = page_elements[-1]
    return last_element.inner_text()

def chat(message):
    print("Sending message: ", message)
    send_message(message)
    response = get_last_message()
    print("Response: ", response)
    return response

def start_browser():
    PAGE.goto("https://chat.openai.com/")
    if not is_logged_in():
        print("Please log in to OpenAI Chat")
        print("Press enter when you're done")
        input()
    else:
        print("Logged in")
        
if __name__ == "__main__":
    start_browser()
    