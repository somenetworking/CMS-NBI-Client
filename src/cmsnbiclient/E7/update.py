# IMPORT STATEMENTS
from cmsnbiclient import (requests, xmltodict, pydash, Client)
# IMPORT STATEMENTS


class Update():

    def __init__(self, cms_nbi_connect_object):
        """
                Description
                -----------
                Class (Update) is the update/merge query constructor/posting class for the E7 CMS NETCONF NBI

                Attributes
                ----------
                :var self.cms_nbi_connect_object: accepts object created by the cms_nbi_client.client.Client()
                :type self.cms_nbi_connect_object: object
                """
        # Test if the provided object is of a CMS_NBI_Client instance

        if isinstance(cms_nbi_connect_object, Client):
            pass
        else:
            raise ValueError(f"""Query_E7_Data accepts a instance of CMS_NBI_Client, a instance of {type(cms_nbi_connect_object)}""")
        self.cms_nbi_connect_object = cms_nbi_connect_object
        # Test if the cms_netconf_url is a str object and contains the e7 uri
        if isinstance(self.cms_nbi_connect_object.cms_netconf_url, str):
            if self.cms_nbi_connect_object.cms_nbi_config['cms_netconf_uri']['e7'] in self.cms_nbi_connect_object.cms_netconf_url:
                pass
            else:
                raise ValueError(
                    f"""uri:{self.cms_nbi_connect_object.cms_nbi_config['cms_netconf_uri']['e7']} was not found in self.cms_nbi_connect_object.cms_netconf_url:{self.cms_nbi_connect_object.cms_netconf_url}""")
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

    def ont(self, message_id='1', cms_user_nm='rootgod', network_nm='', http_timeout=1, ont_id='', admin_state='', ont_sn='', reg_id='', sub_id='', ont_desc='', ontpwe3prof_id='', ontprof_id='', us_sdber_rate='', low_rx_opt_pwr_ne_thresh='', high_rx_opt_pwr_ne_thresh='', battery_present='', pse_max_power_budget='', poe_class_control='', replace_sn='0'):
        """
        Description
        -----------
        function ont() performs a http/xml Update query for the provided network_nm(e7_node) requesting an <Ont> object be updated with the provided details

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
            ConnectTimeout: Will be raised if the http(s) connection timesout
            ValueError: Will be raised if the ont_id is not an int str ie whole number

        :return: ont() returns a response.models.Response object on a failed call, and a nested dict on a successful call

        Example
        ______

        Next we create an Update instance and pass the cms_nbi_client.Client() instance to it
        update_e7_data = Update(client)
        Once the Update_E7_Data object is created we can then call the ont() function and update ont variables for a specific ont
        For any updated query an ont_id must be provided in the ont_id var
        Only the var being updated needs to be supplied

        Updating the ont 1 admin_state>>disabled
        update_e7_data.ont(cms_user_nm=client.cms_nbi_config['cms_nodes']['example_node']['cms_creds']['user_nm'],
                           network_nm='NTWK-Example_Network',
                           ont_id='1',
                           admin_state='disabled')

        Updating the ont 2 Subscriber Id  && Description
        update_e7_data.ont(cms_user_nm=client.cms_nbi_config['cms_nodes']['example_node']['cms_creds']['user_nm'],
                           network_nm='NTWK-Example_Network',
                           ont_id='2',
                           sub_id='9999999',
                           ont_desc='example_ont')

        Updating ont 4 to False on the battery_present
        update_e7_data.ont(cms_user_nm=client.cms_nbi_config['cms_nodes']['example_node']['cms_creds']['user_nm'],
                           network_nm='NTWK-Example_Network',
                           ont_id='4',
                           battery_present='false')

        Replace an ONT with a new ont
        this requires two calls one to unlink the cxnk and another to link a new cxnk
        update_e7_data.ont(cms_user_nm=client.cms_nbi_config['cms_nodes']['example_node']['cms_creds']['user_nm'],
                           network_nm='NTWK-Example_Network',
                           ont_id='4',
                           ont_sn='0',
                           replace_sn='1')

        update_e7_data.ont(cms_user_nm=client.cms_nbi_config['cms_nodes']['example_node']['cms_creds']['user_nm'],
                           network_nm='NTWK-Example_Network',
                           ont_id='4',
                           ont_sn='9999')
        """
        # Since i dont know how to filter parameters that are empty this is what im doing , hopefully it works
        # using change_var_list as a tmp list to filter out any ont vars that are not being changed, ie the empty vars will be removed from the dictionary
        # before using xmltodict.unparse to convert it to an xml str
        par_inputs = vars()
        if isinstance(par_inputs['ont_id'], str):
            if par_inputs['ont_id'].isdigit and not par_inputs['ont_id'] == '0':
                pass
            else:
                raise ValueError(f"""{par_inputs['ont_id']} NEEDS TO BE A INT STR 1..2..3..ie""")

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

        change_var = dict([(vkey, vdata) for vkey, vdata in change_var.items() if(vdata)])
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
                            <rpc message-id="{message_id}" nodename="{network_nm}" username="{cms_user_nm}" sessionid="{self.cms_nbi_connect_object.session_id}">
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