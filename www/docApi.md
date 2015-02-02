WeIO overview
=============
Architecture
------------
### First steps
There are two ways to bring electricity to the board : using wires from DC transformer (5V only) or using micro USB cable. If you want to start fast use micro USB cable and plug the board into your computer. When using wires make attention to plug them with correct polarity. Powering up the board will result turning on LED power diode. Wait a few moments (about 1 minute) until LED AP stays steady. That means that Linux finished boot process, server is started and you board created AP - Access Point WiFi network that will permit you to enter to IDE Web Interface for the first time.
Choose from available networks on your computer "WeIO MACADDRESSNUMBER" and type inside your web browser http://weio.local:8080 address. This will prompt you the signup screen. If this address don't work it's possible that you don't have support for Bonjour on your machine. However you can always type http://10.0.0.1:8080 and get in WeIO.
After initial sign up into WeIO, everything is ready. WeIO application is always on port 8080 and user application will be on the stantard http port 80.

### Connect to WeIO and First Time Setup
After WeIO has been plugged to electricity and AP LED diode is lit up it's possible to connect to it's own WiFi.
Choose from available networks on your computer "WeIO rescue" and type inside your web browser http://weio.local:8080 address.
This will prompt you the signup screen. If this address don't work it's possible that you don't have support for Bonjour on your machine.
However you can always type http://10.0.0.1:8080 and get in WeIO. If this problem persists, just click on the button "Soft Reset" on the board.

Please fill in all fields. After setting up root password two additional services will be created : SSH access and SAMBA access. 

WeIO IDE environnement is now present on the screen. The next thing to do is to connect WeIO to your local WiFi network or so called STA network.

Feel free to explore WeIO WiFi configurator and try to create your own networks or to connect to existants. Once WeIO connected to Internet it will update it's local time and date, updates will be accessibles and other objects or services on the network can be directly accessed.

WeIO in the network
-------------------
### SSH server
WeIO is available over ssh connection using root as username. Password is the same one provided during signup procedure
```shell
ssh root@weio.local
```
### Samba server
WeIO is available over SMB or Samba sharing. This is used to explore contents of your projects or sources of WeIO platform. This is also  useful for transfering or backuping data between PC and WeIO board. Those who prefer using their own developement tools are welcome using SMB so they can edit codes externally from their prefered IDE.
SAMBA sharing can be accesed using "weio" as username and password is the same one provided during signup procedure.