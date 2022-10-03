from __future__ import print_function
# Responsible for loading related locator and selector for each ui-element
# from the specified pool (test_data\ui_elements_vault.yaml)
import time

from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from enums.bdd_variables_enum import BddVariablesEnum
from core import execution_logger
from multi_key_dict import multi_key_dict


def get_locator_strategies(context):
    locators = {
        'xpath': context.session.driver.find_element_by_xpath,
        'css': context.session.driver.find_element_by_css_selector,
        'id': context.session.driver.find_element_by_id,
        'class': context.session.driver.find_element_by_class_name,
        'name': context.session.driver.find_element_by_name,
        'link_text': context.session.driver.find_element_by_link_text,
        'partial_link_text': context.session.driver.find_element_by_partial_link_text,
        'tag': context.session.driver.find_element_by_tag_name,
        'elements_xpath': context.session.driver.find_elements_by_xpath,
        'elements_class': context.session.driver.find_elements_by_class_name,
        'elements_css': context.session.driver.find_elements_by_css_selector,
        'elements_link_text': context.session.driver.find_elements_by_link_text,
        'elements_partial_link_text': context.session.driver.find_elements_by_partial_link_text,
        'elements_name': context.session.driver.find_elements_by_name,
        'elements_tag': context.session.driver.find_elements_by_tag_name,
        'elements_id': context.session.driver.find_elements_by_id
    }
    if 'mobile' in context.config.userdata['platform']:
        locators['id'] = context.session.driver.find_element_by_accessibility_id
    return locators


def get_ui_element_by_key(context, element_name, should_return_collection=False, wait= BddVariablesEnum.LONG_ELEMENT_WAIT):
    try:
        ui_element_locator = context.vault_elements[element_name]['locator']
        if should_return_collection:
            ui_element_locator = 'elements_' + ui_element_locator
        execution_logger.info(context.log, 'Element: { ' + element_name + ' }, will be located via: ' + ui_element_locator)
        ui_element_selector = context.vault_elements[element_name]['selector']
        execution_logger.info(context.log, 'Selector: { ' + ui_element_selector + ' } found for element: ' + element_name)
        execution_logger.info(context.log, 'Waiting for {0}'.format(element_name))
        context.web_driver_wait(context.session.driver, wait).until(
            context.expected_conditions.presence_of_element_located((get_by(ui_element_locator), ui_element_selector)))
        element = context.session.driver.find_element(get_by(ui_element_locator), ui_element_selector)

        if 'desktop' in context.config.userdata["platform"]:
            highlight(context.js, element)
        if should_return_collection:
            element = context.session.driver.find_elements(get_by(ui_element_locator), ui_element_selector)
        else:
            element = context.session.driver.find_element(get_by(ui_element_locator), ui_element_selector)
        return element

    except KeyError:
        execution_logger.info(context.log, f'Selector for {element_name} was not found in vault!')
        raise
    except TimeoutException:
        execution_logger.info(context.log, f'Element {element_name} not found on the page!')
        raise


def get_ui_element_by_key_and_wait_to_be_clickable(context, element_name, should_return_collection=False, wait=BddVariablesEnum.MEDIUM_ELEMENT_WAIT):
    element = get_locator_strategies(context)
    ui_element_locator = ''
    ui_element_selector = ''
    try:
        ui_element_locator = context.vault_elements[element_name]['locator']
        if should_return_collection:
            ui_element_locator = 'elements_' + ui_element_locator
        execution_logger.info(context.log, 'Element: { ' + element_name + ' }, will be located via: ' + ui_element_locator)
        ui_element_selector = context.vault_elements[element_name]['selector']
        execution_logger.info(context.log, 'Selector: { ' + ui_element_selector + ' } found for element: ' + element_name)
        execution_logger.info(context.log, 'Waiting for {0}'.format(element_name))
        context.web_driver_wait(context.session.driver, wait).until(
            context.expected_conditions.presence_of_element_located((get_by(ui_element_locator), ui_element_selector)))
        context.web_driver_wait(context.session.driver, wait).until(
            context.expected_conditions.element_to_be_clickable((get_by(ui_element_locator), ui_element_selector)))
    except KeyError:
        execution_logger.info(context.log, f'Selector for {element_name} was not found in vault!')
    except TimeoutException:
        execution_logger.info(context.log, f'Element {element_name} not found on the page!')
    elem = element[ui_element_locator](ui_element_selector)

    return elem


def get_by(ui_element_locator):
    by = multi_key_dict()

    by['xpath', 'elements_xpath'] = By.XPATH
    by['css', 'elements_css'] = By.CSS_SELECTOR
    by['id', 'elements_id'] = By.ID
    by['class', 'elements_class'] = By.CLASS_NAME
    by['name', 'elements_name'] = By.NAME
    by['link_text', 'elements_link_text'] = By.LINK_TEXT
    by['partial_link_text', 'elements_partial_link_text'] = By.PARTIAL_LINK_TEXT
    by['tag', 'elements_tag'] = By.TAG_NAME

    return by[ui_element_locator]


def get_element_locator(context, element_name):
    try:
        return context.vault_elements[element_name]['locator']
    except KeyError:
        execution_logger.info(context.log, 'Selector for {0} was not found in vault!'.format(element_name))


def get_element_selector(context, element_name):
    try:
        return context.vault_elements[element_name]['selector']
    except KeyError:
        execution_logger.info(context.log, 'Selector for {0} was not found in vault!'.format(element_name))
