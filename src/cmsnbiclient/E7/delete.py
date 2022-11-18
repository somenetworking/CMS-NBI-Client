# IMPORT STATEMENTS
from cmsnbiclient import (requests, xmltodict, pydash, Client)
# IMPORT STATEMENTS


class Delete():

    def __init__(self, cms_nbi_connect_object):
        """
                Description
                -----------
                Class (Delete) is the delete query constructor/posting class for the E7 CMS NETCONF NBI

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

    def ont(self, message_id='1', cms_user_nm='rootgod', network_nm='', http_timeout=1, ont_id='', force='false'):
        """
        Description
        -----------
        function ont() performs a http/xml creation query for the provided network_nm(e7_node) requesting an <Ont> object be deleted with the provided details

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

        :param ont_id: Identifies the ONT by its E7 scope ID (1 to 64000000), as described in pg.129 of Calix Management System (CMS) R15.x Northbound Interface API Guide
        :type ont_id:str

        :param force: force expects a boolean string ['true', 'false'] Note: For a non-force(ie..force='false') delete to be successful, all service must be removed from the ONT. force="true"—Perform a force delete (deletes that all services on the ONT). as described in pg.47 of Calix Management System (CMS) R15.x Northbound Interface API Guide
        :type force:str

        :raise:
            AttributeError: will be raised if the ont_id is not a digit in the form of a str object
            ConnectTimeout: will be raised if http(s) connection times out

        :return: ont() returns a response.models.Response object on a failed call, and a nested dict on a successful call
        """
        if isinstance(ont_id, str):
            if ont_id.isdigit():
                pass
            else:
                raise AttributeError("""param:ont_id is expected to be a digit in the form of a str object""")
        else:
            raise AttributeError("""param:ont_id is expected to be a digit in the form of a str object""")

        payload = f"""<soapenv:Envelope xmlns:soapenv="http://www.w3.org/2003/05/soap-envelope">
                        <soapenv:Body>
                            <rpc message-id="{message_id}" nodename="{network_nm}" username="{cms_user_nm}" sessionid="{self.cms_nbi_connect_object.session_id}">
                                <edit-config>
                                    <target>
                                        <running/>
                                    </target>
                                    <config>
                                        <top>
                                            <object operation="delete" force="{force}">
                                                <type>Ont</type>
                                                <id>
                                                    <ont>{ont_id}</ont>
                                                </id>
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
            if pydash.objects.has(resp_dict, 'soapenv:Envelope.soapenv:Body.rpc-reply.ok'):
                return resp_dict['soapenv:Envelope']['soapenv:Body']['rpc-reply']
            else:
                return response

    def vlan(self, message_id='1', cms_user_nm='rootgod', network_nm='', http_timeout=1, vlan_id='', force='false'):
        """
        Description
        -----------
        function vlan() performs a http/xml Deletion query for the provided network_nm(e7_node) requesting an <Vlan> object be deleted with the provided details

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

        :param force: force expects a boolean string ['true', 'false'] Note: For a non-force(ie..force='false') delete to be successful, all membership must be removed from the vlan. force="true"—Perform a force delete (deletes that all memberships on the VLAN). as described in pg.47 of Calix Management System (CMS) R15.x Northbound Interface API Guide
        :type force:str

        :raise:
            AttributeError: will be raised if the vlan_id is not a digit in the form of a str object
            ConnectTimeout: Will be raised if the http(s) connection timesout

        :return: ont() returns a response.models.Response object on a failed call, and a nested dict on a successful call
        """
        if isinstance(vlan_id, str):
            if vlan_id.isdigit():
                pass
            else:
                raise AttributeError("""param:vlan_id is expected to be a digit in the form of a str object""")
        else:
            raise AttributeError("""param:vlan_id is expected to be a digit in the form of a str object""")

        payload = f"""<soapenv:Envelope xmlns:soapenv="http://www.w3.org/2003/05/soap-envelope">
                                <soapenv:Body>
                                    <rpc message-id="{message_id}" nodename="{network_nm}" username="{cms_user_nm}" sessionid="{self.cms_nbi_connect_object.session_id}">
                                        <edit-config>
                                            <target>
                                                <running/>
                                            </target>
                                            <config>
                                                <top>
                                                    <object operation="delete" force="{force}">
                                                        <type>Vlan</type>
                                                        <id>
                                                            <vlan>{vlan_id}</vlan>
                                                        </id>
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
            if pydash.objects.has(resp_dict, 'soapenv:Envelope.soapenv:Body.rpc-reply.ok'):
                return resp_dict['soapenv:Envelope']['soapenv:Body']['rpc-reply']
            else:
                return response

    def vlanmem(self, message_id='1', cms_user_nm='rootgod', network_nm='', http_timeout=1, vlan_id='',
                vlan_member_id='', force='false'):
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

        :param vlan_member_id: —Identifies the VLAN member. 1 to 1000 as described in pg.50 of Calix Management System (CMS) R15.x Northbound Interface API Guide
        :type vlan_member_id:str

        :raise:
            ConnectTimeout: Will be raised if the http(s) connection timesout

        :return: vlan_members() will return a dict on a successful query and a response.models.response object on a failed query

        Example
        -----------

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
                                            <object operation="delete" force="{force}">
                                                <type>VlanMem</type>
                                                <id>
                                                    <vlan>{vlan_id}</vlan>
                                                    <vlanmem>{vlan_member_id}</vlanmem>
                                                </id>
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
            if pydash.objects.has(resp_dict, 'soapenv:Envelope.soapenv:Body.rpc-reply.ok'):
                resp_dict = resp_dict['soapenv:Envelope']['soapenv:Body']['rpc-reply']
                return resp_dict
            else:
                return response

