import json


class Network:
    def __init__(self, json_):
        self.direction = json_['ConnectionDirection']
        self.remote = self.Remote(json_)
        self.local = self.Local(json_)

    class Local:
        def __init__(self, json_):
            self.__dict__ = json.loads(json.dumps(json_['LocalIpDetails']))

    class Remote:
        def __init__(self, json_):
            self.__dict__ = json.loads(json.dumps(json_['RemoteIpDetails']))


class Finding(object):
    def __init__(self, json_):

        self.service = self.Service(json_['Service'])
        self.resource = self.Resource(json_['Resource'])
        self.severity = json_['Severity']
        self.title = json_['Title']
        self.type = json_['Type']
        self.description = json_['Description']

    class Service:
        def __init__(self, json_):
            self.action = self.Action(json_['Action'])
            self.first_seen = json_['EventFirstSeen']
            self.last_seen = json_['EventLastSeen']
            self.count = json_['Count']

        class Action:

            NETWORK_CONNECTION = 'NETWORK_CONNECTION'
            PORT_PROBE = 'PORT_PROBE'
            DNS_REQUEST = 'DNS_REQUEST'
            AWS_API_CALL = 'AWS_API_CALL'

            def __init__(self, json_):
                self.type = json_['ActionType']

                actions = {
                    self.DNS_REQUEST: lambda d: self.DNSRequest(d),
                    self.AWS_API_CALL: lambda d: self.AWSAPICall(d),
                    self.NETWORK_CONNECTION: lambda d: self.NetworkConnection(d),
                    self.PORT_PROBE: lambda d: self.PortProbe(d)
                }
                self.data = actions[self.type](json_)

            class DNSRequest:
                def __init__(self, json_):
                    self.__dict__ = json.loads(json.dumps(json_['DnsRequestAction']))

            class AWSAPICall:
                def __init__(self, json_):
                    self.__dict__ = json.loads(json.dumps(json_['AwsApiCallAction']))

            class PortProbe(Network):
                def __init__(self, json_):
                    super().__init__(json_['PortProbeAction']['PortProbeDetails'])

            class NetworkConnection(Network):
                def __init__(self, json_):
                    super().__init__(json_['NetworkConnectionAction'])

    class Resource:
        def __init__(self, json_):
            self.type = json_['ResourceType']
            self.details = self.InstanceDetails(json_['InstanceDetails'])

        class InstanceDetails:
            def __init__(self, json_):
                self.platform = json_['Platform']
                self.interfaces = [
                    self.NetworkInterface(interface) for interface in json_['NetworkInterfaces']
                ]

            class NetworkInterface:
                def __init__(self, json_):
                    self.__dict__ = json.loads(json.dumps(json_))
