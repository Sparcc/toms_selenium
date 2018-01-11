from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys, getopt
import os
import time
import getpass
import configparser
import re
import logging

def str2bool(v):
    returnValue = False
    if v.lower() in ("yes", "true", "t"):
        returnValue = True
    elif v.lower() in ("no", "false", "f"):
        returnValue = False
    return returnValue

def comp2HumanInt(x, h=True):
    x3=0
    if x <=0:
        x3=0
    else:
        if h:
            x3 = x - 1
            if x3 < 0:
                x3 = x
        else:
            x3=0
            x3 = x + 1
            if x3 < 0:
                x3 = x
    return x3
  
def RepresentsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

class Environment:
    #fetch initial data to start script from config.ini
    driverPaths = {'Chrome': 'C:\Selenium\chromedriver.exe',
                'Edge': 'C:\Selenium\MicrosoftWebDriver.exe',
                'IE': 'C:\Selenium\IEDriverServer.exe'
                };
                
    #people = []
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        
        self.buildEnvironmentAttributes()
        
    def buildEnvironmentAttributes(self):
        logging.warning('There are no extra attributes being built for Environment class')

class DriverManagement:
    #run drivers
    #impersonate users
    #go to requested items
    driver = 0
    driverRun = False
    env = 0
    comq = []
    
    def __init__(self, env, run = False):
        if run:
            self.env = env
            self.runDriver(env)
            self.driverRun = True
        
    def runDriver(self, env, browserType = None):
        if browserType is None:
            self.driver = webdriver.Chrome(env.driverPaths['Chrome'])
        else:
            self.driver = webdriver.Chrome(env.driverPaths[browserType])
        
    def quitDriver(self):
        self.driver.quit()
        
    def goURL(self, url, sleep = 0, wait = 0):
        self.driver.get(url)
        self.applyDelays(sleep, wait)
        
    def clickXpath(self, xpath, sleep = 0, wait = 0):
        self.applyDelays(sleep, wait)
        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
            element.click()
        except:
            loging.error('Could not find element at xpath "' + xpath +'"')
        
    def inputXpath(self, xpath, data, sleep = 0, wait = 0):
        self.applyDelays(sleep, wait)
        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
            element.clear()
            element.send_keys(data)
        except:
            loging.error('Could not find element at xpath "' + xpath +'"')
    
    def enterKeyXpath(self, xpath, sleep = 0, wait = 0):
        self.applyDelays(sleep, wait)
        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
            element.send_keys(Keys.RETURN)
        except:
            loging.error('Could not find element at xpath "' + xpath +'"')
    
    def applyDelays(self, sleep = 0, wait = 0):
        if sleep > 0:
            time.sleep(sleep)
        if wait > 0:
            self.driver.implicitly_wait(wait)
            
    def assertis(self, xpath, data):
        assert data == driver.find_element_by_xpath(xpath).text
        
    def assertin(self, xpath, data):
        assert data in driver.find_element_by_xpath(xpath).text

class CommandActionSystem:
    #process commands
    actionsAvailable = []
    actions = {}
    driverManager = 0
    defaultArgs = {}
    prefabArgs = {}
    prefabActions = {}
    initPrefabAction = 'LoginUTAS'
    config = 0
    def __init__(self, driverManager, debug = False, runPrefabs = True):
        self.debug = debug
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        self.driverManager = driverManager
        
        if not debug:
            self.actionsAvailable = self.config['actions']['actions'].strip().replace(" ","").split(",")
            self.buildActions()
            self.buildPrefabArgs()
            self.buildPrefabActions()

            if self.driverManager.driverRun:
                command = self.prefabActions[self.initPrefabAction].split(" ")
                action = command[0]
                argsKey = command[1]
                self.executeAction(action,*self.prefabArgs[argsKey])
        
    def buildPrefabArgs(self):
        logging.warning('There are no extra args being built for CommandActionSystem class')
    
    def buildPrefabActions(self):
        logging.warning('There are no extra actions being built for CommandActionSystem class')
        
    def buildActions(self):
        #each action
        for action in self.actionsAvailable:
            numSteps = int(self.config[action]['numSteps'])
            steps = []
            #each step
            for i in range(0,numSteps):
                #each comma-space delimited string or subStep is split into a list
                key = 's'+str(i)
                subSteps = self.config[action][key].strip().replace(" ","").split(",")
                subSteps = self.convertList(subSteps)
                steps.append(subSteps)
            #place list of step
            self.actions[action] = steps
    
    #TODO: Enhance performance - integrate into buildActions
    def convertList(self,data):
        returnData = []
        for x in data:
            match = re.search('\'.+\'',x)
            #is xpath
            if match:
                x = x[1:-1]
            #is boolean
            elif x.lower() in ("yes", "no", "true", "false","t", "f"):
                x = str2bool(x)
            #is int
            elif x != 'url' and x != 'delay' and x != 'enter' and x != 'assertis' and x != 'assertin':
                if isinstance(int(x), int):
                    x = int(x)
            returnData.append(x)
        return returnData
        
    #command format: <action/quit> *<actionName/Data>...*<actionName/Data> <---up to inf
    def acceptInput(self):
        acceptInput = True
        
        while acceptInput:
            print('Please input command')
            command = input()
            command = command.split(" ")
            acceptInput = self.parseCommand(command)
            
    #command is a list of actions and args afterwards
    def parseCommand(self, command):
        acceptInput = True
        action = ''
        if command[0].lower() == 'action':
            if len(command)>1:
                action = command[1]
                args = command[2:]
                self.executeAction(action, *args)
        if command[0].lower() == 'reload':
            self.actionsAvailable = self.config['actions']['actions'].strip().replace(" ","").split(",")
            self.buildActions()
            self.buildPrefabArgs()
            self.buildPrefabActions()
        if command[0] in self.prefabActions.keys():
                command = self.prefabActions[command[0]].split(" ")
                action = command[0]
                argsKey = command[1]
                self.executeAction(action,*self.prefabArgs[argsKey])
        if command[0].lower() == 'quit':
            self.driverManager.quitDriver()
            acceptInput = False
            return acceptInput
            
    def executeAction(self, action, *args):
        i = 0
        for step in self.actions[action]:
            print('-----------steps--\n%s------'%str(step))
            if step[0] == 'url': #url navigation step
                self.driverManager.goURL(step[1],step[2],step[3])
            elif step[0] == False: #click step
                self.driverManager.clickXpath(step[1],step[2],step[3])
            elif step[0] == 'enter':
                self.driverManager.enterKeyXpath(step[1],step[2],step[3])
            elif step[0] == 'delay':
                self.driverManager.applyDelays(1,0)
            elif step[0] == 'assertin':
                self.driverManager.assertin(stept[1],args[i])
                i+=1
            elif step[0] == 'assertis':
                self.driverManager.assertis(stept[1],args[i])
                i+=1
            else:#param: xpath, data, sleep = 0, wait = 0
                self.driverManager.inputXpath(step[1], args[i].replace("'","").replace("-"," "), step[2],step[3])
                i+=1