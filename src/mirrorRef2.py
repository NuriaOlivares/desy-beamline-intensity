# -*- coding: utf-8 -*-
"""
Created on Fri Jul 26 08:44:36 2019
@author: olivaren
"""

import pandas as pd
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys

submission_dir = 'completed_assignments'


def thickmirror2(lambdamin, lambdamax, lambdanum, pol, density, material, roughness, angle):
    webthickmirror = 'http://henke.lbl.gov/optical_constants/mirror2.html'
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(webthickmirror)

    # Selecting Variable Options
    formulabox = driver.find_element_by_name('Formula')
    formulabox.clear()
    formulabox.send_keys(material)

    densitybox = driver.find_element_by_name('Density')
    densitybox.clear()
    densitybox.send_keys(density)

    roughnessbox = driver.find_element_by_name('Sigma')
    roughnessbox.clear()
    roughnessbox.send_keys(roughness)

    polbox = driver.find_element_by_name('Pol')
    polbox.clear()
    polbox.send_keys(pol)

    select = Select(driver.find_element_by_name('Scan'))
    select.select_by_value('Wave')

    lambdaminbox = driver.find_element_by_name('Min')
    lambdamaxbox = driver.find_element_by_name('Max')
    stepbox = driver.find_element_by_name('Npts')

    lambdaminbox.send_keys(Keys.BACKSPACE * 2)
    lambdaminbox.send_keys(lambdamin)

    lambdamaxbox.send_keys(Keys.BACKSPACE * 4)
    lambdamaxbox.send_keys(lambdamax)

    stepbox.send_keys(Keys.BACKSPACE * 3)
    stepbox.send_keys(lambdanum)

    anglebox = driver.find_element_by_name('Fixed')
    anglebox.clear()
    anglebox.send_keys(angle)

    enterbutton = driver.find_element_by_xpath("/html/body/form/input")
    enterbutton.click()

    # In case of pop ups: alert = driver.switch_to.alert()
    driver.switch_to.window(driver.window_handles[1])

    link = driver.find_element_by_link_text('data file here')
    link.click()

    url = driver.current_url
    test = pd.read_csv(url, skiprows=2, names=['Wl'])
    test.dropna(inplace=True)

    new = test["Wl"].str.split(" ", n=4, expand=True)
    new.drop(new.columns[[0, 1, 2]], axis=1, inplace=True)
    new.columns = ['Wavelength', 'Refl']
    new['Wavelength'] = pd.to_numeric(new['Wavelength'])
    new['Refl'] = pd.to_numeric(new['Refl'])

    Reflectivity = new.Refl.tolist()
    Wave = new.Wavelength.tolist()

    driver.close()

    return Reflectivity, Wave