"""This module takes the name of the profile and return the Wi-Fi details like SSID name,
Authentication and Key. Generating the Saved Wi-Fi details of some special SSID's gives a
problem. For a different type of SSID name, like some SSID name contain 'emojis' while some
contain special symbols which create a lot of problems when dealing with command prompt. So,
generating XML file of the per profile doesn't resolve some problem but not all. Some SSID's
like 'Redm"i=" are still creating problems.
"""

import os, re, subprocess, time, uuid

from xml.etree import ElementTree
from xml.dom import minidom


def RUN(cmd): return subprocess.run(cmd, shell=True, capture_output=True, text=True)

class WiFi:
    dicting = dict(ssid='name', key='keyMaterial', auth='authentication', mode='connectionMode', type='connectionType', seed='randomizationSeed', random='enableRandomization')

    def __str__(self): return self.name

    def __repr__(self): return f'<{self}>'

    def __init__(self, name='', xmlfile=''):

        self.name = name
        self.hex = ''
        self.connectionType = ''
        self.connectionMode = ''
        self.authentication = ''
        self.encryption = ''
        self.useOneX = ''
        self.keyType = ''
        self.protected = ''
        self.keyMaterial = ''
        self.enableRandomization = ''
        self.randomizationSeed = ''
                
        if xmlfile: self.xml_parsing(xmlfile)
        # elif name: self.parse_self()
    
    def get(self, attr):
        if attr in WiFi.dicting:
            attr = WiFi.dicting[attr]
        return self.__dict__[attr]
        
    def parse(self, element):
        dictt = {}
        for elem in element:
            if elem.text.strip(): dictt.update({elem.tag.split('}')[1]: elem.text})
            if len(elem): dictt.update(self.parse(elem))
        return dictt
    # def parse_self(self):
    #     output = RUN("netsh wlan show profile")

    def xml_parsing(self, xmlfile):
        """Parsing XML file to retrieve ssid, authentication and key(if any).
        """
        if not os.path.isfile(xmlfile): raise ValueError('xmlfile is invalid')

        tree = ElementTree.parse(xmlfile)

        dictt = self.parse(tree._root)
        self.__dict__.update(dictt)

        os.remove(xmlfile)


