Easy Read data from com port and send them to the server Easier
============
Project Description Its hard to read data from the serial communication
and send the data over your server, especially with us students, hence
using a python script we can read the data written over the
communication port and manipulate them as we want Example: Read serial
data from proteus virtual terminal or your arduino project or raspberry
pi

Installation
============

``` {.bash}
pip install read_comports_tonet
```

Requirements || dependecies 
==========

Pyserial >=  2.20.0 \
requests >= 3.0 \
schedule >= 1.0.0 

Note
====

The comport should be there if it\'s for simulation one can use the
virtual ports emulators like Vspe

Usage
=====

Import the module and inside there is the class named ReadFromComPorts
then instatiate it like below passing two parameter comportname example
COM1 and baudarate e.g 9600

``` {.bash}
from read_comports_tonet import ReadFromComPorts
COM1 = ReadFromComPorts("<comport name e.g COM1>", baudrate)
```

## Testing if comport is open Use the COM object created  the method below

``` {.bash}
COM1.checkifTheComportisOpen()
```

Reading the line
================

The method here return data that have been decoded ready and in list if
you have sent them and separated them for obtain various data from the
same string \< parameters: optional but if you have written a string
like 33\**667*\*67 for separating your data then you can separate them
to obtain the data using this method

``` {.bash}
data = COM1.readLineOfData(splitter="<eg. ** its optional")
```

Reading the single character return the character
============

``` {.bash}
charObtained = COM1.readCharacterData()
```

Post data to the server Here the http post method is used hence one
============ 
have to provide the payload Parameter: Url \|\| payload should be a
dictionary

``` {.bash}
COM.postDataToServer("<url e.g thingspeak.com/post" , payload:dict)
```

## Perform the GET request The methods perform the get request and also
it can be used for pposting the data using the Route parameters
Parameters: url e.g Github routes RouteParameter: type dict e.g
{\'api\_key\' = \"shms24\" }

``` {.bash}
COM.getRequest("<url e.g thingspeak.com/post" , payload:dict)
```

## Schedule sending the data or fetching the data Scheduling the
sending of data to the server is easier since the package under the hood
uses the schedule module too, here both GET & POST methods can be
automated also setting the time your want to data to be sent Parameters:
time (type float)-\> Seconds that will be taken before calling the same
function for fetching the data or sending the data Method: here its http
method it can be POST or GET Payload (type-Dict-Optional): the data to
be sent if its posting

``` {.bash}
COM.scheduleSending("<url e.g thingspeak.com/post", time, "method e.g Post"  payload:dict(optional))
```

## Scheduling sending of the data without passing payload, package will
fetch the data from com port provided example Proteus The package was
inspired by this feature since students struggle taking of the data from
the various softwares they are using to the server that they can be
saved to the database, the package will fetch data under the hood and be
posting them basing on the time you have scheduled Parameters: method:
POST \|\| GET \*keys: (\"e.g temp\" , \"hum\") // Should be tuple

``` {.bash}
COM.scheduleSendingDataFromPorts("<url e.g thingspeak.com/post", time, "method e.g Post", "splitterstring e.g xx to separate data", *keys)
```

## Powered By: Yosia Lukumai

Github Account: <https://github.com/yosiaLukumai>
