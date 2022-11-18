# IMPORT STATEMENTS
from cmsnbiclient import (requests, xmltodict, pydash, Client)
# IMPORT STATEMENTS


class Create():

    def __init__(self, cms_nbi_connect_object):
        """
        Description
        -----------
        Class (Create) is the creation query constructor/posting class for the E7 CMS NETCONF NBI

        Attributes
        ----------
        :param cms_nbi_connect_object: Create() accepts an object create from the cms_nbi_client.Client() class
        :var self.cms_nbi_connect_object: accepts object created by the cms_nbi_client.Client()
        :type self.cms_nbi_connect_object: object
        """
        # Test if the provided object is of a CMS_NBI_Client instance

        if isinstance(cms_nbi_connect_object, Client):
            pass
        else:
            raise ValueError(f"""Query_E7_Data accepts a instance of cms_nbi_client.E7.client.Client, a instance of {type(cms_nbi_connect_object)} was provided""")
        self.cms_nbi_connect_object = cms_nbi_connect_object
        # Test if the cms_netconf_url is a str object and contains the e7 uri
        if isinstance(self.cms_nbi_connect_object.cms_netconf_url, str):
            if self.cms_nbi_connect_object.cms_nbi_config['cms_netconf_uri']['e7'] in self.cms_nbi_connect_object.cms_netconf_url:
                pass
            else:
                raise ValueError(f"""uri:{self.cms_nbi_connect_object.cms_nbi_config['cms_netconf_uri']['e7']} was not found in self.cms_nbi_connect_object.cms_netconf_url:{self.cms_nbi_connect_object.cms_netconf_url}""")
        else:
            raise ValueError(f"""self.cms_nbi_connect_object.cms_netconf_url must be a str object""")
        # test if the session_id is a str object
        if isinstance(self.cms_nbi_connect_object.session_id, str):
            if self.cms_nbi_connect_object.session_id.isdigit():
                pass
            else:
                raise ValueError(f"""self.cms_nbi_connect_object.session_id must be a int in a str object""")
        else:
            raise ValueError(f"""self.cms_nbi_connect_object.session_id must be a str object""")

    def ont(self, message_id='1', cms_user_nm='rootgod', network_nm='', http_timeout=1, ont_id='0',
            admin_state='enabled', ont_sn='0', reg_id='', sub_id='', ont_desc='', ontpwe3prof_id='1', ontprof_id='',
            us_sdber_rate='5', low_rx_opt_pwr_ne_thresh='-30.0', high_rx_opt_pwr_ne_thresh='-7.0',
            battery_present='false', pse_max_power_budget='30', poe_class_control='disabled'):
        """
        Description
        -----------
        function ont() performs a http/xml creation query for the provided network_nm(e7_node) requesting an <Ont> object be created with the provided details

        Attributes
        ----------
        :param message_id: is the message_id used by the cms server to correlate http responses, if None is provided and self.cms_nbi_connect_object.message_id is None the default of 1 will be used
        :type message_id:str

        :param cms_user_nm: this parameter contains the username for the CMS USER ACCOUNT utilized in the interactions, this is described in pg.15 of Calix Management System (CMS) R15.x Northbound Interface API Guide
        :type cms_user_nm:str

        :param network_nm: this parameter contains the node name, which is made of the case-sensitive name of the E7 OS platform, preceded by NTWK-. Example: NTWK-Pet02E7. The nodename value can consist of alphanumeric, underscore, and space characters, this is described in pg.26 of Calix Management System (CMS) R15.x Northbound Interface API Guide
        :type network_nm:str

        :param http_timeout: this parameter is fed to the request.request() function as a timeout more can be read at the request library docs
        :type http_timeout:int

        :param ont_id: Identifies the ONT by its E7 scope ID (1 to 64000000), submitting '0' requests the ont be built on the first available ID, as described in pg.129 of Calix Management System (CMS) R15.x Northbound Interface API Guide
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

        :raise:
            ConnectTimeout: Will be raised if the http(s) connection timesout

        :return: ont() returns a response.models.Response object on a failed call, and a nested dict on a successful call

        Example
        -----------
        IMPORTANT NOTE

        You will need to submit the correct structured dictionary to the int_id param

        # CREATE A DEFAULT 812G ONT, USING THE FIRST ONT_ID available on NTWK-Example_Name.
        # Coupled with ont_sn='0', this call will tell the cms server to create a new ont record with no SN allowing us to fill it in later.
        create_e7_data.ont( message_id='1',
                            cms_user_nm=client.cms_nbi_config['cms_nodes']['example_node']['cms_creds']['user_nm'],
                            network_nm='NTWK-Example_Name',
                            http_timeout=1,
                            ont_id='0',
                            admin_state='enabled',
                            ont_sn='0',
                            reg_id='',
                            sub_id='999999',
                            ont_desc='Example_Description',
                            ontpwe3prof_id='1',
                            ontprof_id='162')

        # CREATE A DEFAULT 812G ONT, USING THE FIRST ONT_ID AVAILABLE ONT NTWK-Example_Name
        # With this call we provided the ONT_SN, this will create a record tying the ONT_SN to the ONT provisioning, once the ont is discovered by the E7 the config is pushed.
        create_e7_data.ont( message_id='1',
                        cms_user_nm=client.cms_nbi_config['cms_nodes']['example_node']['cms_creds']['user_nm'],
                        network_nm='NTWK-Example_Name',
                        http_timeout=1,
                        ont_id='0',
                        admin_state='enabled',
                        ont_sn='0',
                        reg_id='',
                        sub_id='999999',
                        ont_desc='Example_Description',
                        ontpwe3prof_id='1',
                        ontprof_id='162')
        """

        payload = f"""<soapenv:Envelope xmlns:soapenv="http://www.w3.org/2003/05/soap-envelope">
                        <soapenv:Body>
                            <rpc message-id="{message_id}" nodename="{network_nm}" username="{cms_user_nm}" sessionid="{self.cms_nbi_connect_object.session_id}">
                                <edit-config>
                                    <target>
                                        <running/>
                                    </target>
                                    <config>
                                        <top>
                                            <object operation="create" get-config="true">
                                                <type>Ont</type>
                                                <id>
                                                    <ont>{ont_id}</ont>
                                                </id>
                                                <admin>{admin_state}</admin>
                                                <serno>{ont_sn}</serno>
                                                <reg-id>{reg_id}</reg-id>
                                                <subscr-id>{sub_id}</subscr-id>
                                                <descr>{ont_desc}</descr>
                                                <pwe3prof>
                                                    <type>OntPwe3Prof</type>
                                                    <id>
                                                        <ontpwe3prof>{ontpwe3prof_id}</ontpwe3prof>
                                                    </id>
                                                </pwe3prof>
                                                <ontprof>
                                                    <type>OntProf</type>
                                                    <id>
                                                        <ontprof>{ontprof_id}</ontprof>
                                                    </id>
                                                </ontprof>
                                                <us-sdber-rate>{us_sdber_rate}</us-sdber-rate>
                                                <low-rx-opt-pwr-ne-thresh>{low_rx_opt_pwr_ne_thresh}</low-rx-opt-pwr-ne-thresh>
                                                <high-rx-opt-pwr-ne-thresh>{high_rx_opt_pwr_ne_thresh}</high-rx-opt-pwr-ne-thresh>
                                                <battery-present>{battery_present}</battery-present>
                                                <pse-max-power-budget>{pse_max_power_budget}</pse-max-power-budget>
                                                <poe-class-control>{poe_class_control}</poe-class-control>
                                            </object>
                                        </top>
                                    </config>
                                </edit-config>
                            </rpc>
                        </soapenv:Body>
                    </soapenv:Envelope>"""

        headers = {'Content-Type': 'text/xml;charset=ISO-8859-1',
                   'User-Agent': f'CMS_NBI_CONNECT-{cms_user_nm}'}

        if 'https' not in self.cms_nbi_connect_object.cms_netconf_url:
            try:
                response = requests.post(url=self.cms_nbi_connect_object.cms_netconf_url, headers=headers, data=payload,
                                         timeout=http_timeout)
            except requests.exceptions.Timeout as e:

                raise e
        else:
            # will need to research how to implement https connection with request library
            pass

        if response.status_code != 200:
            # if the response code is not 200 FALSE and the request.response object is returned.
            return response

        else:
            resp_dict = xmltodict.parse(response.content)
            if pydash.objects.has(resp_dict, 'soapenv:Envelope.soapenv:Body.rpc-reply.data.top.object'):
                return resp_dict['soapenv:Envelope']['soapenv:Body']['rpc-reply']['data']['top']['object']
            else:
                return response

    def vlan(self, message_id='1', cms_user_nm='rootgod', network_nm='', http_timeout=1, vlan_id='', name='',
             igmp_mode='flood', vlanigmpprof_id='1', dhcp_mode='none', mac_force_forw='false', ip_src_verify='false',
             mac_learn='true', ae_ont_discovery='false', pon_tlan='false', pon_hairpin='false', igmp_pbit='pbit-4',
             dhcp_svc_profile={'dhcp-svc-prof': ''}, option82_enable='true', eth_opt82prof_id='2',
             gpon_opt82prof_id='1', mobility='false', pppoe_profile={'pppoe-prof': ''}):
        """
        Description
        -----------
        function vlan() performs a http/xml creation query for the provided network_nm(e7_node) requesting an <Vlan> object be created with the provided details

        Attributes
        ----------
        :param message_id: is the message_id used by the cms server to correlate http responses, if None is provided and self.cms_nbi_connect_object.message_id is None the default of 1 will be used
        :type message_id:str

        :param cms_user_nm: this parameter contains the username for the CMS USER ACCOUNT utilized in the interactions, this is described in pg.15 of Calix Management System (CMS) R15.x Northbound Interface API Guide
        :type cms_user_nm:str

        :param network_nm: this parameter contains the node name, which is made of the case-sensitive name of the E7 OS platform, preceded by NTWK-. Example: NTWK-Pet02E7. The nodename value can consist of alphanumeric, underscore, and space characters, this is described in pg.26 of Calix Management System (CMS) R15.x Northbound Interface API Guide
        :type network_nm:str

        :param http_timeout: this parameter is fed to the request.request() function as a timeout more can be read at the request library docs
        :type http_timeout:int

        :param vlan_id: Identifies the VLAN: 2 to 4093 (Except for 1002-1005 which are reserved for E7 operation.), excluding any reserved VLANs as described in pg.50 of Calix Management System (CMS) R15.x Northbound Interface API Guide
        :type vlan_id:str

        :param name:Identifies the name of the VLAN. Spaces and special characters are permitted. as described in pg.43 of Calix Management System (CMS) R15.x Northbound Interface API Guide
        :type name:str

        :param igmp_mode: Identifies the igmp_mode used by the e7 node to treat mcast traffic on the vlan, as described in pg.43 of Calix Management System (CMS) R15.x Northbound Interface API Guide
        :type igmp_mode:str

        :param vlanigmpprof_id: Numerical identifier for the local profile (1 to 20), The local IGMP profile ID can be viewed in the management interface. In the IGMP profile list, double-click a profile to view its ID above the Name field.  If <igmp-prof> is not specified, the systemdefault IGMP profile (1) is used.  this is described in pg.43 of Calix Management System (CMS) R15.x Northbound Interface API Guide
        :type vlanigmpprof_id:str

        :param dhcp_mode: this setting enables or disabled dhcp snooping on the vlan, as described in pg.43 of Calix Management System (CMS) R15.x Northbound Interface API Guide
        :type dhcp_mode:str

        :param mac_force_forw:this setting enables or disabled mac_force_forwarding on the vlan, as described in pg.43 of Calix Management System (CMS) R15.x Northbound Interface API Guide
        :type mac_force_forw:str

        :param ip_src_verify: enable or disables IP source verification (binding the IP and MAC addresses to the physical ONT Ethernet port), as described in pg.43 of Calix Management System (CMS) R15.x Northbound Interface API Guide
        :type ip_src_verify:str

        :param mac_learn: enables or disables mac-learning on the vlan, "Only applicable for E7-20 and E7-2 standalone systems; Modular Chassis configurations only support MAC learning", as described in pg.43 of Calix Management System (CMS) R15.x Northbound Interface API Guide
        :type mac_learn:str

        :param ae_ont_discovery: enables or disables ae-ont-discovery, (Only supported when DHCP snooping is enabled, as described in pg.43 of Calix Management System (CMS) R15.x Northbound Interface API Guide
        :type ae_ont_discovery:str

        :param pon_tlan: enables or disables pon-tlan perameter, as described in pg.43 of Calix Management System (CMS) R15.x Northbound Interface API Guide
        :type pon_tlan:str

        :param pon_hairpin:(Applicable for TLAN and T1/E3 PWE3 services) this allows for traffice to be hair-pin back to the same olt on a differing or same uni, this is explained better in pg.337 of Calix E-Series (E7 OS R2.5) Engineering and Planning Guide
        :type pon_hairpin:str

        :param igmp_pbit: The P-bit value(pbit-0 through pbit-7) for IGMP traffic that passes through the system, allowing the traffic type to be treated differently as it passes through the network. this is explained better in pg.337 of Calix E-Series (E7 OS R2.5) Engineering and Planning Guide
        :type igmp_pbit:str

        :param dhcp_svc_profile:Required for the configuration of DHCPv4 Proxy (Layer 3 DHCP Relay) on the client-side VLAN,The selected profile determines the DHCP Proxy Agent IP interface and IP address of the DHCP server(s). this is explained better in pg.337 of Calix E-Series (E7 OS R2.5) Engineering and Planning Guide
        :type dhcp_svc_profile:dict

        :param option82_enable:Enables or disables Option 82/LDRA at the VLAN level
        :type option82_enable:str

        :param eth_opt82prof_id:Access Identifier Profile for Ethernet/xDSL subscribers, specifying the Circuit and Remote ID format for Option 82 content insertion, this is explained better in pg.337 of Calix E-Series (E7 OS R2.5) Engineering and Planning Guide
        :type eth_opt82prof_id:str

        :param gpon_opt82prof_id:Access Identifier Profile for GPON subscribers, specifying the Circuit and Remote ID format for Option 82 content insertion, this is explained better in pg.337 of Calix E-Series (E7 OS R2.5) Engineering and Planning Guide
        :type gpon_opt82prof_id:str

        :param mobility:Enables or disables the ability for client devices to move freely between different ONTs on the same PON or card. (Not supported across multiple cards, this is explained better in pg.338 of Calix E-Series (E7 OS R2.5) Engineering and Planning Guide
        :type mobility:str

        :param pppoe_profile:Assign a previously-created PPPoE profile. When a PPPoE profile is selected, the DHCP features are disabled. Setting a VLAN PPPoE profile to “none” passes through all PPPoE traffic, transparently. If a PPPoE profile is used with PPPoE snoop, a list of all the active sessions and statistics are available, and the PPPoE stack is enabled, which passes through PPPoE traffic transparently as long as the Clients/BRAS are operating normally (illegal packets will be dropped),this is explained better in pg.338 of Calix E-Series (E7 OS R2.5) Engineering and Planning Guide
        :type pppoe_profile:dict

        :raise:
            ConnectTimeout: Will be raised if the http(s) connection timesout

        :return: vlan() function will return a dict on a successfull call, and a request.Models.Response object on a failed call
        """
        if isinstance(pppoe_profile['pppoe-prof'], dict):
            _pppoe_profile = xmltodict.unparse(pppoe_profile, full_document=False)
        else:
            _pppoe_profile = """<pppoe-prof></pppoe-prof>"""

        if isinstance(dhcp_svc_profile['dhcp-svc-prof'], dict):
            _dhcp_svc_prof_id = xmltodict.unparse(dhcp_svc_profile, full_document=False)
        else:
            _dhcp_svc_prof_id = """<dhcp-svc-prof></dhcp-svc-prof>"""

        payload = f"""<soapenv:Envelope xmlns:soapenv="http://www.w3.org/2003/05/soap-envelope">
                        <soapenv:Body>
                            <rpc message-id="{message_id}" nodename="{network_nm}" username="{cms_user_nm}" sessionid="{self.cms_nbi_connect_object.session_id}">
                                <edit-config>
                                    <target>
                                        <running/>
                                    </target>
                                    <config>
                                        <top>
                                            <object operation="create" get-config="true">
                                                <type>Vlan</type>
                                                <id>
                                                    <vlan>{vlan_id}</vlan>
                                                </id>
                                                <name>{name}</name>
                                                <igmp-mode>{igmp_mode}</igmp-mode>
                                                <igmp-prof>
                                                    <type>VlanIgmpProf</type>
                                                    <id>
                                                        <vlanigmpprof>{vlanigmpprof_id}</vlanigmpprof>
                                                    </id>
                                                </igmp-prof>
                                                <dhcp-mode>{dhcp_mode}</dhcp-mode>
                                                <mac-force-forw>{mac_force_forw}</mac-force-forw>
                                                <ip-src-verify>{ip_src_verify}</ip-src-verify>
                                                <mac-learn>{mac_learn}</mac-learn>
                                                <ae-ont-discovery>{ae_ont_discovery}</ae-ont-discovery>
                                                <pon-tlan>{pon_tlan}</pon-tlan>
                                                <pon-hairpin>{pon_hairpin}</pon-hairpin>
                                                <igmp-pbit>{igmp_pbit}</igmp-pbit>
                                                {_dhcp_svc_prof_id}
                                                <option82-enable>{option82_enable}</option82-enable>
                                                <eth-opt82prof>
                                                    <type>Opt82Prof</type>
                                                    <id>
                                                        <opt82prof>{eth_opt82prof_id}</opt82prof>
                                                    </id>
                                                </eth-opt82prof>
                                                <gpon-opt82prof>
                                                    <type>Opt82Prof</type>
                                                    <id>
                                                        <opt82prof>{gpon_opt82prof_id}</opt82prof>
                                                    </id>
                                                </gpon-opt82prof>
                                                <mobility>{mobility}</mobility>
                                                {_pppoe_profile}
                                            </object>
                                        </top>
                                    </config>
                                </edit-config>
                            </rpc>
                        </soapenv:Body>
                    </soapenv:Envelope>"""

        headers = {'Content-Type': 'text/xml;charset=ISO-8859-1',
                   'User-Agent': f'CMS_NBI_CONNECT-{cms_user_nm}'}

        if 'https' not in self.cms_nbi_connect_object.cms_netconf_url:
            try:
                response = requests.post(url=self.cms_nbi_connect_object.cms_netconf_url, headers=headers, data=payload,
                                         timeout=http_timeout)
            except requests.exceptions.Timeout as e:

                raise e
        else:
            # will need to research how to implement https connection with request library
            pass

        if response.status_code != 200:
            # if the response code is not 200 FALSE and the request.response object is returned.
            return response

        else:
            resp_dict = xmltodict.parse(response.content)
            if pydash.objects.has(resp_dict, 'soapenv:Envelope.soapenv:Body.rpc-reply.data.top.object'):
                return resp_dict['soapenv:Envelope']['soapenv:Body']['rpc-reply']['data']['top']['object']
            else:
                return response

    def vlan_members(self, message_id='1', cms_user_nm='rootgod', network_nm='', http_timeout=1, vlan_id='',
                     vlan_member_id='0', int_id={' ': ''}):
        """
        Description
        -----------
        function vlan_members() performs a http/xml creation query for the provided network_nm(e7_node) requesting an <VlanMem> object be created with the provided details

        Attributes
        ----------
        :param message_id: is the message_id used by the cms server to correlate http responses, if None is provided and self.cms_nbi_connect_object.message_id is None the default of 1 will be used
        :type message_id:str

        :param cms_user_nm: this parameter contains the username for the CMS USER ACCOUNT utilized in the interactions, this is described in pg.15 of Calix Management System (CMS) R15.x Northbound Interface API Guide
        :type cms_user_nm:str

        :param network_nm: this parameter contains the node name, which is made of the case-sensitive name of the E7 OS platform, preceded by NTWK-. Example: NTWK-Pet02E7. The nodename value can consist of alphanumeric, underscore, and space characters, this is described in pg.26 of Calix Management System (CMS) R15.x Northbound Interface API Guide
        :type network_nm:str

        :param http_timeout: this parameter is fed to the request.request() function as a timeout more can be read at the request library docs
        :type http_timeout:int

        :param vlan_id:  Identifies the VLAN: 2 to 4093 (Except for 1002-1005 which are reserved for E7 operation.), excluding any reserved VLANs as described in pg.50 of Calix Management System (CMS) R15.x Northbound Interface API Guide
        :type vlan_id:str

        :param vlan_member_id: —Identifies the VLAN member. Use one of the following: 0—The E7 auto-generates the VLAN member ID. 1 to 1000—Supply the VLAN member ID to use (must be unique). as described in pg.50 of Calix Management System (CMS) R15.x Northbound Interface API Guide
        :type vlan_member_id:str

        :param int_id: identifies the interface object being added to the vlan object, please review pg.50 of Calix Management System (CMS) R15.x Northbound Interface API Guide for more information
        :type int_id:dict

        :raise:
            ConnectTimeout: Will be raised if the http(s) connection timesout

        :return: vlan_members() will return a dict on a successfull query and a response.models.response object on a failed query

        Example
        -----------
        IMPORTANT NOTE

        You will need to submit the correct structured dictionary to the int_id param

        ------FOR ETHERNET INTERFACES------
        {
            'ethintf': {
                    'type': 'EthIntf',
                     'id': {
                         'shelf': '1',
                         'card': '1',
                         'ethintf': '1'}
                     }
         }
        Create_E7_Data.vlan_members(message_id='1',
                                    cms_user_nm=client.cms_nbi_config['cms_nodes']['example_node']['cms_creds']['user_nm'],
                                    network_nm='NTWK-Example_Name',
                                    vlan_member_id='0',
                                    int_id={'ethintf': {
                                                'type': 'EthIntf',
                                                 'id': {
                                                     'shelf': '1',
                                                     'card': '1',
                                                     'ethintf': '1'}
                                                 }
                                            })

        ------FOR ERPS/G8032 RINGS------
        {
            'eapsintf': {
                'type': 'EapsIntf',
                'id': {'eapsintf':'1'
                      }
            }
        }
        Create_E7_Data.vlan_members(message_id='1',
                                    cms_user_nm=client.cms_nbi_config['cms_nodes']['example_node']['cms_creds']['user_nm'],
                                    network_nm='NTWK-Example_Name',
                                    vlan_member_id='0',
                                    int_id={'eapsintf': {
                                                'type': 'EapsIntf',
                                                'id': {'eapsintf':'1'}
                                                        }
                                            })

        ------FOR LAG INTERFACES------
        {
            'lagintf': {
                    'type': 'LagIntf',
                     'id': {
                         'lagintf': '1'
                        }
                     }
        }
        Create_E7_Data.vlan_members(message_id='1',
                                    cms_user_nm=client.cms_nbi_config['cms_nodes']['example_node']['cms_creds']['user_nm'],
                                    network_nm='NTWK-Example_Name',
                                    vlan_member_id='0',
                                    int_id={'lagintf': {
                                                        'type': 'LagIntf',
                                                         'id': {'lagintf': '1'}
                                                         }
                                            })
        """

        if ' ' not in int_id.keys() and len(int_id.keys()) == 1:
            if 'ethintf' in int_id.keys():
                _int_id = xmltodict.unparse(int_id['ethintf'], full_document=False)
            elif 'lagintf' in int_id.keys():
                _int_id = xmltodict.unparse(int_id['lagintf'], full_document=False)
            elif 'eapsintf' in int_id.keys():
                _int_id = xmltodict.unparse(int_id['eapsintf'], full_document=False)
            else:
                raise AttributeError("int_id expects a object to add to the vlan_members please review and resubmit")
        else:
            raise AttributeError("int_id expects a object to add to the vlan_members please review and resubmit")

        payload = f"""<soapenv:Envelope xmlns:soapenv="http://www.w3.org/2003/05/soap-envelope">
                        <soapenv:Body>
                            <rpc message-id="{message_id}" nodename="{network_nm}" username="{cms_user_nm}" sessionid="{self.cms_nbi_connect_object.session_id}">
                                <edit-config>
                                    <target>
                                        <running/>
                                    </target>
                                    <config>
                                        <top>
                                            <object operation="create" get-config="true">
                                                <type>VlanMem</type>
                                                <id>
                                                    <vlan>{vlan_id}</vlan>
                                                    <vlanmem>{vlan_member_id}</vlanmem>
                                                </id>
                                                <member>
                                                    {_int_id}
                                                </member>
                                            </object>
                                        </top>
                                    </config>
                                </edit-config>
                            </rpc>
                        </soapenv:Body>
                    </soapenv:Envelope>"""

        headers = {'Content-Type': 'text/xml;charset=ISO-8859-1',
                   'User-Agent': f'CMS_NBI_CONNECT-{cms_user_nm}'}

        if 'https' not in self.cms_nbi_connect_object.cms_netconf_url:
            try:
                response = requests.post(url=self.cms_nbi_connect_object.cms_netconf_url, headers=headers, data=payload,
                                         timeout=http_timeout)
            except requests.exceptions.Timeout as e:

                raise e
        else:
            # will need to research how to implement https connection with request library
            pass

        if response.status_code != 200:
            # if the response code is not 200 FALSE and the request.response object is returned.
            return response

        else:
            resp_dict = xmltodict.parse(response.content)
            if pydash.objects.has(resp_dict, 'soapenv:Envelope.soapenv:Body.rpc-reply.data.top.object'):
                resp_dict = resp_dict['soapenv:Envelope']['soapenv:Body']['rpc-reply']['data']['top']['object']
                return resp_dict
            else:
                return response

    def ethsvc_ont(self, message_id='1', cms_user_nm='rootgod', network_nm='', http_timeout=1):
        """
        Description
        -----------
        function ethsvc_ont() performs a http/xml creation query for the provided network_nm(e7_node) requesting an <ethsvc> object be created with the provided details

        Attributes
        ----------
        :param message_id: is the message_id used by the cms server to correlate http responses, if None is provided and self.cms_nbi_connect_object.message_id is None the default of 1 will be used
        :type message_id:str

        :param cms_user_nm: this parameter contains the username for the CMS USER ACCOUNT utilized in the interactions, this is described in pg.15 of Calix Management System (CMS) R15.x Northbound Interface API Guide
        :type cms_user_nm:str

        :param network_nm: this parameter contains the node name, which is made of the case-sensitive name of the E7 OS platform, preceded by NTWK-. Example: NTWK-Pet02E7. The nodename value can consist of alphanumeric, underscore, and space characters, this is described in pg.26 of Calix Management System (CMS) R15.x Northbound Interface API Guide
        :type network_nm:str

        :param http_timeout: this parameter is fed to the request.request() function as a timeout more can be read at the request library docs
        :type http_timeout:int

        :return:
        """

