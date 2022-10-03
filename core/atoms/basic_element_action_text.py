from __future__ import print_function
from builtins import str
import datetime
import sys
import time


from random import randint
from hamcrest import assert_that, contains_string, is_
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException, \
    InvalidElementStateException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from core import execution_logger, elements_loader
from core.atoms import basic_element_actions
from core.atoms.basic_element_actions import get_element_containing_visible_text_via_xpath, click_all_elements_by_xpath
from enums.bdd_variables_enum import BddVariablesEnum


def __assert_element_containing_following_text(context, random_element, text):
    if random_element is None:
        angular_element_actions.wait_for_angular(context)
        text_element = get_element_containing_visible_text_via_xpath(context, text)
        assert_that(text_element.text, contains_string(str(text)))
    else:
        assert_that(get_element_containing_visible_text_via_xpath(context, text).text, contains_string(str(random_element)))


def element_containing_following_text(context, text):
    if BddVariablesEnum.SAVED_RANDOM_NUMBER in text:
        text = context.config.userdata[BddVariablesEnum.SAVED_RANDOM_NUMBER]

    random_element = None
    try:
        random_element = context.config.userdata['calendar_event_name']
        execution_logger.info(context.log, 'Context.config.userdata[\'calendar_event_name\'] value: ' + random_element)
    except KeyError:
        execution_logger.info(context.log, 'Context.config.userdata[\'calendar_event_name\'] is NOT found')
    __assert_element_containing_following_text(context, random_element, text)


def get_element_containing_text(context, text):
    execution_logger.log_current_def_name(sys._getframe().f_code.co_name, context.log)
    return get_element_containing_visible_text_via_xpath(context, text)


def get_element_text_against_section(context, element_name, section_name):
    execution_logger.log_current_def_name(sys._getframe().f_code.co_name, context.log)
    return get_element_by_visible_text_via_xpath(context, section_name).find_element(
        elements_loader.get_by(context.vault_elements[element_name]['locator']),
        context.vault_elements[element_name]['selector']).text


def click_all_elements_by_visible_text(context, visible_text, element_type='*', wait=BddVariablesEnum.LONG_ELEMENT_WAIT):
    click_all_elements_by_xpath(context, f'//{element_type}[text()="{visible_text}"]')


def wait_all_elements_by_visible_text(context, visible_text, element_type='*', wait=BddVariablesEnum.LONG_ELEMENT_WAIT):
    xpath = f'//{element_type}[text()="{visible_text}"]'
    execution_logger.info(context.log, 'Trying to locate ALL elements via: ' + xpath)
    for element in context.session.driver.find_elements_by_xpath(xpath):
        try:
            basic_element_actions.wait_element_to_stop_moving(element)
            context.web_driver_wait(context.session.driver, BddVariablesEnum.MEDIUM_ELEMENT_WAIT).until(
                context.expected_conditions.presence_of_element_located((By.XPATH, xpath)))
        except:  # noqa: E722
            execution_logger.info(context.log, 'Element is not available!')


def click_all_elements_containing_visible_text(context, visible_text, element_type='*', wait=BddVariablesEnum.LONG_ELEMENT_WAIT):
    click_all_elements_by_xpath(context, '//{0}[contains(text(), "{1}")]'.format(element_type, visible_text))


def click_element_by_visible_text_if_present(context, visible_text, wait=BddVariablesEnum.EXTRA_SHORT_ELEMENT_WAIT):
    try:
        get_element_by_visible_text_via_xpath(context, visible_text, wait).is_displayed()
        get_element_by_visible_text_via_xpath(context, visible_text, wait).is_enabled()
        get_element_by_visible_text_via_xpath(context, visible_text, wait).click()
        execution_logger.info(context.log, f'Click successful on element with text: {visible_text}')
        return True
    except:  # noqa: E722
        print(f'{visible_text} - element not found for the time specified!')
        return False


def click_element_containing_visible_text_if_present(context, visible_text, wait=BddVariablesEnum.EXTRA_SHORT_ELEMENT_WAIT):
    try:
        get_element_containing_visible_text_via_xpath(context, visible_text, wait).is_displayed()
        get_element_containing_visible_text_via_xpath(context, visible_text, wait).is_enabled()
        get_element_containing_visible_text_via_xpath(context, visible_text, wait).click()
        execution_logger.info(context.log, f'Click successful on element containing text: {visible_text}')
    except:  # noqa: E722
        print(f'{visible_text} - element not found for the time specified!')

def click_element_containing_text_against_section_via_xpath(context, element_name, section_name):
    execution_logger.log_current_def_name(sys._getframe().f_code.co_name, context.log)
    context.session.driver.find_element(
        elements_loader.get_by(context.vault_elements[element_name]['locator']),
        '//*[contains(text(), \"' + section_name + '\")]/../..' + context.vault_elements[element_name]['selector'])\
        .click()


def select_option_by_visible_text(context, select_element, option_text):
    execution_logger.info(context.log,
                          'Trying to select option by text {0}  at {1}: '.format(option_text, select_element))
    select = Select(elements_loader.get_ui_element_by_key(context, select_element))
    select.select_by_visible_text(option_text)
    execution_logger.info(context.log, 'Select successful!')

def get_element_by_visible_text_via_xpath(context, element_visible_text, ui_element=None, wait=BddVariablesEnum.SHORT_ELEMENT_WAIT, element_type='*'):
    element_selector = f'//{element_type}[normalize-space(.) = "{element_visible_text}"]'
    # allows recursive chaining of find element
    if ui_element is not None:
        # wait parameter not passed in here because it blows up the stack
        get_element_by_visible_text_via_xpath(context, element_visible_text).is_displayed()
        get_element_by_visible_text_via_xpath(context, element_visible_text).is_enabled()
        return get_element_by_visible_text_via_xpath(context, element_visible_text)

    context.web_driver_wait(context.session.driver, wait).until(
        context.expected_conditions.visibility_of_all_elements_located((By.XPATH, element_selector)))
    all_found = context.web_driver_wait(context.session.driver, wait).until(
        context.expected_conditions.presence_of_all_elements_located((By.XPATH, element_selector)))
    return fixed_empty_html_with_text(all_found, element_visible_text)


def clear_text(context, element_name, wait=BddVariablesEnum.LONG_ELEMENT_WAIT):
    angular_element_actions.wait_for_angular(context, wait)
    execution_logger.info(context.log, 'Trying to clear text at element: ' + element_name)

    element = elements_loader.get_ui_element_by_key(context, element_name)
    by = elements_loader.get_by(context.vault_elements[element_name]['locator'])
    WebDriverWait(context.session.driver, BddVariablesEnum.MEDIUM_ELEMENT_WAIT).until(
        ec.visibility_of_element_located((by, context.vault_elements[element_name]['selector'])))

    element.clear()

    execution_logger.info(context.log, 'Text cleared successfully!')


def clear_and_enter_text(context, element_name, text, wait=BddVariablesEnum.LONG_ELEMENT_WAIT):
    element = elements_loader.get_ui_element_by_key(context, element_name)
    element.clear()

    enter_text(context, element_name, text)
    execution_logger.info(context.log, 'Text sent successfully!')
