from __future__ import print_function
# Responsible for providing needed Wrappers by the DSL to interact with the Application drivers.
from builtins import str
import os
import time
import sys

from hamcrest import assert_that, has_length
from selenium.common.exceptions import WebDriverException, TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.webdriver import ActionChains
from selenium.webdriver.remote.webelement import WebElement
from core import elements_loader, execution_logger
from enums.bdd_variables_enum import BddVariablesEnum
from selenium.webdriver.common.keys import Keys


def wait_for_element(context, element_name, wait=BddVariablesEnum.LONG_ELEMENT_WAIT):
    execution_logger.info(context.log, 'Trying to locate and click on element: ' + element_name)

    try:
        element_locator = elements_loader.get_by(context.vault_elements[element_name]['locator'])
        element_selector = context.vault_elements[element_name]['selector']
        WebDriverWait(context.session.driver, wait).until(
            ec.visibility_of_element_located((element_locator, element_selector)))
    except KeyError:
        execution_logger.info(context.log, 'Selector for {0} was not found in vault!'.format(element_name))
    except TimeoutException:
        execution_logger.error(context.log, f"Element: {element_name} not found on page.")


def wait_and_click_element(context, element_name, wait=BddVariablesEnum.LONG_ELEMENT_WAIT):
    wait_for_element(context, element_name, wait)

    element = elements_loader.get_ui_element_by_key(context, element_name)
    wait_element_to_stop_moving(element)
    element.click()

    execution_logger.info(context.log, 'Click successful!')


def click_element_by_index(context, elements_name, index, wait=BddVariablesEnum.LONG_ELEMENT_WAIT):
    execution_logger.info(context.log, 'Trying to locate and click on element: ' + elements_name)

    elements = elements_loader.get_ui_element_by_key(context, elements_name)
    by = elements_loader.get_by(context.vault_elements[elements_name]['locator'])
    WebDriverWait(context.session.driver, wait).until(ec.element_to_be_clickable(
        (by, context.vault_elements[elements_name]['selector'])))
    elements[index].click()

    execution_logger.info(context.log, 'Click successful!')


def get_element(context, element_name, wait=BddVariablesEnum.LONG_ELEMENT_WAIT, should_return_collection=False):
    element = elements_loader.get_ui_element_by_key(context, element_name.lower(), should_return_collection)

    return element  # noqa: F405

def click_element_if_present(context, element_name, wait=BddVariablesEnum.LONG_ELEMENT_WAIT):
    if is_element_present(context, element_name, wait):
        click_element(context, element_name, wait)


def click_element(context, element_name, wait=BddVariablesEnum.LONG_ELEMENT_WAIT):
    execution_logger.info(context.log, 'Trying to locate and click on element: ' + element_name)
    action_chains = ActionChains(context.session.driver)
    action_chains.move_to_element(elements_loader.get_ui_element_by_key(context, element_name)).click()
    action_chains.perform()
    execution_logger.info(context.log, 'Click successful!')


def is_ui_element_present_by_key(context, element_name):
    execution_logger.info(context.log, 'Identify if element ' + element_name + ' is present')
    try:
        elements_loader.get_ui_element_by_key(context, element_name)
        return True
    except WebDriverException:
        return False


def get_element_list_containing_visible_text_via_xpath(context, element_visible_text, element_type='*', wait=BddVariablesEnum.SHORT_ELEMENT_WAIT, attribute='text()'):
    element_selector = f'//{element_type}[contains({attribute}, "{element_visible_text}")]'
    context.web_driver_wait(context.session.driver).until(
        context.expected_conditions.visibility_of(context.session.driver.find_element(By.XPATH, element_selector)))
    all_found = context.web_driver_wait(context.session.driver, wait).until(
        context.expected_conditions.presence_of_all_elements_located((By.XPATH, element_selector)))
    return all_found


def get_element_containing_visible_text_via_xpath(
        context, element_visible_text, element_type='*', wait=BddVariablesEnum.SHORT_ELEMENT_WAIT, attribute='text()'):
    all_found = get_element_list_containing_visible_text_via_xpath(
        context, element_visible_text, element_type, wait, attribute)
    return fixed_empty_html_containing_text(all_found, element_visible_text)


def execute_script_on_element_with_text(context, element_visible_text, element_type='*', attribute='text()', script='click()', wait=BddVariablesEnum.SHORT_ELEMENT_WAIT):
    try:
        angular_element_actions.wait_for_angular(context, wait)
        element_selector = f'//{element_type}[contains({attribute}, "{element_visible_text}")]'
        element = context.session.driver.find_element(By.XPATH, element_selector)
        context.session.driver.execute_script(f'arguments[0].{script};', element)
    except TimeoutException:
        execution_logger.error(context.log, f'Element {element_visible_text} not found on the page!')


