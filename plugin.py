# Basic Python Plugin Example
#
# Author: GizMoCuz
#
"""
<plugin key="WeMoCrockpot" name="Belkin WeMo Crockpot" author="Christopher KOBAYASHI" version="1.0.0" wikilink="http://www.domoticz.com/wiki/plugins/plugin.html" externallink="https://www.google.com/">
    <description>
        <h2>Belkin WeMo Crockpot</h2><br/>
        Overview...
        <h3>Features</h3>
        <ul style="list-style-type:square">
            <li>Feature one...</li>
            <li>Feature two...</li>
        </ul>
        <h3>Devices</h3>
        <ul style="list-style-type:square">
            <li>Crockpot - cooks food slowly</li>
        </ul>
        <h3>Configuration</h3>
        Configuration options...
    </description>
    <params>
        <param field="Address" label="IP Address" width="200px" required="true"/>
        </param>
        <param field="Mode6" label="Debug" width="75px">
            <options>
                <option label="True" value="Debug"/>
                <option label="False" value="Normal"  default="true" />
            </options>
        </param>
    </params>
</plugin>
"""

import pywemo
import socket
import Domoticz
from enum import Enum

# >>> wemo_device.mode
# 50
# >>> wemo_device.set_state(51)
# >>> wemo_device.set_state(52)
MODE_NAMES = {
    CrockPotMode.Off: "Off",
    CrockPotMode.Warm: "Warm",
    CrockPotMode.Low: "Low",
    CrockPotMode.High: "High",
}

class BasePlugin:
    enabled = False
    def __init__(self):
        self.alive = False
        self.interval = 6  # 6*10 seconds
        self.heartbeatcounter = 0

    def onStart(self):
        Domoticz.Log("onStart called")
        try:
        	wemo_ip = socket.gethostbyname(Parameters["Address"])
        	wemo_port = pywemo.ouimeaux_device.probe_wemo(wemo_ip)
			wemo_url = 'http://%s:%i/setup.xml' % (wemo_ip, wemo_port)
			self.wemo_device = pywemo.discovery.device_from_description(wemo_url, None)
		except:
			Domoticz.log("not available or unrecognized")
			return

		self.alive = True
		if (len(Devices) == 0):
			SelectorOptions =	{	"LevelActions": "|||",
									"LevelNames": "Off|Warm|Low|High"
									"LevelOffHidden": "false",
									"SelectorStyle": "1"
								}
			Domoticz.Device(Name="Cooking Mode", Unit=0, TypeName="Selector Switch", Image=7, Options=SelectorOptions, Used=1).Create()

		current_mode = self.wemo_device.mode
		Devices[0].Update(nValue=current_mode, sValue=str(MODE_NAMES.get(current_mode)))


    def onStop(self):
        Domoticz.Log("onStop called")

    def onConnect(self, Connection, Status, Description):
        Domoticz.Log("onConnect called")

    def onMessage(self, Connection, Data):
        Domoticz.Log("onMessage called")

    def onCommand(self, Unit, Command, Level, Hue):
        if self.alive:
            Domoticz.Log("onCommand called for Unit " +
                     str(unit) + ": Parameter '" + str(command) + "', Level: " + str(level))

#            if command.lower() == 'on':
#                self.bulb.turn_on()
#                okay = self.bulb.is_on
#            elif command.lower() == 'off':
#                self.bulb.turn_off()
#                okay = self.bulb.is_off
#            elif command.lower() == 'set level':
#                if self.bulb.is_off:
#                    self.bulb.turn_on()
#                self.bulb.set_brightness(level)
#                okay = self.bulb.is_on
#            else:
#                okay = False
#
#            if okay is True:
#           Devices[unit].Update(nValue = self.bulb.is_on, sValue=str(level))
#           # Reset counter so we trigger emeter poll next heartbeat
#            self.heartbeatcounter = 0
        return

    def onNotification(self, Name, Subject, Text, Status, Priority, Sound, ImageFile):
        Domoticz.Log("Notification: " + Name + "," + Subject + "," + Text + "," + Status + "," + str(Priority) + "," + Sound + "," + ImageFile)

    def onDisconnect(self, Connection):
        Domoticz.Log("onDisconnect called")

    def onHeartbeat(self):
        Domoticz.Log("onHeartbeat called")

global _plugin
_plugin = BasePlugin()

def onStart():
    global _plugin
    _plugin.onStart()

def onStop():
    global _plugin
    _plugin.onStop()

def onConnect(Connection, Status, Description):
    global _plugin
    _plugin.onConnect(Connection, Status, Description)

def onMessage(Connection, Data):
    global _plugin
    _plugin.onMessage(Connection, Data)

def onCommand(Unit, Command, Level, Hue):
    global _plugin
    _plugin.onCommand(Unit, Command, Level, Hue)

def onNotification(Name, Subject, Text, Status, Priority, Sound, ImageFile):
    global _plugin
    _plugin.onNotification(Name, Subject, Text, Status, Priority, Sound, ImageFile)

def onDisconnect(Connection):
    global _plugin
    _plugin.onDisconnect(Connection)

def onHeartbeat():
    global _plugin
    _plugin.onHeartbeat()

    # Generic helper functions
def DumpConfigToLog():
    for x in Parameters:
        if Parameters[x] != "":
            Domoticz.Debug( "'" + x + "':'" + str(Parameters[x]) + "'")
    Domoticz.Debug("Device count: " + str(len(Devices)))
    for x in Devices:
        Domoticz.Debug("Device:           " + str(x) + " - " + str(Devices[x]))
        Domoticz.Debug("Device ID:       '" + str(Devices[x].ID) + "'")
        Domoticz.Debug("Device Name:     '" + Devices[x].Name + "'")
        Domoticz.Debug("Device nValue:    " + str(Devices[x].nValue))
        Domoticz.Debug("Device sValue:   '" + Devices[x].sValue + "'")
        Domoticz.Debug("Device LastLevel: " + str(Devices[x].LastLevel))
    return
