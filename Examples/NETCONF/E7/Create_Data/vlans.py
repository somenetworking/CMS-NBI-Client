# IMPORT STATEMENT
from CMSNBIClient import CMS_NBI_Client
from CMSNBIClient import Create_E7_Data
# IMPORT STATEMENT

# Create the CMS_NBI_Client() instance
client = CMS_NBI_Client()

# Next step is to submit a login request to the CMS server, I will be using an example node
client.login_netconf(message_id='1',
                     cms_user_nm=client.cms_nbi_config['cms_nodes']['example_node']['cms_creds']['user_nm'],
                     cms_user_pass=client.cms_nbi_config['cms_nodes']['example_node']['cms_creds']['pass_wd'],
                     cms_node_ip=client.cms_nbi_config['cms_nodes']['example_node']['connection']['cms_node_ip'],
                     uri=client.cms_nbi_config['cms_netconf_uri']['e7'])
# if the login_netconf() function is successful a tuple with (True, '') is returned  else a response.Models.Response object is returned
# you can use the response library to debug the response.models.response object

# Next we create a Create_E7_Data instance and pass the CMS_NBI_Client instance to it
create_e7_data = Create_E7_Data(client)

# Once the Create_E7_Data object is created we can then call the vlan function and create a vlan with the provided parameters
#################################################################################################################
# CREATE DEFAULT VLAN PER DOCUMENTATION IN pg.335-338 Calix E-Series (E7 OS R2.5) Engineering and Planning Guide
create_e7_data.vlan(message_id='1',
                    cms_user_nm=client.cms_nbi_config['cms_nodes']['example_node']['cms_creds']['user_nm'],
                    network_nm='NTWK-Example_Name',
                    http_timeout=1,
                    vlan_id='15',
                    name='Example_VLAN')

# CREATE A TLAN USED FOR MEF E-Line,E-LAN, E-TREE circuits
create_e7_data.vlan(message_id='1',
                    cms_user_nm=client.cms_nbi_config['cms_nodes']['example_node']['cms_creds']['user_nm'],
                    network_nm='NTWK-Example_Name',
                    http_timeout=1,
                    vlan_id='15',
                    name='Example_TLAN',
                    pon_tlan='true')

# CREATE A VLAN USED FOR SERVING PPPOE TRAFFIC USING PPPOE_PROFILE WITH AN ID OF 1
create_e7_data.vlan(message_id='1',
                    cms_user_nm=client.cms_nbi_config['cms_nodes']['example_node']['cms_creds']['user_nm'],
                    network_nm='NTWK-Example_Name',
                    http_timeout=1,
                    vlan_id='15',
                    name='Example_PPPOE_VLAN',
                    pppoe_profile={'pppoe-prof': {'type': 'PppoeProf', 'id': {'pppoeprof': '1'}}})

# CREATE A VLAN USED FOR SERVING HSI DHCP SERVICES WITHOUT USING A DHCP_SERVICE
create_e7_data.vlan(message_id='1',
                    cms_user_nm=client.cms_nbi_config['cms_nodes']['example_node']['cms_creds']['user_nm'],
                    network_nm='NTWK-Example_Name',
                    http_timeout=1,
                    vlan_id='15',
                    name='Example_Basic_DHCP',
                    dhcp_mode='snoop')

# CREATE A VLAN USED FOR SERVING HSI DHCP SERVICES USING THE DHCP_SERVICE WITH A PROFILE ID OF 1
create_e7_data.vlan(message_id='1',
                    cms_user_nm=client.cms_nbi_config['cms_nodes']['example_node']['cms_creds']['user_nm'],
                    network_nm='NTWK-Example_Name',
                    http_timeout=1,
                    vlan_id='15',
                    name='Example_Complex_DHCP',
                    dhcp_mode='proxy',
                    dhcp_svc_profile={'dhcp-svc-prof': {'type': 'DhcpSvcProf', 'id': {'dhcpsvcprof': '1'}}})
