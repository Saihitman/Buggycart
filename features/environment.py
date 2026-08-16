from selenium import webdriver

def before_scenario(context, scenario):
    # Standard Selenium 4 auto-detects Chrome automatically!
    context.driver = webdriver.Chrome()
    context.driver.implicitly_wait(5)
    context.driver.maximize_window()

def after_scenario(context, scenario):
    if hasattr(context, "driver"):
        context.driver.quit()