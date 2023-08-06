# LabAutomation Communication Request Manager

In the context of a physics lab automation project, this package aims to simplify communication with different devices. 
Communication is based on 0mq and json-based messages. This package is meant to be used in combination with a 0mq-based device server.

## Sending a request
The only relevant function to use is ReqParser.request():
Parameters:
  * device: to be addressed device name as string (defined in Device Server)
  * action: requested action as string ("connect", "disconnect", "test", arbitrary)
  * payload: values to be passed for arbitrary action 
        
Returns:
  * status: True (successful) or False (communication request failed)
  * info: string of more detailed information 

## Including / Replacing Communication Manager
By using the following import line, the package can be used:
from la_com_request_parser.com_request_parser import ReqParser

If you previously used the Communication Manager and it is deeply rooted in the project you can just import the 
following line to maintain full functionality:
from la_com_request_parser.com_request_parser import ReqParser as CommunicationManager