class WiFi_Manager:
    """ This class generates and return the SSID, Authentication, Key
    for the Wi-Fi profile as given as input.
    """

    def __getitem__(self, item): return self.wifi_profiles[item]
    def __len__(self): return len(self[:])

    def __init__(self, app_path='', lists=None, parse=0):

        """
            This method is used to check if the necessary folder, file is present,
        otherwise create it. Also, initialize object variables.
        """
        
        self.interface_name = None
        self.ssid_name = None
        self._ip = ''

        self.app_path = app_path or os.path.dirname(__file__)
        
        self.temp_path = os.path.join(self.app_path, 'temps')

        if not os.path.isdir(self.temp_path): os.mkdir(self.temp_path)

        if lists:
            self.wifi_profiles = lists
            self.profiles = [lis.name for lis in lists]

        elif parse: self.parse_wifi_profiles()

    @property
    def mac(self): return ':'.join(re.findall('..', '%012x'%uuid.getnode()))

    @property
    def ip(self):
        if self._ip: return self._ip
        t = RUN('netsh interface ipv4 show ipaddresses').stdout
        tt = t.splitlines()

        for a, b in enumerate(tt):
            if 'Wi-Fi' in b:
                self._ip = tt[a+4].split()[-1]
                return self._ip

    def current_profiles(self):
        profiles = []
        output = RUN("netsh wlan show profile")

        for line in output.stdout.splitlines():
            _line = line.split(':')
            if len(_line) > 1:
                ne = ''.join(_line[1:]).lstrip()
                if ne: profiles.append(ne)
        return profiles

    def create_from_xml(self):
        xmlfiles = [os.path.join(self.temp_path, xml) for xml in os.listdir(self.temp_path) if xml.startswith('Wi-Fi-') and xml.endswith('.xml')]
        
        for xml in xmlfiles:
            if os.path.isfile(xml):
                wifi = WiFi(xmlfile=xml)
                self.wifi_profiles.append(wifi)
                self.profiles.append(wifi.name)

    def create_wifi_profile(self, name):
        output = RUN(f'netsh wlan export profile name="{name}" key=clear folder="{self.temp_path}"')
        self.create_from_xml()

    
    def parse_wifi_profiles(self):
        """ Generates the list of Wi-Fi saved in your system and save it in parent folder of temps.
        """
        self.profiles = []
        self.wifi_profiles = []

        profiles = self.current_profiles()
        
        for profile in profiles: self.create_wifi_profile(profile)

    refresh = parse_wifi_profiles

    @property
    def connected_to(self):
        """ Check if system is connected to any Wi-Fi network. If true,
        return wifi object else return None.
        """
        output = RUN('netsh wlan show interfaces | findstr "Name State SSID"')

        my_regex = r"Name.*?connected.*?(?= *BSSID)"
        network_status = re.search(my_regex, output.stdout, re.DOTALL)

        if network_status is None: return None

        network_status = network_status.group()
        
        self.interface = re.findall(r"[\n\r-<>():]?.*Name\s*: ([^\n\r]*)", network_status)[0]

        self.ssid_name = re.findall(r"[\n\r-<>():]?.*SSID\s*: ([^\n\r]*)", network_status)[0]

        for wifi in self:
            if self.ssid_name == wifi.name: return wifi

    @property
    def is_connected(self): return True if self.connected_to else False
    
    def disconnect(self):
        """ Disconnects if system is connected to any Wi-Fi network"""

        output = RUN('netsh wlan disconnect interface = "' + self.interface_name + '"')

        # Check if system is disconnected from network successfully.
        message = "Sorry, unable to disconnect"

        return True if output.returncode == 0 else False
    
    # WARNING
    # There is a bug in below function i.e., when user disconnect and reconnect to same network
    # and network is not available anymore. It still shows the result that connection to same
    # network is done successfully. It is a bug of 'command prompt'.
    def connect(self):
        """ Try to reconnect to same network. """

        output = RUN(f'netsh wlan connect name="{self.ssid_name}" interface = "{self.interface_name}"')

        # Check if system reconnect to same network successfully.
        if output.returncode != 0:
            message = "Unable to reconnect(either previous network is not available in range or profile is deleted)"
            return False
        return True

    def add_profile(self, ssid, mode, auth, encrypt, key):
        """ Create xml file and add profile to system"""

        file_name = str(sum([ord(i) for i in self.ssid.get()]))

        def saving_file(xml):
            """ Save user profile in xml format to temp_ dir."""

            xml_string = ElementTree.tostring(xml)
            parsed = minidom.parseString(xml_string)
            with open(self.app_path + "\\temp_\\" + file_name + ".xml", "w") as file:
                file.write(parsed.toprettyxml(indent="        "))

        parse_xml = ElementTree.parse(os.path.dirname(os.path.realpath(__file__)) +
                                "/data/sampleProfile.xml")

        # The below code will parse the sample xml file
        # and fill important details entered by the user.
        root_tree = parse_xml.getroot()
        root_tree[0].text = self.ssid.get()
        root_tree[1][0][0].text = self.ssid.get()
        root_tree[3].text = self.connection_mode.get().lower()
        security = root_tree[4][0]
        security[0][0].text = self.authentication.get()
        security[0][1].text = self.encryption.get()
        if self.authentication.get() != "open":
            ElementTree.SubElement(security, "sharedKey")
            ElementTree.SubElement(security[1], "keyType").text = "passPhrase"
            ElementTree.SubElement(security[1], "protected").text = "false"
            ElementTree.SubElement(security[1], "keyMaterial").text = self.password.get()

        # Save the xml file
        saving_file(root_tree)

        # Add profile to the system.
        temp_path = 'netsh wlan add profile filename="' + self.app_path + "\\temp_\\"
        output_ = RUN(temp_path + file_name + '.xml"')
        os.remove(self.app_path + "\\temp_\\" + file_name + ".xml")

        # If unable to add profile.
        if output_.returncode != 0:
            message = "Sorry, Unable to add profile.\n(You entered wrong details " \
                      "or else you don't have admin rights.)"
            image_ = "error"

        else:
            message = "Profile added successfully (Please Refresh)"
            image_ = "warning"

    def delete_profile(self, name):
        
        command = 'netsh wlan delete profile name="' + name + '"'
        output = RUN(f'netsh wlan delete profile name="{name}"')

        if output.returncode != 0: raise ValueError(output.stderr)


w = WiFi_Manager()
print(w.ip, w.connected_to)
