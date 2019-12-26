# Basic Python Plugin Example
#
# Author: GizMoCuz
#
"""
<plugin key="WeMoCrockpot" name="Belkin WeMo Crockpot" author="Christopher KOBAYASHI" version="1.0.0" wikilink="http://www.domoticz.com/wiki/plugins/plugin.html" externallink="https://www.google.com/">
    <description>
        <h2>Belkin WeMo Crockpot</h2>
        <h3>Devices</h3>
        <ul style="list-style-type:square">
            <li>Crockpot</li>
        </ul>
    </description>
    <params>
        <param field="Address" label="IP Address" width="200px" required="true"/>
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

class WeMoCrockpotPlugin:
    enabled = False
    alive = False

    state_dict = {
                    0: "0",
                    50: "10",
                    51: "20",
                    52: "30"
        }

    def __init__(self):
        self.interval = 6  # 6*10 seconds
        self.heartbeatcounter = 0

    def onStart(self):
        Domoticz.Log("onStart called")
        try:
            Domoticz.Log(Parameters["Address"])
       	    wemo_ip = socket.gethostbyname(Parameters["Address"])
       	    Domoticz.Log(str(wemo_ip))
            wemo_port = pywemo.ouimeaux_device.probe_wemo(wemo_ip)
            wemo_url = 'http://%s:%i/setup.xml' % (wemo_ip, wemo_port)
            self.wemo_device = pywemo.discovery.device_from_description(wemo_url, None)
        except:
            Domoticz.Log("not available or unrecognized")
            return

        self.alive = True
        current_state = self.wemo_device.get_state()

        SelectorOptions =   {   "LevelActions": "|||",
                                "LevelNames": "Off|Warm|Low|High",
                                "LevelOffHidden": "false",
                                "SelectorStyle": "0"
                            }
        if (len(Devices) == 0):
            Domoticz.Device(Name="Slow Cooker", Unit=1, TypeName="Selector Switch", Image=7, Options=SelectorOptions, Used=1).Create()
            Domoticz.Log("created")
            Devices[1].Update(nValue=2, sValue=self.state_dict[self.wemo_device.mode])
        else:
            Devices[1].Update(nValue=2, sValue=self.state_dict[self.wemo_device.mode],
                TypeName="Selector Switch", Options=SelectorOptions, Used=1)
            Domoticz.Log("updated")
        Domoticz.Log(str(self.wemo_device.mode))

    def onStop(self):
        Domoticz.Log("onStop called")

    def onConnect(self, Connection, Status, Description):
        Domoticz.Log("onConnect called")

    def onMessage(self, Connection, Data):
        Domoticz.Log("onMessage called")

    def onCommand(self, Unit, Command, Level, Hue):
        if self.alive:
            Domoticz.Log("onCommand called for Unit " +
                     str(Unit) + ": Parameter '" + str(Command) + "', Level: " + str(Level))

            if Command.lower() == 'off':
                Level = 0

            try:
                vstate = list(self.state_dict.keys())[list(self.state_dict.values()).index(str(Level))]
            except:
                return
            self.wemo_device.set_mode(vstate, 0)
            Devices[Unit].Update(nValue = 2, sValue=str(Level))
            self.heartbeatcounter = 0

    def onNotification(self, Name, Subject, Text, Status, Priority, Sound, ImageFile):
        Domoticz.Log("Notification: " + Name + "," + Subject + "," + Text + "," + Status + "," + str(Priority) + "," + Sound + "," + ImageFile)

    def onDisconnect(self, Connection):
        Domoticz.Log("onDisconnect called")

    def onHeartbeat(self):
        Domoticz.Log("onHeartbeat called")
        if self.alive:
            if (self.heartbeatcounter % self.interval == 0):
                Devices[1].Update(nValue=2, sValue=self.state_dict[self.wemo_device.mode])
        else:
            onStart()

global _plugin
_plugin = WeMoCrockpotPlugin()

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
