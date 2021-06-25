import json

INBOUND = 'INBOUND'
OUTBOUND = 'OUTBOUND'

PORT_PROBE = 'PORT_PROBE'
DNS_REQUEST = 'DNS_REQUEST'
AWS_API_CALL = 'AWS_API_CALL'
CONNECTION = 'NETWORK_CONNECTION'


class BaseAction:
    def __init__(self, data):
        self.remote_details = data['RemoteIpDetails']
        self.local_port_details = data['LocalPortDetails']
        self.organization = self.remote_details['Organization']


class Finding(object):

    def __init__(self, data):
        self.id = data['Id']
        self.type = data['Type']
        self.title = data['Title']
        self.severity = data['Severity']
        self.description = data['Description']
        self.service = self.Service(data['Service'])
        self.resource = self.Resource(data['Resource'])

    class Service:
        def __init__(self, data):
            self.count = data['Count']
            self.last_seen = data['EventLastSeen']
            self.first_seen = data['EventFirstSeen']
            self.name = data['ServiceName']
            self.action = self.Action(data['Action'])

        def attrs(self):
            data = self.action.data.organization
            data.update(self.action.data.local_port_details)
            data['ServiceName'] = self.name
            return data

        class Action:

            def __init__(self, data):
                self.type = data['ActionType']

                actions = {
                    DNS_REQUEST: lambda d: self.DNSRequest(d),
                    AWS_API_CALL: lambda d: self.AWSAPICall(d),
                    PORT_PROBE: lambda d: self.PortProbe(d),
                    CONNECTION: lambda d: self.Connection(d)
                }
                self.data = actions[self.type](data)

            class DNSRequest:
                def __init__(self, data):
                    self.__dict__ = \
                        json.loads(json.dumps(data['DnsRequestAction']))

            class AWSAPICall:
                def __init__(self, data):
                    self.__dict__ = \
                        json.loads(json.dumps(data['AwsApiCallAction']))

            class PortProbe(BaseAction):
                def __init__(self, data):
                    self.action = \
                        data['PortProbeAction']['PortProbeDetails'][0]
                    super().__init__(self.action)

            class Connection(BaseAction):
                def __init__(self, data):
                    self.action = data['NetworkConnectionAction']
                    self.local_details = self.action['LocalIpDetails']
                    self.directing = self.action['ConnectionDirection']
                    super().__init__(self.action)

                def direction(self):
                    local_ip = self.local_details['IpAddressV4']
                    remote_ip = self.remote_details['IpAddressV4']
                    directions = {
                        INBOUND: [remote_ip, local_ip],
                        OUTBOUND: [local_ip, remote_ip]
                    }
                    return directions[self.directing]

    class Resource:
        def __init__(self, data):
            self.type = data['ResourceType']
            self.details = self.Details(data['InstanceDetails'])

        class Details:
            def __init__(self, data):
                self.interfaces = [
                    self.Interface(obj) for obj in data['NetworkInterfaces']
                ]

            class Interface:
                def __init__(self, data):
                    self.__dict__ = json.loads(json.dumps(data))
