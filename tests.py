import unittest
import logging
from driver import *

class MockCommandActionSystem(CommandActionSystem):
    #process commands
    actionsAvailable = []
    actions = {}
    driverManager = 0
    def __init__(self, driverManager, debug = False):
        self.debug = debug
        config = configparser.ConfigParser()
        config.read('config.ini')
        
        self.actionsAvailable = config['DEFAULT']['Actions'].strip().replace(" ","").split(",")
        if driverManager.driverRun:
            self.loginSNOW()
        
        buildActions(config)

class MockDriverManagement(DriverManagement):
    browserType = 'Chrome'
    def runDriver(self, env, browserType = 0):

        self.driver = 1
        self.driverName = 'Test Driver'
    def goURL(self, url, sleep = 0, wait = 0):
        self.driver.get(url)
        applyDelays(sleep, wait)
        
    def clickXpath(self, xpath, sleep = 0, wait = 0):
        applyDelays(sleep, wait)
        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
            element.click()
        except:
            print('Could not find element at xpath "' + xpath +'"')
        
    def inputXpath(self, data, xpath, sleep = 0, wait = 0):
        applyDelays(sleep, wait)
        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
            element.send_keys(data)
        except:
            print('Could not find element at xpath "' + xpath +'"')
            
    def applyDelays(self, sleep = 0, wait = 0):
        print('Sleep: %i Wait: %i'%sleep%wait)

class utas_login(unittest.TestCase):
    def setUp(self):
        self.env = Environment()
        self.driverManager = MockDriverManagement(self.env,True)
        
    def testComp2HumanInt(self):
        self.assertEqual(comp2HumanInt(4),3)
        self.assertEqual(comp2HumanInt(3,False),4)
        self.assertEqual(comp2HumanInt(0),0)
        self.assertEqual(comp2HumanInt(-1),0)
        
    def testDriverManagerExists(self):
        self.assertNotEqual(self.driverManager.driver, 0)
        self.assertTrue(self.driverManager.driverRun)
        self.assertEqual(self.driverManager.browserType,'Chrome')
        
    def testEnvironmentLoading(self):
        logging.warning('environment sub classes not tested')
        
    def testCommandSystemInitialisation(self):
        comSys = CommandActionSystem(self.driverManager, True)

    def testActionIdentification(self):
        #logging.warning('action identification not tested')
        comSys = CommandActionSystem(self.driverManager, False)
        self.assertEqual(comSys.actionsAvailable[0],'login')
        self.assertEqual(comSys.actionsAvailable[1],'impersonate')
        self.assertEqual(comSys.actionsAvailable[2],'lookAtRIT')
        
    def testActionBuilding(self):
        #logging.warning('action building not tested')
        comSys = CommandActionSystem(self.driverManager, False)
        self.assertEqual(comSys.actions['login'][0][0],'url')
        self.assertEqual(comSys.actions['impersonate'][0][0],False)
        self.assertEqual(comSys.actions['impersonate'][0][1],'//*[@id="user_info_dropdown"]')
        self.assertEqual(comSys.actions['impersonate'][0][2],0)
        self.assertEqual(comSys.actions['impersonate'][0][3],0)
        self.assertEqual(comSys.actions['impersonate'][1][0],False)
        self.assertEqual(comSys.actions['impersonate'][1][1],'/html/body/div/header/div[1]/div/div[2]/div/div[2]/div/ul/li[2]/a')
        self.assertEqual(comSys.actions['impersonate'][1][2],0)
        self.assertEqual(comSys.actions['impersonate'][1][3],0)
        self.assertEqual(comSys.actions['lookAtRIT'][0][0],False)
        self.assertEqual(comSys.actions['lookAtRIT'][0][1],'/html/body/div[1]/header/div[1]/div/div[2]/div/div[4]/form/div/label/span')
        self.assertEqual(comSys.actions['lookAtRIT'][0][2],0)
        self.assertEqual(comSys.actions['lookAtRIT'][0][3],0)
    
    #def testPrefabActionBuilding(self):
        #comSys = CommandActionSystem(self.driverManager)
        #self.assertEqual(comSys.actions['LoginUTAS']
    
    def testCommandExecution(self):
        logging.warning('command execution not tested')
        
    def tearDown(self):
        logging.warning('teardown not tested')
        
if __name__ == '__main__':
    unittest.main()