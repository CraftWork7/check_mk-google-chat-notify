#!/usr/bin/env python3
# Google Chat Webhook Notification

import os
import sys
import requests
import json


# Get Tines WebHookURL from the environment variables and validate it
def GetPluginParams():
  env_vars = os.environ

  WebHookURL = str(env_vars.get("NOTIFY_PARAMETER_1"))

  # "None", if not in the environment variables
  if (WebHookURL == "None"):
          print("GChat-plugin: Mandatory first parameter is missing: Webhook URL")
          return 2, ""    # do not return anything, create final error

  return 0, WebHookURL


# Get the content of the message from the environment variables
def GetNotificationDetails():
  env_vars = os.environ
  HOSTNAME = env_vars.get("NOTIFY_HOSTNAME")
  HOSTALIAS = env_vars.get("NOTIFY_HOSTALIAS")
  ADDRESS = env_vars.get("NOTIFY_HOSTADDRESS")
  SERVICE = env_vars.get("NOTIFY_SERVICEDESC")
  OUTPUT_HOST = env_vars.get("NOTIFY_HOSTOUTPUT")
  OUTPUT_SERVICE = env_vars.get("NOTIFY_SERVICEOUTPUT")
  LONG_OUTPUT_HOST = env_vars.get("NOTIFY_LONGHOSTOUTPUT")
  LONG_OUTPUT_SERVICE = env_vars.get("NOTIFY_LONGSERVICEOUTPUT")
#  PERF_DATA = env_vars.get("NOTIFY_SERVICEPERFDATA")

  NOTIFY_SERVICESTATE = env_vars.get("NOTIFY_SERVICESTATE")
  NOTIFY_LASTSERVICESTATE = env_vars.get("NOTIFY_LASTSERVICESTATE")

  NOTIFY_HOSTSTATE = env_vars.get("NOTIFY_HOSTSTATE")
  NOTIFY_LASTHOSTSHORTSTATE = env_vars.get("NOTIFY_LASTHOSTSHORTSTATE")


  EVENT_HOST = f"{NOTIFY_HOSTSTATE} -> {NOTIFY_LASTHOSTSHORTSTATE}"
  EVENT_SERVICE = f"{NOTIFY_LASTSERVICESTATE} -> {NOTIFY_SERVICESTATE}"


  host_notify = {
    "Summary": f"CheckMK {HOSTNAME} - {EVENT_HOST}",
    "Host": HOSTNAME,
    "Alias": HOSTALIAS,
    "Address": ADDRESS,
    "Event": EVENT_HOST,
    "Output": OUTPUT_HOST,
    "LongOutput": LONG_OUTPUT_HOST
  }

  service_notify = {
    "Summary": f"CheckMK {HOSTNAME}/{SERVICE} {EVENT_SERVICE}",
    "Host": HOSTNAME,
    "Alias": HOSTALIAS,
    "Address": ADDRESS,
    "Service": SERVICE,
    "Event": EVENT_SERVICE,
    "Output": OUTPUT_SERVICE,
    "LongOutput": LONG_OUTPUT_SERVICE,
#    "PerfData": PERF_DATA
  }

  what = env_vars.get("NOTIFY_WHAT")
  # Handy hosts or service differently
  if what == "SERVICE":
          notify = service_notify
  else:
          notify = host_notify


  return notify


# Send the message to Google Chat
def SendToGchat(WebHookURL, data):
  return_code = 0

  msg = []
  for key,value in data.items():
      msg.append(f"*{key}*:\t {value}")

  # Set header information
  headers = { 'Content-Type': 'application/json' }

  try:
  # Make the POST request
    response = requests.post(WebHookURL, headers=headers, json={"text" : "\n".join(msg)})

  # Check the response status code
    if response.status_code == 200:
      print(f"Google Chat Webhook posted successfully.")
    else:
      print(f"Google Chat Webhook failed to post. Status code: {response.status_code}")
      print(response.text)
      return_code = 2
  except Exception as e:
    print(f"Google Chat Webhook: An error occurred: {e}")
    return_code = 2

  return return_code



def main():
        
  return_code, WebHookURL = GetPluginParams()
  if return_code != 0:
    return return_code   # Abort, if parameter for the webhook is missing

  data = GetNotificationDetails()
  return SendToGchat(WebHookURL, data)

if __name__ == '__main__':
        sys.exit(main())
