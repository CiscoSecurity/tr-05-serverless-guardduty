import json

INBOUND = 'INBOUND'
OUTBOUND = 'OUTBOUND'


class Network:

    def __init__(self, data):
        self.local = self.Local(data)
        self.remote = self.Remote(data)
        self.direction = self.direction(data['ConnectionDirection'])

    def direction(self, type_):
        directing = {
            INBOUND: [self.remote, self.local],
            OUTBOUND: [self.local, self.remote]
        }
        return directing[type_]

    class Local:
        def __init__(self, data):
            self.__dict__ = json.loads(json.dumps(data['LocalIpDetails']))

    class Remote:
        def __init__(self, data):
            self.__dict__ = json.loads(json.dumps(data['RemoteIpDetails']))


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
            self.action = self.Action(data['Action'])

        class Action:

            PORT_PROBE = 'PORT_PROBE'
            DNS_REQUEST = 'DNS_REQUEST'
            AWS_API_CALL = 'AWS_API_CALL'
            CONNECTION = 'NETWORK_CONNECTION'

            def __init__(self, data):
                self.type = data['ActionType']

                actions = {
                    self.DNS_REQUEST: lambda d: self.DNSRequest(d),
                    self.AWS_API_CALL: lambda d: self.AWSAPICall(d),
                    self.PORT_PROBE: lambda d: self.PortProbe(d),
                    self.CONNECTION: lambda d: self.Connection(d)
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

            class PortProbe:
                def __init__(self, data):
                    self.details = data['PortProbeAction']['PortProbeDetails']

            class Connection(Network):
                def __init__(self, data):
                    super().__init__(data['NetworkConnectionAction'])

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
