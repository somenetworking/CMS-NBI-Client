# IMPORT STATEMENTS
from cmsnbiclient import (requests, xmltodict, pydash, random, Client)
# IMPORT STATEMENTS


class Update():

    def __init__(self, client_object: Client, network_nm: str = '', http_timeout: int = 1):
        """
        Description
        -----------
        Class (Update) is the update/merge query constructor/posting class for the E7 CMS NETCONF NBI

        Attributes
        ----------
        :param client_object:accepts object created by the cms_nbi_client.client.Client()
        :type client_object:Client

        :param network_nm:this parameter contains the node name, which is made of the case-sensitive name of the E7 OS platform, preceded by NTWK-. Example: NTWK-Pet02E7. The nodename value can consist of alphanumeric, underscore, and space characters, this is described in pg.26 of Calix Management System (CMS) R15.x Northbound Interface API Guide
        :type network_nm:str

        :param http_timeout:this parameter is fed to the request.request() function as a timeout more can be read at the request library docs
        :type http_timeout:int

        :var self.message_id:a positive int up to 32bit is generated with each call of self.message_id, the CMS server uses this str to match requests/responses, for more infomation please read pg.29 of Calix Management System (CMS) R15.x Northbound Interface API Guide
        :type self.message_id:str

        :var self.client_object:accepts object created by the cmsnbiclient.client.Client()
        :type self.client_object:object

        :raises:
            ValueError: Will be raised if the object provided is not of cmsnbiclient.client.Client()
            ValueError: Will be raised if the network_nm is not a str with a length at least 1 char
        """
        # Test if the provided object is of a Client instance

        if isinstance(client_object, Client):
            pass
        else:
            raise ValueError(f"""Update() accepts a instance of cmsnbiclient.client.Client(), a instance of {type(client_object)} was passed instead""")
        self.client_object = client_object
        # Test if the cms_netconf_url is a str object and contains the e7 uri
        if isinstance(self.client_object.cms_netconf_url, str):
            if self.client_object.cms_nbi_config['cms_netconf_uri']['e7'] in self.client_object.cms_netconf_url:
                pass
            else:
                raise ValueError(
                    f"""uri:{self.client_object.cms_nbi_config['cms_netconf_uri']['e7']} was not found in self.client_object.cms_netconf_url:{self.client_object.cms_netconf_url}""")
        else:
            raise ValueError(f"""self.client_object.cms_netconf_url must be a str object""")
        # TEST THE SESSION_ID VAR, THIS INSURES THAT ANY REQUEST ARE GOOD TO AUTHED
        if isinstance(self.client_object.session_id, str):
            if self.client_object.session_id.isdigit():
                pass
            else:
                raise ValueError(f"""self.client_object.session_id must be a int in a str object""")
        else:
            raise ValueError(f"""self.client_object.session_id must be a str object""")
        # TEST IF THE NETWORK_NM is an empty string
        if isinstance(network_nm, str):
            if len(network_nm) >= 1:
                pass
            else:
                raise ValueError(f"""network_nm cannot be an empty str""")
        else:
            raise ValueError(f"""network_nm must be a str""")
        # END PARAMETER TEST BLOCK

        # ASSIGNING CLASS VARIABLES
        self.network_nm = network_nm
        self.http_timeout = http_timeout

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
        return {'Content-Type': 'text/xml;charset=ISO-8859-1',
                'User-Agent': f'CMS_NBI_CONNECT-{self.cms_user_nm}'}

    @property
    def cms_user_nm(self):
        return self.client_object.cms_user_nm

    def ont(self, ont_id='', admin_state='', ont_sn='', reg_id='', sub_id='', ont_desc='', ontpwe3prof_id='', ontprof_id='', us_sdber_rate='', low_rx_opt_pwr_ne_thresh='', high_rx_opt_pwr_ne_thresh='', battery_present='', pse_max_power_budget='', poe_class_control='', replace_sn='0'):
        """
        Description
        -----------
        function ont() performs a http/xml Update query for the provided network_nm(e7_node) requesting an <Ont> object be updated with the provided details

        Attributes
        ----------
        :param ont_id: Identifies the ONT by its E7 scope ID (1 to 64000000),
        :type ont_sn:str

        :param admin_state: operational status of the created ONT, valid values are [disabled,enabled,enabled-no-alarms], this is explained further in pg.237 of Calix Management System (CMS) R15.x Northbound Interface API Guide
        :type admin_state:str

        :param ont_sn: identifies the Hexadecimal representation of the ONT serial number, to assign the SN at a later date, input '0', as described in pg.140 of Calix Management System (CMS) R15.x Northbound Interface API Guide
        :type ont_sn:str

        :param reg_id: ONT registration ID that is the RONTA identifier., as described in pg.232 of Calix Management System (CMS) R15.x Northbound Interface API Guide
        :type reg_id:str

        :param sub_id: Identifies the subscriber ID., as described in pg.63 of Calix Management System (CMS) R15.x Northbound Interface API Guide
        :type sub_id:str

        :param ont_desc: Identifies the ONT Description
        :type ont_desc:str

        :param ontpwe3prof_id: identifies the ID of the profile that sets the ONT PWE3 mode. Use 1 (also the default, if not supplied) for the system-default profile, which is set to use either T1 or E1 mode in the management interface. as described in pg.141 of Calix Management System (CMS) R15.x Northbound Interface API Guide
        :type ontpwe3prof_id:str

        :param ontprof_id: identifies the ID of a global or local ONT profile (1 to 50, or one of the default global profiles listed in Global ONT Profile IDs, as described in pg.282-285 of Calix Management System (CMS) R15.x Northbound Interface API Guide
        :type ontprof_id:str

        :param us_sdber_rate: Also Known as (Upstream Signal Degraded Error Rate) identifies the threshold for upstream bit errors before an alarm is raised range (2-6), please see pg.31 of E-Series EXA R3.x Maintenance and Troubleshooting Guide for more information
        :type us_sdber_rate:str

        :param low_rx_opt_pwr_ne_thresh: Also known as (Low Receive Optical Power Near End Threshold) identifies the lowest optical signal level that the ONT will accept before raising a low-rx-opt-pwr-ne alarm, default value(-30.0) accepts(-30.0 to -7.0), please see pg.61 & pg.421 of E-Series EXA R3.x Maintenance and Troubleshooting Guide for more information
        :type low_rx_opt_pwr_ne_thresh:str

        :param high_rx_opt_pwr_ne_thresh: Also known as (High Receive Optical Power Near End Threshold) identifies the highest optical signal level that the ONT will accept before raising a high-rx-opt-pwr-ne alarm, default value(-7.0) accepts(-30.0 to -7.0) please see pg.61 & pg.421 of E-Series EXA R3.x Maintenance and Troubleshooting Guide for more information
        :type high_rx_opt_pwr_ne_thresh:str

        :param battery_present: Identifies the requested batter-present state ie(true or false), this will determine if the ont alarms once it identifies the commercial power has been cut, please see pg.532 of Calix E-Series (E7 OS R3.1/R3.2) Engineering and Planning Guide for more information
        :type battery_present:str

        :param pse_max_power_budget: This defines the Power Sourcing Equipment (PSE) maximum power budget in Watts that the OLT can source on all Power over Ethernet (PoE) enabled Ethernet UNI ports. The PSE maximum power budget is effective in ONT only if the ownership is OMCI. default value(30) accepts(1 to 90), please see  E7 EXA R3.x GPON Applications Guide for more information
        :type pse_max_power_budget:str

        :param poe_class_control: the port can be classified to the type of Powered Device (PD) that will be connected to the port. Different classes of PD require different amounts of power, accepts 'enabled' or 'disabled', please see pg.532 of Calix E-Series (E7 OS R3.1/R3.2) Engineering and Planning Guide for more information
        :type poe_class_control:str

        :param replace_sn: '0' or '1', this option indicates if the ont's CXNK serial number is being replaced. ont_sn must be set to '0'
        :type replace_sn:str

        :raise:
            ConnectTimeout: Will be raised if the http(s) connection times-out
            ValueError: Will be raised if the ont_id is not an int str ie whole number

        :return: ont() returns a response.models.Response object on a failed call, and a nested dict on a successful call

        Example
        ______

        Next we create a cmsnbiclient.E7.Update() instance and pass the cms_nbi_client.Client() instance to it
        netconf_update = cmsnbiclient.E7.Update(client, network_nm='NTWK-Example_Network, http_timeout=5)
        Once the netconf_update object is created we can then call the ont() function and update ont variables for a specific ont
        For any updated query an ont_id must be provided in the ont_id var
        Only the var(s) being updated needs to be supplied

        Updating the ont 1 admin_state>>disabled
        netconf_update.ont(ont_id='1',
                           admin_state='disabled')

        Updating the ont 2 Subscriber Id  && Description
        netconf_update.ont(ont_id='2',
                           sub_id='9999999',
                           ont_desc='example_ont')

        Updating ont 4 to False on the battery_present
        netconf_update.ont(ont_id='4',
                           battery_present='false')

        Replace an ONT with a new ont
        this requires two calls one to unlink the cxnk and another to link a new cxnk
        netconf_update.ont(ont_id='4',
                           ont_sn='0',
                           replace_sn='1')

        netconf_update.ont(ont_id='4',
                           ont_sn='9999')
        """
        # Since i dont know how to filter parameters that are empty this is what im doing , hopefully it works
        # using change_var_list as a tmp list to filter out any ont vars that are not being changed, ie the empty vars will be removed from the dictionary
        # before using xmltodict.unparse to convert it to a xml str
        par_inputs = vars()
        if isinstance(par_inputs['ont_id'], str):
            if par_inputs['ont_id'].isdigit and not par_inputs['ont_id'] == '0':
                pass
            else:
                raise ValueError(f"""{par_inputs['ont_id']} NEEDS TO BE A INT STR BETWEEN 1 and 64000000""")
        # APPLYING STRUCTURE TO THE PROVIDED PARAMETERS BEFORE PARSING, THIS IS DESIGN SO XMLTODICT CAN UNPARSE THEM INTO THE CORRECT XML FORMAT
        change_var = {'admin': par_inputs['admin_state'],
                      'battery-present': par_inputs['battery_present'],
                      'descr': par_inputs['ont_desc'],
                      'high-rx-opt-pwr-ne-thresh': par_inputs['high_rx_opt_pwr_ne_thresh'],
                      'low-rx-opt-pwr-ne-thresh': par_inputs['low_rx_opt_pwr_ne_thresh'],
                      'ontprof': {'id': {'ontprof': par_inputs['ontprof_id']}, 'type': 'OntProf'},
                      'poe-class-control': par_inputs['poe_class_control'],
                      'pse-max-power-budget': par_inputs['pse_max_power_budget'],
                      'pwe3prof': {'id': {'ontpwe3prof': par_inputs['ontpwe3prof_id']}, 'type': 'OntPwe3Prof'},
                      'reg-id': par_inputs['reg_id'],
                      'serno': par_inputs['ont_sn'],
                      'subscr-id': par_inputs['sub_id'],
                      'us-sdber-rate': par_inputs['us_sdber_rate'],
                      'linked-pon': par_inputs['replace_sn']}
        # REMOVING ANY Key/Value pair that contains an empty value
        change_var = dict([(vkey, vdata) for vkey, vdata in change_var.items() if(vdata)])
        # REMOVING ANY KEY/VALUE pairs where the lowest value is empty
        # FOR link-pon it sets it to None if the value is 1(True)
        if not change_var['ontprof']['id']['ontprof']:
            change_var.pop('ontprof')
        if not change_var['pwe3prof']['id']['ontpwe3prof']:
            change_var.pop('pwe3prof')
        if change_var['linked-pon'] == '1':
            change_var['linked-pon'] = None
        else:
            change_var.pop('linked-pon')

        chang_xml = xmltodict.unparse(change_var, full_document=False)
        payload = f"""<soapenv:Envelope xmlns:soapenv="http://www.w3.org/2003/05/soap-envelope">
                        <soapenv:Body>
                            <rpc message-id="{self.message_id}" nodename="{self.network_nm}" username="{self.cms_user_nm}" sessionid="{self.client_object.session_id}">
                                <edit-config>
                                <target>
                                <running/>
                                </target>
                                    <config>
                                        <top>
                                            <object operation="merge" get-config="true">
                                                <type>Ont</type>
                                                <id>
                                                    <ont>{ont_id}</ont>
                                                </id>{chang_xml}
                                            </object>
                                        </top>
                                    </config>
                                </edit-config>
                            </rpc>
                            </soapenv:Body>
                        </soapenv:Envelope>"""

        if 'https' not in self.client_object.cms_netconf_url[:5]:
            try:
                response = requests.post(url=self.client_object.cms_netconf_url, headers=self.headers, data=payload, timeout=self.http_timeout)
            except requests.exceptions.Timeout as e:
                raise e
        else:
            # TODO:Need to implement HTTPS handling as the destination port will be different than the http port
            pass

        if response.status_code != 200:
            # if the response code is not 200 FALSE and the request.Models.response object is returned.
            return response

        else:
            resp_dict = xmltodict.parse(response.content)
            if pydash.objects.has(resp_dict, 'soapenv:Envelope.soapenv:Body.rpc-reply.data.top.object'):
                return resp_dict['soapenv:Envelope']['soapenv:Body']['rpc-reply']['data']['top']['object']
            else:
                return response

    def ont_geth(self, ont_id: str = '', ontethge: str = ''):
        """
        Description
        -----------
        function ont_geth() performs a http/xml  query for the provided network_nm(e7_node) requesting the current data for the specified ontethge

        Attributes
        ----------
        :param ont_id: Identifies the ONT by its E7 scope ID (1 to 64000000).

        :param ontethge: Identifies the ONT-GE port number (1 to 8).

        :raise:
            ConnectTimeout: Will be raised if the http(s) connection between the client and server times-out

        :return: ont() returns a response.models.Response object on a failed call, and a nested dict on a successful call
        """

        payload = f"""<soapenv:Envelope xmlns:soapenv="http://www.w3.org/2003/05/soap-envelope">
                                <soapenv:Body>
                                    <rpc message-id="{self.message_id}" nodename="{self.network_nm}" username="{self.cms_user_nm}" sessionid="{self.client_object.session_id}">
                                        <edit-config>
                                            <target>
                                                <running/>
                                            </target>
                                            <config>
                                                <top>
                                                    <object operation="merge">
                                                        <type>OntEthGe</type>
                                                        <id>
                                                            <ont>1</ont>
                                                            <ontslot>3</ontslot>
                                                            <ontethge>1</ontethge>
                                                        </id>
                                                        <intf></intf>
                                                        <admin>disabled</admin>
                                                        <subscr-id></subscr-id>
                                                        <descr></descr>
                                                        <gos>
                                                            <type>OntEthPortGos</type>
                                                            <id>
                                                                <ontethportgos>1</ontethportgos>
                                                            </id>
                                                        </gos>
                                                        <duplex>full</duplex>
                                                        <sec>
                                                            <type>EthSecProf</type>
                                                            <id>
                                                                <ethsecprof>1</ethsecprof>
                                                            </id>
                                                        </sec>
                                                        <disable-on-batt>true</disable-on-batt>
                                                        <link-oam-events>false</link-oam-events>
                                                        <accept-link-oam-loopbacks>false</accept-link-oam-loopbacks>
                                                        <dhcp-limit-override>none</dhcp-limit-override>
                                                        <force-dot1x>none</force-dot1x>
                                                        <role>uni</role>
                                                        <pbit-map>
                                                            <type>DscpMap</type>
                                                            <id>
                                                                <dscpmap>1</dscpmap>
                                                            </id>
                                                        </pbit-map>
                                                        <speed>auto</speed>
                                                        <poe-power-priority>medium</poe-power-priority>
                                                        <poe-class-control>disabled</poe-class-control>
                                                        <voice-policy-profile></voice-policy-profile>
                                                        <ppte-power-control>false</ppte-power-control>
                                                        <policing>disable</policing>
                                                    </object>
                                                </top>
                                            </config>
                                        </edit-config>
                                    </rpc>
                                    </soapenv:Body>
                                </soapenv:Envelope>"""