def click_all_elements(context, element_name, wait=BddVariablesEnum.LONG_ELEMENT_WAIT):
    execution_logger.info(context.log, 'Trying to locate and click on ALL elements: ' + element_name)
    action_chains = ActionChains(context.session.driver)
    for element in elements_loader.get_ui_element_by_key(context, element_name, True):
        try:
            angular_element_actions.wait_for_angular(context, wait)
            action_chains.move_to_element(element).perform()
            action_chains.click(element).perform()
        except:  # noqa: E722 AWS Batch unable to import ElementClickInterceptedException
            execution_logger.info(context.log, 'Error trying to click on: ' + element_name)


def switch_to_window(context, window_element, wait=BddVariablesEnum.EXTRA_LONG_ELEMENT_WAIT):
    angular_element_actions.wait_for_angular(context, wait)
    context.session.driver.switch_to_frame(elements_loader.get_ui_element_by_key(context, window_element))


def send_key_to_element(context, key, element_name, wait=BddVariablesEnum.LONG_ELEMENT_WAIT):
    elements_loader.get_ui_element_by_key(context, element_name).send_keys(key)


def wait_element_to_stop_moving(find_element, *args):
    element = find_element
    if not isinstance(find_element, WebElement):
        element = find_element(*args)

    element_x = element.location['x']
    element_y = element.location['y']
    while (element.location['x'] > element_x) and (element.location['y'] > element_y):
        time.sleep(0.5)
        element_x = element.location['x']
        element_y = element.location['y']
        element = find_element(*args)


def click_all_elements_by_xpath(context, xpath, wait=BddVariablesEnum.LONG_ELEMENT_WAIT):
    execution_logger.info(context.log, 'Trying to locate and click on ALL elements via: ' + xpath)

    for element in context.session.driver.find_elements_by_xpath(xpath):
        try:
            wait_element_to_stop_moving(element)
            context.web_driver_wait(context.session.driver, wait).until(
                context.expected_conditions.presence_of_element_located((By.XPATH, xpath)))
            ActionChains(context.session.driver).move_to_element(element).perform()
            wait_element_to_stop_moving(element)
            ActionChains(context.session.driver).click(element).perform()
            if not element.is_selected():
                ActionChains(context.session.driver).click(element).perform()
        except:  # noqa: E722
            execution_logger.info(context.log, 'Element is not selected!')


def is_element_displayed_by_xpath(context, element, wait=BddVariablesEnum.LONG_ELEMENT_WAIT):
    is_widget_displayed = True
    try:
        get_element(context, element, wait).is_displayed()
    except WebDriverException:
        execution_logger.info(context.log, 'Widget {0} is not displayed on the board.'.format(element))
        is_widget_displayed = False
    return is_widget_displayed


def is_text_displayed_by_xpath(context, text):
    try:
        return len(get_element_list_containing_visible_text_via_xpath(context, text)) >= 1
    except NoSuchElementException:
        return 0


def safe_try(func, context, *args, **kwargs):
    execution_logger.info(context.log, 'Attempting to call function:' + func.__str__())
    execution_logger.info(context.log, 'params:' + args.__str__())
    new_args = (context,) + args
    try:
        return func(*new_args, **kwargs)
    except:  # noqa: E722
        execution_logger.info(context.log, 'Error during function execution')


def safe_try_do(action, element_func, *args, **kwargs):
    element = safe_try(element_func, *args, **kwargs)
    if element is not None:
        if action == 'click':
            element.click()
        else:
            raise NotImplementedError('No WebDriver method is mapped to: ' + action)
    else:
        print('Element not found!')

def close_modal(context):
    execution_logger.log_current_def_name(sys._getframe().f_code.co_name, context.log)
    context.session.driver.find_element_by_css_selector('body').send_keys(Keys.ESCAPE)
    context.session.driver.find_element_by_css_selector('body').send_keys(Keys.ESCAPE)
    context.session.driver.find_element_by_css_selector('body').send_keys(Keys.ESCAPE)
    angular_element_actions.wait_for_angular(context)

def select_option_by_value(context, select_element, option_value):
    execution_logger.info(context.log,
                          f'Trying to select option by text {option_value} at {select_element}')
    select = Select(elements_loader.get_ui_element_by_key(context, select_element))
    select.select_by_value(option_value)
    execution_logger.info(context.log, 'Select successful!')


def is_element_present(context, element_name, wait=BddVariablesEnum.EXTRA_SHORT_ELEMENT_WAIT):
    angular_element_actions.wait_for_angular(context, wait)
    try:
        elements_loader.get_ui_element_by_key(context, element_name, wait=wait).is_enabled()
        execution_logger.info(context.log, f'Found element: {element_name}')
        return True
    except Exception as e:  # noqa: E722
        execution_logger.info(context, f'Element not found{element_name}: {e}')
        return False
