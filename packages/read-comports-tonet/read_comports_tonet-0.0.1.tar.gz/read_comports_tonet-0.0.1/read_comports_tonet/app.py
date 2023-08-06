#importing the modules
# Pyserial 
# Author: Yosia Lukumai


import serial
import time
import requests
import schedule

class ReadFromComPorts:
    comPort = ""
    data = []

    def __init__(self, comportname: str , baudrate: int , timeout=None):
        """
        Initialize the com port and baudrate then we create the virual port that can be shared
        """
        self.comportname = comportname
        self.baudrate = baudrate
        self.timeout = timeout
    
    @property
    def comPort(self):
        """
        This decorator will setup the comport 
        return : serial object with the port details
        """
        try:
            if(self.timeout == None):
                comPort = serial.Serial(self.comportname, self.baudrate)
                return comPort
            else:
                comPort = serial.Serial(self.comportname, self.baudrate, self.timeout)
                return comPort
        except serial.serialutil.SerialException as err:
            print("---> The port can't be found configure it make sure is  seen by your computer {}".format(self.comportname))
    
    @comPort.setter
    def comPort(self, comportname: str , baudrate:int , timeout: None):
        """
        Set up the comport if there are the changes

        return: serial object with the port info
        """
        comPort = serial.Serial(comportname, baudrate, timeout)
        return comPort
    
    def openPorts(self):
        """
        This will open the ports
        return: None
        """
        try:
            if(self.comPort.is_open):
                print("---> Port already opened")
            else:
                self.comPort.open()
        except (AttributeError, Exception ) as e:
            print("---> Configure well your ports {}".format(self.comportname))
            print(e)

    def checkifTheComportisOpen(self):
        try:
            if(self.comPort.is_open):
                print(self.comPort.is_open)
                print(">>>>> Port is open ready for use")
            else:
                print(">>>> Port is not open")
        except Exception as e:
            print("---> Configure your port {} well ".format(self.comportname))
            print("---> The port isn't open.... || Error:  {}".format(e))

    
    def closePort(self):
        """
        This will be used for closing the port
        return: 
        """
        try:
            if(self.comPort.is_open == False):
                print("---> Port is not opened")
            else:
                print("here is {}".format(self.comPort.is_open))
                return self.comPort.close()
        except Exception as e:
            print(">>> something has went wrong restart the script")
            print(e)
        
    
    def readCharacterData(self):
        """
        This  will return the character from the communication port that has been obtained after reading
        return: 
        Sequence: characters that has been obtained from the comp port
        """
        try:
            if(self.comPort.is_open):
                data = self.comPort.read().decode("utf-8")
                return data
        except Exception as e:
            print("---> something has went wrong while trying to read the line from the communication port")
            print(e)
    
    def readLineOfData(self, splitparameter=' '):
        """
        This methods return the characters received 
        return:
        list - That various data can be separated
        """
        try:
            if self.comPort.is_open:
                print("Reading the line from the comport")
                data = self.comPort.readline()
                dataDecoded = str(data[0: len(data)].decode('utf-8'))
                sortedData = dataDecoded.split(splitparameter)
                sortedData.pop()
                return sortedData
        except Exception as e:
            print("---> something has went wrong while trying to read the line from the communication port")
            print(e)

    
    def postDataToServer(self, url: str, payload: None):
        """
        The methods will be performing the work of sending data to the server according to the paload provided
        when one wants to make it continualy he/she can use the method schedule sending or use a loop after 
        building the payload to be sent

        Return: Response object when the data has been sent successful
        """
        try:
            requestSent = requests.post(url, json=payload)
            print(requestSent.text)
            print("")
            print("----> Data sent successful")
            print("")
            return requestSent.text
            
        except Exception as e:
            print(" --> Warning: Data wasn't sent")
            print(" >> Something has went wrong try to read the docs of the error raised from request lib")
            print(e)

    def getRequest(self,url: str, paramsReceived=None):
        """
        This methods helps one to send a get request
        Perform Get request and attach the route parameters this method will be useful like sending data to things speak sever 
        since they use the route parameters
        Return: requsets.text as the response
        """
        try:
            if( paramsReceived == None):
                requestSent = requests.get(url)
                print(requestSent.text)
                print("")
                print("----> Data sent successful")
                print("")
                return requestSent.text
            elif paramsReceived is not None and type(paramsReceived) is dict:
                requestSent = requests.get(url, params= paramsReceived)
                print(requestSent.text)
                print("")
                print("----> Data sent successful")
                print("")
                return requestSent.text
        except Exception as e:
            print(" --> Warning: Data wasn't sent")
            print(" >> Something has went wrong try to read the docs of the error raised from request lib")
            print(e)

    
    
    def scheduleSending(self, url:str, time:float, method: str, payload: None):
        """
        This method is helpful for sending data continously one can simulate real time sending of data using this method
        Return : None but prints the logs of the request.text response
        """
        try:
            if method.lower() == 'post':
                schedule.every(time).seconds.do(lambda: self.postDataToServer(url, payload))
            elif method.lower() == "get":
                schedule.every(time).seconds.do(lambda : self.getRequest(url,payload))
            else:
                print(">> Warning: Unsupported method ({}) ".format(method))
                print("we have not supported the other request format uses the request lib directly on the data you have received from ports")
                return -1
            
            while True:
                schedule.run_pending()
        except Exception as e:
            print(" --> Warning: Data wasn't sent")
            print(" >> Something has went wrong try to read the docs of the error raised from request lib || schedule lib || pyserial")
            print(e)
    

    def getMedataInDictionary(self,  splitparameter, url, method, *seq):
        try:
            data = self.readLineOfData(splitparameter)
            print(seq[0])
            payload = dict(zip(seq[0], data))
            print("Payload: {}".format(payload))
            if method.lower() == "post":
                self.postDataToServer(url, payload)
            elif method.lower() == 'get':
                self.getRequest(url, payload)
            else:
                print("--> Sorry the package was built with post and get for sending data to the server")
                print("--> Use the right http request method or obtain data and post via request lib or other lib")
        except Exception as e:
            print(" Error: Observe the sequence parameter of keys you passed to the function")
            print(e)
        
    
        

    def scheduleSendingDataFromPorts(self, url:str,  time:float, method:str, splitparameter: str, *keys):
        """
        The methods read data from ports and  assigning to dict then send data over the server according to the schedule
        Return: None  but prints log of success sending
        """

        # extracting the dictionary
        print(keys[0])
        schedule.every(time).seconds.do(lambda: self.getMedataInDictionary(splitparameter, url, method, keys[0]) )
        while True:
            schedule.run_pending()


#Instatiate the object then one can sart using the packckage smoothly

# com1 = ReadFromComPorts("com1", 9600)
# com1.checkifTheComportisOpen()
# Testing the post method
# com1.postDataToServer('https://eozpeglcqyig8l.m.pipedream.net', {'name': "yoa", 'age': 34})


# Testing the get method
# response = com1.getRequest('https://api.github.com/events')
# print(response)



# Perform Get request and attach the route parameters this method will be useful like sending data to things speak sever 
#since they use the route parameters
# Example
# response = com1.getRequest('https://eopzpeglcqyig8l.m.pipedream.net', {"api_key": 345245, 'name': "migos"})
# print(response)

# data = com1.readLineData("xx")
# print(data)


# com1.scheduleSending("https://eopzpeglcqyig8l.m.pipedream.net", 2, 'POST',{"name": "op"})

# com1.scheduleSendingDataFromPorts("https://opzpeglcqyig8l.m.pipedram.net", 1,'GET', "xx", ('speed', 'long', 'lat'))








