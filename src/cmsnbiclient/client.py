# IMPORT STATEMENTS
from cmsnbiclient import (requests, json, os, random, xmltodict, pydash)
# IMPORT STATEMENTS


class Client:

    def __init__(self):
        """
        Description
        -----------
        Class (Client) is the main class and contains the config, message_id and session_id variables, login function, logout function, update_config function.

        Attributes
        ----------
        :var self.cms_nbi_config:a nested dict generated by reading the cms_nbi_config.json file located in the CWD of Client.py this var contains the complete config
        :type self.cms_nbi_config:dict

        :var self.cms_netconf_url:this class var contains the full URL for the specific CMS API NBI
        :type self.cms_netconf_url:str

        :var self.message_id:CMS uses this 32bit int string variable to identify incoming/outgoing http(s) requests/responses
        :type self.message_id:str

        :var self.session_id:this class var is generated by a successful login_netconf() call, CMS uses this var in its auth process
        :type self.session_id:str
        """
        # default config data
        self.cms_nbi_config = {}
        config_data = {'config': {'cms_nodes': {'default': {
            'connection': {'protocol': {'http': 'http', 'https': 'https'}, 'netconf_http_port': '18080',
                           'netconf_https_port': '18443', 'rest_http_port': '8080', 'http_timeout': 500,
                           'cms_node_ip': 'localhost'},
            'cms_creds': {'user_nm': 'rootgod', 'pass_wd': 'root'}
            }
                                                },
                                  'cms_netconf_uri': {'e7': '/cmsexc/ex/netconf', 'c7/e3/e5-100': '/cmsweb/nc',
                                                      'ae_ont': '/cmsae/ae/netconf'},
                                  'cms_rest_uri': {'devices': '/restnbi/devices?deviceType=',
                                                   'region': '/restnbi/region', 'topology': '/restnbi/toplinks',
                                                   'profile': '/restnbi/profiles?profileType='}
                                  }
                       }
        # collects the current working directory(cwd) then creates a path for the cms_nbi_config.json file
        cwd = os.getcwd()
        cf_path = os.path.join(cwd, 'cms_nbi_config.json')

        def config_file_checker(data=config_data, config_file_path=cf_path):
            # function to check if the cms_nbi_config.json file exist in the local dir
            # if it doesn't it will dump the default config to the cms_nbi_config.json file in local dir
            if not os.path.exists(config_file_path):
                with open(config_file_path, 'w') as config_file:
                    json.dump(data, config_file, indent=5)
                return True
            else:
                pass

        def config_importer(config_file_path=cf_path):
            # function to import the stored json data at cms_nbi_config.json
            with open(config_file_path, 'r') as cf_file:
                self.cms_nbi_config = json.load(cf_file)['config']

        # try/except clause to check if the config file exist and import the data
        # if cms_nbi_config.json does not exist then it will create it and dump a default config into it
        try:
            config_importer()
        except FileNotFoundError:
            if config_file_checker(data=config_data):
                config_importer()
        # create Cms_nbi_connect vars
        self.cms_netconf_url = None
        self.session_id = None
        self.cms_user_nm = None
        self.cms_user_pass = None

    @property
    def message_id(self):
        """
        Description
        -----------
        :var self.message_id: a positive 32bit int is generated with each call of self.message_id, the CMS server uses this str to match requests/responses, for more infomation please read pg.29 of Calix Management System (CMS) R15.x Northbound Interface API Guide
        :return: self.message_id
        """
        return str(random.getrandbits(random.randint(2, 31)))

    @property
    def headers(self):
        return {'Content-Type': 'text/xml;charset=ISO-8859-1', 'User-Agent': f'CMS_NBI_CONNECT-{self.cms_user_nm}'}

    def login_netconf(self, cms_user_nm='rootgod', cms_user_pass='root', protocol='http', port='18080', cms_node_ip='localhost', uri='', http_timeout=1):
        """
        Description
        -----------
        function login_netconf() performs the login function as explained in the in pg.14-15 of Calix Management System (CMS) R15.x Northbound Interface API Guide

        Parameter(s)
        ------------

        :param cms_user_nm: this var contains the username for the CMS USER ACCOUNT utilized in the interactions, this is described in pg.15 of Calix Management System (CMS) R15.x Northbound Interface API Guide
        :type cms_user_nm:str

        :param cms_user_pass: this var contains the plain text password for the provided username, this is described in pg.15 of Calix Management System (CMS) R15.x Northbound Interface API Guide
        :type cms_user_pass:str

        :param protocol: this var determines the protocol to use when building the CMS NETCONF NBI URL, CMS supports http/s as described in pg.14 of Calix Management System (CMS) R15.x Northbound Interface API Guide
        :type protocol:str

        :param port: this var determines the TCP/UDP port to use when building the CMS NETCONF NBI URL, this will be dependent on whether HTTP or HTTPS was chosen, this is described in pg.14 of Calix Management System (CMS) R15.x Northbound Interface API Guide
        :type port:str

        :param cms_node_ip: this var contains the FQDN/IP of the targeted CMS node
        :type cms_node_ip:str

        :param uri: this var contains the uri specifying the CMS NBI, this is described in pg.14 of Calix Management System (CMS) R15.x Northbound Interface API Guide
        :type uri:str

        :param http_timeout: this var contains the http_timeout for the request library, this is in the form of an int
        :type http_timeout:int

        :raise:
            ConnectTimeout: Will be raised if the http(s) connection timesout

        :return: login_netconf() returns '0' on a successful call and a response.models.Response object on a failed call
        """

        if self.cms_netconf_url is None:
            self.cms_netconf_url = f"{protocol}://{cms_node_ip}:{port}{uri}"
        else:
            pass

        if len(cms_user_nm) >= 1:
            self.cms_user_nm = cms_user_nm
        else:
            raise ValueError(f"""cms_user_nm parameter must be a string with at least one char""")

        if len(cms_user_pass) >= 1:
            self.cms_user_pass = cms_user_pass
        else:
            raise ValueError(f"""cms_user_pass parameter must be a string with at least one char""")

        payload = f"""<?xml version="1.0" encoding="UTF-8"?>
                    <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
                        <soapenv:Body>
                            <auth message-id="{self.message_id}">
                                <login>
                                    <UserName>{self.cms_user_nm}</UserName>
                                    <Password>{self.cms_user_pass}</Password>
                                </login>
                            </auth>
                        </soapenv:Body>
                    </soapenv:Envelope>"""

        if protocol == 'http':
            try:
                response = requests.post(url=self.cms_netconf_url, headers=self.headers, data=payload, timeout=http_timeout)
            except requests.exceptions.Timeout as e:

                # future came and it decided to have raise
                raise e
        else:
            # TODO:Need to implement https handling
            pass

        if response.status_code != 200:
            # if the response code is not 200 FALSE and the request.post object is returned.
            return False, response

        else:
            # converts the response.content to a dict using xmltodict library
            resp_dict = xmltodict.parse(response.content)
            if pydash.objects.has(resp_dict, 'Envelope.Body.auth-reply.ResultCode'):
                # test if the resp_dict has a Resultcode key this indicates a response from the server
                if resp_dict['Envelope']['Body']['auth-reply']['ResultCode'] == '0':
                    # Resultcode is 0, the login was successful, the sessionid is saved in memory
                    self.session_id = resp_dict['Envelope']['Body']['auth-reply']['SessionId']
                    return resp_dict['Envelope']['Body']['auth-reply']['ResultCode']

                elif resp_dict['Envelope']['Body']['auth-reply']['ResultCode'] == '6':
                    # Resultcode is 6, the login was unsuccessful, returns false and the request.post object
                    return response

                else:
                    # other result codes will need to be worked out
                    return response
            else:
                # other responses will need to be worked out and coded for
                return response

    def logout_netconf(self, protocol='http', port='18080', cms_node_ip='localhost', uri='', http_timeout=1):
        """
        Description
        -----------
        function logout_netconf() performs the logout function as explained in the in pg.14-16 of Calix Management System (CMS) R15.x Northbound Interface API Guide

        Parameter(s)
        ------------
        :param protocol: this var determines the protocol to use when building the CMS NETCONF NBI URL, CMS supports http/s as described in pg.14 of Calix Management System (CMS) R15.x Northbound Interface API Guide
        :type protocol:str

        :param port: this var determines the TCP/UDP port to use when building the CMS NETCONF NBI URL, this will be dependent on whether HTTP or HTTPS was chosen, this is described in pg.14 of Calix Management System (CMS) R15.x Northbound Interface API Guide
        :type port:str

        :param cms_node_ip: this var contains the FQDN/IP of the targeted CMS node
        :type cms_node_ip:str

        :param uri: this var contains the uri specifying the CMS NBI, this is described in pg.14 of Calix Management System (CMS) R15.x Northbound Interface API Guide
        :type uri:str

        :param http_timeout: this var contains the http_timeout for the request library, this is in the form of an int
        :type http_timeout:int

        :raise:
            ConnectTimeout: Will be raised if the http(s) connection timesout

        :return: logout_netconf() returns a tuple with (False,requests.models.Response object) or (True,'')
        """

        if self.cms_netconf_url is None:
            self.cms_netconf_url = f"{protocol}://{cms_node_ip}:{port}{uri}"

        payload = f"""<?xml version="1.0" encoding="UTF-8"?>
                        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
                            <soapenv:Body>
                                <auth message-id="{self.message_id}">
                                    <logout>
                                        <UserName>{self.cms_user_nm}</UserName>
                                        <SessionId>{self.session_id}</SessionId>
                                    </logout>
                                </auth>
                            </soapenv:Body>
                        </soapenv:Envelope>"""

        if protocol == 'http':
            try:
                response = requests.post(url=self.cms_netconf_url, headers=self.headers, data=payload, timeout=http_timeout)
            except requests.exceptions.Timeout as e:
                # debating between exit and raise will update in future
                raise e
        else:
            # will need to research how to implement https connection with request library
            pass

        if response.status_code != 200:
            # if the response code is not 200 response.models.Response is returned.
            return response

        else:
            # converts the response.content to a dict using xmltodict library
            resp_dict = xmltodict.parse(response.content)
            if pydash.objects.has(resp_dict, 'Envelope.Body.auth-reply.ResultCode'):
                # test if the resp_dict has a Resultcode key this indicates a response from the server
                if resp_dict['Envelope']['Body']['auth-reply']['ResultCode'] == '0':
                    # Resultcode is 0, the logout was successful,
                    # TODO: Research how to correctly implement a __del__ for a cmsnbiclient instance
                    # it will also return the ResultCode
                    self.session_id = None
                    return '0'
                elif resp_dict['Envelope']['Body']['auth-reply']['ResultCode'] == '2':
                    # Resultcode is 2, the logout was unsuccessful, this means that the one of the required variables were incorrect,
                    # (session_id or username)
                    return response
                else:
                    # other result codes will need to be worked out
                    return response
            else:
                # other responses will need to be worked out and coded for
                return response

    def update_config(self, pass_wd='', user_nm='', cms_node_ip='', cms_node_name=''):
        """
        Description
        ___________
        function update_config() updates the cms_nbi_config file with the new CMS node data, it will then pull the updated config into the self.cms_nbi_config

        Paremeter(s)
        ------------
        :param pass_wd: this param is the password for the CMS USER ACCOUNT provided in the user_nm param
        :type pass_wd:str

        :param user_nm: this param is the username for the CMS USER ACCOUNT
        :type user_nm:str

        :param cms_node_ip: this param is the FQDN/IP of the CMS node
        :type cms_node_ip:str

        :param cms_node_name: this param is the 'name' of the CMS node
        :type cms_node_name:str

        :return: update_config() currently does not return any objects
        """
        cwd = os.getcwd()
        cf_path = os.path.join(cwd, '../cms_nbi_config.json')

        def config_file_updater(data=self.cms_nbi_config, config_file_path=cf_path):
            # function to check if the cms_nbi_config.json file exist in the local dir
            # if it doesn't it will dump the default config to the cms_nbi_config.json file in local dir
            with open(config_file_path, 'w') as config_file:
                json.dump(data, config_file, indent=5)

        new_cms_node = {'cms_creds': {'pass_wd': pass_wd, 'user_nm': user_nm},
                        'connection': {'cms_node_ip': cms_node_ip,
                                       'http_timeout': 500,
                                       'netconf_http_port': '18080',
                                       'netconf_https_port': '18443',
                                       'protocols': {'http': 'http', 'https': 'https'},
                                       'rest_http_port': '8080'}
                        }

        if isinstance(cms_node_name, str) and len(cms_node_name) >= 1:
            # checks to make sure the cms_node_name is a string and at least 1 char long
            # updated the config in memory then on disk
            self.cms_nbi_config['cms_nodes'][cms_node_name] = new_cms_node
            new_cms_config = {}
            new_cms_config['config'] = self.cms_nbi_config
            config_file_updater(data=new_cms_config)

