import datetime


AFFECTED_INSTANCES_TILE = {
    "default_period": "last_7_days",
    "description": ("Affected Instances tile shows what"
                    " types of findings EC2 instances have."),
    "id": "affected_instances",
    "periods": [
        "last_24_hours",
        "last_7_days",
        "last_30_days"
    ],
    "short_description": ("Affected Instances by finding "
                          "types for given time period."),
    "tags": [
        "affected_instances"
    ],
    "title": "Affected Instances",
    "type": "donut_graph"
}

EVENTS_PER_DAY_TILE = {
    "default_period": "last_7_days",
    "description": "Events grouped by severity per day "
                   "tile shows quantity of events per "
                   "day for the given period of time.",
    "id": "events_per_day",
    "periods": ["last_7_days", "last_30_days"],
    "short_description": "Events grouped by severity per "
                         "day for given time period.",
    "tags": ["events_per_day"],
    "title": "Events grouped by severity per day",
    "type": "vertical_bar_chart"
}

TOP_TEN_FINDINGS_TILE = {
    "default_period": "last_7_days",
    "description": "Top 10 Findings by count tile provides a list of "
                   "the top 10 findings by count.",
    "id": "top_ten_findings",
    "periods": [
        "last_24_hours",
        "last_7_days",
        "last_30_days",
        "last_60_days",
        "last_90_days"
    ],
    "short_description": "Top 10 Findings by count tile provides a list "
                         "of the top 10 findings by count.",
    "tags": ["top_ten_findings"],
    "title": "Top 10 Findings by count",
    "type": "markdown"
}

TOTAL_EVENTS_TILE = {
    "default_period": "last_7_days",
    "description": ("Total Events tile provides the total number of "
                    "findings grouped by resource type."),
    "id": "total_events",
    "periods": ["last_24_hours",
                "last_7_days",
                "last_30_days",
                "last_60_days",
                "last_90_days"],
    "short_description": ("Total Events tile provides the total number "
                          "of findings grouped by resource type."),
    "tags": ["total_events"],
    "title": "Total Events",
    "type": "metric_group"
}

PORT_PROBE_COUNTRIES_TILE = {
    "default_period": "last_7_days",
    "description": ("Port Probe Source Countries tile visualizes the "
                    "countries where port probes are issued from."),
    "id": "port_probe_source_countries",
    "periods": [
        "last_24_hours",
        "last_7_days",
        "last_30_days",
        "last_60_days",
        "last_90_days"
    ],
    "short_description": ("Port Probe Source Countries tile "
                          "visualizes the countries where port probes "
                          "are issued from."),
    "tags": [
        "port_probe_source_countries"
    ],
    "title": "Port Probe Source Countries",
    "type": "threat_map"
}


OBSERVE_RESPONSE = {
    "data": {
        "indicators": {
            "count": 2,
            "docs": [
                {
                    "confidence": "High",
                    "description": "EC2 instance i-99999999 is "
                                   "querying a domain name of a "
                                   "remote host that is a "
                                   "known source "
                                   "of Drive-By download attacks.",
                    "external_ids": [
                        "aws-guard-duty-indicator-31b81b20c7d6b9d"
                        "add40c06eb8bf1ad079c7e4f96d2be00660f6da9"
                        "b82421335"
                    ],
                    "id": "transient:aws-guard-duty-indicator-"
                          "f001da94620f4d2e8f0fe6d29629e618",
                    "producer": "network.ips",
                    "schema_version": "1.0.17",
                    "severity": "High",
                    "short_description": "EC2 instance i-99999999 "
                                         "is querying a domain "
                                         "name of a remote host that "
                                         "is a known "
                                         "source of Drive-By "
                                         "download attacks.",
                    "source": "Amazon GuardDuty findings",
                    "source_uri": "https://console.aws.amazon.com"
                                  "/guardduty/home?region/"
                                  "findings&region=region"
                                  "#/findings?macros"
                                  "=all&fId=0ebd952561ab2299"
                                  "30385cfe43860cbf&search=id"
                                  "%3D0ebd952561ab229930385c"
                                  "fe43860cbf",
                    "timestamp": "2021-08-09T09:42:27.000Z",
                    "type": "indicator",
                    "valid_time": {
                        "end_time": "2525-01-01T00:00:00.000Z",
                        "start_time": "2021-08-09T09:42:27.000Z"
                    }
                },
                {
                    "confidence": "High",
                    "description": "EC2 instance i-99999999 is "
                                   "querying a domain name "
                                   "associated with a known "
                                   "Command & Control "
                                   "server.",
                    "external_ids": [
                        "aws-guard-duty-indicator-"
                        "31b81b20c7d6b9dadd40c06eb8bf1ad079c7"
                        "e4f96d2be00660f6da9b82421335"
                    ],
                    "id": "transient:aws-guard-duty-"
                          "indicator-88c24095ae564d57"
                          "95cc3f08992e5898",
                    "producer": "network.ips",
                    "schema_version": "1.0.17",
                    "severity": "High",
                    "short_description": "EC2 instance i-99999999 "
                                         "is querying a domain "
                                         "name associated with a "
                                         "known Command & "
                                         "Control server.",
                    "source": "Amazon GuardDuty findings",
                    "source_uri": "https://console.aws.amazon.com/"
                                  "guardduty/home?region/findings&"
                                  "region=region"
                                  "#/findings?macros"
                                  "=all&fId=14bd952561ab40e0b927"
                                  "5f648fcca0f2&search=id"
                                  "%3D14bd952561ab40e0b9275f648fcca0f2",
                    "timestamp": "2021-08-09T09:42:27.000Z",
                    "type": "indicator",
                    "valid_time": {
                        "end_time": "2525-01-01T00:00:00.000Z",
                        "start_time": "2021-08-09T09:42:27.000Z"
                    }
                }
            ]
        },
        "relationships": {
            "count": 2,
            "docs": [
                {
                    "external_ids": [
                        "aws-guard-duty-relationship-"
                        "198e4e9957b34070f57e69942dd2"
                        "c751c72e5dfd41e7ab2ac47f4b26766d7a69"
                    ],
                    "id": "transient:aws-guard-duty-relationship"
                          "-08c0d67d19e5483998953246c094fe0d",
                    "relationship_type": "sighting-of",
                    "schema_version": "1.0.17",
                    "source": "Amazon GuardDuty findings",
                    "source_ref": "transient:aws-guard-duty-"
                                  "sighting-099065c8932f41e2908"
                                  "3ed7a742cb644",
                    "source_uri": "https://console.aws.amazon.com/"
                                  "guardduty/home?region/"
                                  "findings&region=region"
                                  "#/findings?macros"
                                  "=all&fId=0ebd952561ab22993038"
                                  "5cfe43860cbf&search=id"
                                  "%3D0ebd952561ab229930385cfe"
                                  "43860cbf",
                    "target_ref": "transient:aws-guard-duty-"
                                  "indicator-f001da94620f4d2e8f0"
                                  "fe6d29629e618",
                    "type": "relationship"
                },
                {
                    "external_ids": [
                        "aws-guard-duty-relationship-"
                        "198e4e9957b34070f57e69942dd2"
                        "c751c72e5dfd41e7ab2ac47f4b26766d7a69"
                    ],
                    "id": "transient:aws-guard-duty-relationship"
                          "-10774be950d74376bc1bd90a98e89d21",
                    "relationship_type": "sighting-of",
                    "schema_version": "1.0.17",
                    "source": "Amazon GuardDuty findings",
                    "source_ref": "transient:aws-guard-duty-"
                                  "sighting-bc0af638cea2466cb"
                                  "74e34d4dcd3fc4b",
                    "source_uri": "https://console.aws.amazon.com/"
                                  "guardduty/home?region/findings"
                                  "&region=region"
                                  "#/findings?macros"
                                  "=all&fId=14bd952561ab40e0b92"
                                  "75f648fcca0f2&search=id"
                                  "%3D14bd952561ab40e0b9275f648f"
                                  "cca0f2",
                    "target_ref": "transient:aws-guard-duty-"
                                  "indicator-88c24095ae564d5795"
                                  "cc3f08992e5898",
                    "type": "relationship"
                }
            ]
        },
        "sightings": {
            "count": 2,
            "docs": [
                {
                    "confidence": "High",
                    "count": 3,
                    "description": "EC2 instance i-99999999 is "
                                   "querying a domain name of "
                                   "a remote host that is a "
                                   "known source "
                                   "of Drive-By download attacks.",
                    "external_ids": [
                        "aws-guard-duty-sighting-7a830ab68800aff"
                        "6a15e61294b41a4e07d177c495f49ee808d232"
                        "e719e5a34bd"
                    ],
                    "id": "transient:aws-guard-duty-sighting-"
                          "099065c8932f41e29083ed7a742cb644",
                    "internal": True,
                    "observables": [
                        {
                            "type": "ip",
                            "value": "10.0.0.1"
                        }
                    ],
                    "observed_time": {
                        "end_time": "2021-09-20T14:24:35.000Z",
                        "start_time": "2021-08-09T09:42:27.000Z"
                    },
                    "relations": [],
                    "schema_version": "1.0.17",
                    "sensor": "network.ips",
                    "severity": "High",
                    "source": "Amazon GuardDuty findings",
                    "source_uri": "https://console.aws.amazon.com/"
                                  "guardduty/home?region/findings"
                                  "&region=region"
                                  "#/findings?macros=all&fId="
                                  "0ebd952561ab229930385cfe43860cb"
                                  "f&search=id"
                                  "%3D0ebd952561ab229930385cfe43"
                                  "860cbf",
                    "targets": [
                        {
                            "observables": [
                                {
                                    "type": "ip",
                                    "value": "198.51.100.0"
                                },
                                {
                                    "type": "ip",
                                    "value": "10.0.0.1"
                                },
                                {
                                    "type": "domain",
                                    "value": "GeneratedFindingPu"
                                             "blicDNSName"
                                }
                            ],
                            "observed_time": {
                                "end_time": "2021-09-20T14:24:35.000Z",
                                "start_time": "2021-08-09T09:42:27.000Z"
                            },
                            "type": "network.ips"
                        }
                    ],
                    "timestamp": "2021-09-20T14:24:35.000Z",
                    "title": "Drive-by source domain name queried "
                             "by EC2 instance i-99999999.",
                    "type": "sighting"
                },
                {
                    "confidence": "High",
                    "count": 3,
                    "description": "EC2 instance i-99999999 is "
                                   "querying a domain name "
                                   "associated with a known "
                                   "Command & Control "
                                   "server.",
                    "external_ids": [
                        "aws-guard-duty-sighting-0732a5b0377c7e"
                        "48d57e23f71c193220902192eb21c7d52159"
                        "fd819c9c4dc228"
                    ],
                    "id": "transient:aws-guard-duty-sighting-"
                          "bc0af638cea2466cb74e34d4dcd3fc4b",
                    "internal": True,
                    "observables": [
                        {
                            "type": "ip",
                            "value": "10.0.0.1"
                        }
                    ],
                    "observed_time": {
                        "end_time": "2021-09-20T14:24:35.000Z",
                        "start_time": "2021-08-09T09:42:27.000Z"
                    },
                    "relations": [],
                    "schema_version": "1.0.17",
                    "sensor": "network.ips",
                    "severity": "High",
                    "source": "Amazon GuardDuty findings",
                    "source_uri": "https://console.aws.amazon.com/"
                                  "guardduty/home?region/findings"
                                  "&region=region"
                                  "#/findings?macros=all&fId="
                                  "14bd952561ab40e0b9275f648"
                                  "fcca0f2&search=id"
                                  "%3D14bd952561ab40e0b9275f"
                                  "648fcca0f2",
                    "targets": [
                        {
                            "observables": [
                                {
                                    "type": "ip",
                                    "value": "198.51.100.0"
                                },
                                {
                                    "type": "ip",
                                    "value": "10.0.0.1"
                                },
                                {
                                    "type": "domain",
                                    "value": "GeneratedFind"
                                             "ingPublicDNSName"
                                }
                            ],
                            "observed_time": {
                                "end_time": "2021-09-20T14:24:35.000Z",
                                "start_time": "2021-08-09T09:42:27.000Z"
                            },
                            "type": "network.ips"
                        }
                    ],
                    "timestamp": "2021-09-20T14:24:35.000Z",
                    "title": "Command and Control server domain "
                             "name queried by EC2 instance i-99999999.",
                    "type": "sighting"
                }
            ]
        }
    }
}

REFER_RESPONSE = {
    "data": [
        {
            "categories": [
                "Search",
                "Amazon Detective"
            ],
            "description": "Check this IP with Amazon Detective",
            "id": "ref-aws-detective-search-ip-10.0.0.1",
            "title": "Search for this IP",
            "url": "https://region.console.aws.amazon.com/"
                   "detective/home?region=region#entities/IpAddress/10.0.0.1"
        }
    ]
}

OBSERVED_TIME = {
    "end_time": "2021-09-28T19:07:58",
    "start_time": "2021-09-21T16:07:58"
}

DATE_LIST = [
    datetime.date(2021, 9, 28),
    datetime.date(2021, 9, 27),
    datetime.date(2021, 9, 26),
    datetime.date(2021, 9, 25),
    datetime.date(2021, 9, 24),
    datetime.date(2021, 9, 23),
    datetime.date(2021, 9, 22)
]

INSTANCE_SOURCE_FINDINGS = [
    {
        "AccountId": "id",
        "Arn": "arn:aws:guardduty:us-east-2:id:detector/"
               "detector_id/finding/"
               "0ebd952561ab229930385cfe43860cbf",
        "CreatedAt": "2021-08-09T09:42:27.926Z",
        "Description": "EC2 instance i-99999999 is querying "
                       "a domain name of a "
                       "remote host that is a known source "
                       "of Drive-By download attacks.",
        "Id": "0ebd952561ab229930385cfe43860cbf",
        "Partition": "aws",
        "Region": "us-east-2",
        "Resource": {
            "InstanceDetails": {
                "AvailabilityZone": "GeneratedFinding"
                                    "InstaceAvailabilityZone",
                "IamInstanceProfile": {
                    "Arn": "arn:aws:iam::id:example/instance/profile",
                    "Id": "GeneratedFindingInstanceProfileId"
                },
                "ImageDescription": "GeneratedFinding"
                                    "InstaceImageDescription",
                "ImageId": "ami-99999999",
                "InstanceId": "i-99999999",
                "InstanceState": "running",
                "InstanceType": "m3.xlarge",
                "OutpostArn": "arn:aws:outposts:us-west-2:id:"
                              "outpost/op-0fbc006e9abbc73c3",
                "LaunchTime": "2016-07-16T15:55:03.000Z",
                "NetworkInterfaces": [
                    {
                        "Ipv6Addresses": [],
                        "NetworkInterfaceId": "eni-bfcffe88",
                        "PrivateDnsName": "GeneratedFindingPrivateDnsName",
                        "PrivateIpAddress": "10.0.0.1",
                        "PrivateIpAddresses": [
                            {
                                "PrivateDnsName": "Generated"
                                                  "FindingPrivateName",
                                "PrivateIpAddress": "10.0.0.1"
                            }
                        ],
                        "PublicDnsName": "GeneratedFindingPublicDNSName",
                        "PublicIp": "198.51.100.0",
                        "SecurityGroups": [
                            {
                                "GroupId": "GeneratedFindingSecurityId",
                                "GroupName": "GeneratedFinding"
                                             "SecurityGroupName"
                            }
                        ],
                        "SubnetId": "GeneratedFindingSubnetId",
                        "VpcId": "GeneratedFindingVPCId"
                    }
                ],
                "ProductCodes": [
                    {}
                ],
                "Tags": [
                    {
                        "Key": "GeneratedFindingInstaceTag1",
                        "Value": "GeneratedFindingInstaceValue1"
                    },
                    {
                        "Key": "GeneratedFindingInstaceTag2",
                        "Value": "GeneratedFindingInstaceTagValue2"
                    },
                    {
                        "Key": "GeneratedFindingInstaceTag3",
                        "Value": "GeneratedFindingInstaceTagValue3"
                    },
                    {
                        "Key": "GeneratedFindingInstaceTag4",
                        "Value": "GeneratedFindingInstaceTagValue4"
                    },
                    {
                        "Key": "GeneratedFindingInstaceTag5",
                        "Value": "GeneratedFindingInstaceTagValue5"
                    },
                    {
                        "Key": "GeneratedFindingInstaceTag6",
                        "Value": "GeneratedFindingInstaceTagValue6"
                    },
                    {
                        "Key": "GeneratedFindingInstaceTag7",
                        "Value": "GeneratedFindingInstaceTagValue7"
                    },
                    {
                        "Key": "GeneratedFindingInstaceTag8",
                        "Value": "GeneratedFindingInstaceTagValue8"
                    },
                    {
                        "Key": "GeneratedFindingInstaceTag9",
                        "Value": "GeneratedFindingInstaceTagValue9"
                    }
                ]
            },
            "ResourceType": "Instance"
        },
        "SchemaVersion": "2.0",
        "Service": {
            "Action": {
                "ActionType": "DNS_REQUEST",
                "DnsRequestAction": {
                    "Domain": "GeneratedFindingDomainName"
                }
            },
            "Evidence": {
                "ThreatIntelligenceDetails": [
                    {
                        "ThreatListName": "GeneratedFindingThreatListName",
                        "ThreatNames": [
                            "GeneratedFindingThreatName"
                        ]
                    }
                ]
            },
            "Archived": False,
            "Count": 3,
            "DetectorId": "detector_id",
            "EventFirstSeen": "2021-08-09T09:42:27.000Z",
            "EventLastSeen": "2021-09-20T14:24:35.000Z",
            "ResourceRole": "TARGET",
            "ServiceName": "guardduty"
        },
        "Severity": 8,
        "Title": "Drive-by source domain "
                 "name queried by EC2 instance i-99999999.",
        "Type": "Trojan:EC2/DriveBySourceTraffic!DNS",
        "UpdatedAt": "2021-09-23T14:24:35.130Z"
    },
    {
        "AccountId": "id",
        "Arn": "arn:aws:guardduty:us-east-2:id:detector/"
               "detector_id/finding/14bd952561ab40e0b9275f648fcca0f2",
        "CreatedAt": "2021-08-09T09:42:27.926Z",
        "Description": "EC2 instance i-99999999 is querying a domain "
                       "name associated with a "
                       "known Command & Control server.",
        "Id": "14bd952561ab40e0b9275f648fcca0f2",
        "Partition": "aws",
        "Region": "us-east-2",
        "Resource": {
            "InstanceDetails": {
                "AvailabilityZone": "GeneratedFinding"
                                    "InstaceAvailabilityZone",
                "IamInstanceProfile": {
                    "Arn": "arn:aws:iam::id:example/instance/profile",
                    "Id": "GeneratedFindingInstanceProfileId"
                },
                "ImageDescription": "GeneratedFinding"
                                    "InstaceImageDescription",
                "ImageId": "ami-99999999",
                "InstanceId": "i-99999999",
                "InstanceState": "running",
                "InstanceType": "c3.large",
                "OutpostArn": "arn:aws:outposts:us-west-2:id"
                              ":outpost/op-0fbc006e9abbc73c3",
                "LaunchTime": "2017-12-19T01:37:35.000Z",
                "NetworkInterfaces": [
                    {
                        "Ipv6Addresses": [],
                        "NetworkInterfaceId": "eni-bfcffe88",
                        "PrivateDnsName": "GeneratedFindingPrivateDnsName",
                        "PrivateIpAddress": "10.0.0.1",
                        "PrivateIpAddresses": [
                            {
                                "PrivateDnsName": "Generated"
                                                  "FindingPrivateName",
                                "PrivateIpAddress": "10.0.0.1"
                            }
                        ],
                        "PublicDnsName": "GeneratedFindingPublicDNSName",
                        "PublicIp": "198.51.100.0",
                        "SecurityGroups": [
                            {
                                "GroupId": "Generated"
                                           "FindingSecurityId",
                                "GroupName": "GeneratedFinding"
                                             "SecurityGroupName"
                            }
                        ],
                        "SubnetId": "GeneratedFindingSubnetId",
                        "VpcId": "GeneratedFindingVPCId"
                    }
                ],
                "ProductCodes": [
                    {}
                ],
                "Tags": [
                    {
                        "Key": "GeneratedFindingInstaceTag1",
                        "Value": "GeneratedFindingInstaceValue1"
                    },
                    {
                        "Key": "GeneratedFindingInstaceTag2",
                        "Value": "GeneratedFindingInstaceTagValue2"
                    },
                    {
                        "Key": "GeneratedFindingInstaceTag3",
                        "Value": "GeneratedFindingInstaceTagValue3"
                    },
                    {
                        "Key": "GeneratedFindingInstaceTag4",
                        "Value": "GeneratedFindingInstaceTagValue4"
                    },
                    {
                        "Key": "GeneratedFindingInstaceTag5",
                        "Value": "GeneratedFindingInstaceTagValue5"
                    },
                    {
                        "Key": "GeneratedFindingInstaceTag6",
                        "Value": "GeneratedFindingInstaceTagValue6"
                    },
                    {
                        "Key": "GeneratedFindingInstaceTag7",
                        "Value": "GeneratedFindingInstaceTagValue7"
                    },
                    {
                        "Key": "GeneratedFindingInstaceTag8",
                        "Value": "GeneratedFindingInstaceTagValue8"
                    },
                    {
                        "Key": "GeneratedFindingInstaceTag9",
                        "Value": "GeneratedFindingInstaceTagValue9"
                    }
                ]
            },
            "ResourceType": "Instance"
        },
        "SchemaVersion": "2.0",
        "Service": {
            "Action": {
                "ActionType": "DNS_REQUEST",
                "DnsRequestAction": {
                    "Domain": "GeneratedFindingDomainName"
                }
            },
            "Evidence": {
                "ThreatIntelligenceDetails": [
                    {
                        "ThreatListName": "GeneratedFindingThreatListName",
                        "ThreatNames": [
                            "GeneratedFindingThreatName"
                        ]
                    }
                ]
            },
            "Archived": False,
            "Count": 3,
            "DetectorId": "detector_id",
            "EventFirstSeen": "2021-08-09T09:42:27.000Z",
            "EventLastSeen": "2021-09-20T14:24:35.000Z",
            "ResourceRole": "TARGET",
            "ServiceName": "guardduty"
        },
        "Severity": 8,
        "Title": "Command and Control server domain "
                 "name queried by EC2 instance i-99999999.",
        "Type": "Backdoor:EC2/C&CActivity.B!DNS",
        "UpdatedAt": "2021-09-22T14:24:35.130Z"
    }
]

PORT_PROBE_FINDINGS = [
    {
        "AccountId": "id",
        "Arn": "arn:aws:guardduty:us-east-2:id:"
               "detector/detector/"
               "finding/58bd952561ad49467584fc08061c41eb",
        "CreatedAt": "2021-08-09T09:42:27.930Z",
        "Description": "EC2 instance has an unprotected "
                       "EMR-related port which is being probed "
                       "by a known malicious host.",
        "Id": "58bd952561ad49467584fc08061c41eb",
        "Partition": "aws",
        "Region": "us-east-2",
        "Resource": {
            "InstanceDetails": {
                "AvailabilityZone": "GeneratedFindingInstace"
                                    "AvailabilityZone",
                "IamInstanceProfile": {
                    "Arn": "arn:aws:iam::id:example/"
                           "instance/profile",
                    "Id": "GeneratedFindingInstanceProfileId"
                },
                "ImageDescription": "GeneratedFindingInstace"
                                    "ImageDescription",
                "ImageId": "ami-99999999",
                "InstanceId": "i-99999999",
                "InstanceState": "running",
                "InstanceType": "m3.xlarge",
                "OutpostArn": "arn:aws:outposts:us-west-2:"
                              "id:outpost/op-0fbc006e9abbc73c3",
                "LaunchTime": "2016-08-02T02:05:06.000Z",
                "NetworkInterfaces": [
                    {
                        "Ipv6Addresses": [],
                        "NetworkInterfaceId": "eni-bfcffe88",
                        "PrivateDnsName": "GeneratedFindingPrivateDnsName",
                        "PrivateIpAddress": "10.0.0.1",
                        "PrivateIpAddresses": [
                            {
                                "PrivateDnsName": "GeneratedFinding"
                                                  "PrivateName",
                                "PrivateIpAddress": "10.0.0.1"
                            }
                        ],
                        "PublicDnsName": "GeneratedFindingPublicDNSName",
                        "PublicIp": "198.51.100.0",
                        "SecurityGroups": [
                            {
                                "GroupId": "GeneratedFindingSecurityId",
                                "GroupName": "Generated"
                                             "FindingSecurityGroupName"
                            }
                        ],
                        "SubnetId": "GeneratedFindingSubnetId",
                        "VpcId": "GeneratedFindingVPCId"
                    }
                ],
                "ProductCodes": [
                    {}
                ],
                "Tags": [
                    {
                        "Key": "GeneratedFindingInstaceTag1",
                        "Value": "GeneratedFindingInstaceValue1"
                    },
                    {
                        "Key": "GeneratedFindingInstaceTag2",
                        "Value": "GeneratedFindingInstaceTagValue2"
                    },
                    {
                        "Key": "GeneratedFindingInstaceTag3",
                        "Value": "GeneratedFindingInstaceTagValue3"
                    },
                    {
                        "Key": "GeneratedFindingInstaceTag4",
                        "Value": "GeneratedFindingInstaceTagValue4"
                    },
                    {
                        "Key": "GeneratedFindingInstaceTag5",
                        "Value": "GeneratedFindingInstaceTagValue5"
                    },
                    {
                        "Key": "GeneratedFindingInstaceTag6",
                        "Value": "GeneratedFindingInstaceTagValue6"
                    },
                    {
                        "Key": "GeneratedFindingInstaceTag7",
                        "Value": "GeneratedFindingInstaceTagValue7"
                    },
                    {
                        "Key": "GeneratedFindingInstaceTag8",
                        "Value": "GeneratedFindingInstaceTagValue8"
                    },
                    {
                        "Key": "GeneratedFindingInstaceTag9",
                        "Value": "GeneratedFindingInstaceTagValue9"
                    }
                ]
            },
            "ResourceType": "Instance"
        },
        "SchemaVersion": "2.0",
        "Service": {
            "Action": {
                "ActionType": "PORT_PROBE",
                "PortProbeAction": {
                    "Blocked": False,
                    "PortProbeDetails": [
                        {
                            "LocalPortDetails": {
                                "Port": 22,
                                "PortName": "SSH"
                            },
                            "LocalIpDetails": {
                                "IpAddressV4": "10.0.0.23"
                            },
                            "RemoteIpDetails": {
                                "City": {
                                    "CityName": "GeneratedFinding"
                                                "CityName"
                                },
                                "Country": {
                                    "CountryName": "GeneratedFinding"
                                                   "CountryName"
                                },
                                "GeoLocation": {
                                    "Lat": 0,
                                    "Lon": 0
                                },
                                "IpAddressV4": "198.51.100.0",
                                "Organization": {
                                    "Asn": "-1",
                                    "AsnOrg": "GeneratedFindingASNOrg",
                                    "Isp": "GeneratedFindingISP",
                                    "Org": "GeneratedFindingORG"
                                }
                            }
                        }
                    ]
                }
            },
            "Evidence": {
                "ThreatIntelligenceDetails": [
                    {
                        "ThreatListName": "GeneratedFindingThreatListName",
                        "ThreatNames": [
                            "GeneratedFindingThreatName"
                        ]
                    }
                ]
            },
            "Archived": False,
            "Count": 5,
            "DetectorId": "detector",
            "EventFirstSeen": "2021-08-09T09:42:27.000Z",
            "EventLastSeen": "2021-09-30T10:19:47.000Z",
            "ResourceRole": "TARGET",
            "ServiceName": "guardduty"
        },
        "Severity": 8,
        "Title": "Unprotected EMR-related port on EC2 "
                 "instance i-99999999 is being probed.",
        "Type": "Recon:EC2/PortProbeEMRUnprotectedPort",
        "UpdatedAt": "2021-09-30T10:19:47.407Z"
    },
    {
        "AccountId": "id",
        "Arn": "arn:aws:guardduty:us-east-2:id:"
               "detector/detector"
               "/finding/5cbd952561ad83a6e287ba028d676cb7",
        "CreatedAt": "2021-08-09T09:42:27.931Z",
        "Description": "EC2 instance has an unprotected "
                       "port which is being probed by a known malicious host.",
        "Id": "5cbd952561ad83a6e287ba028d676cb7",
        "Partition": "aws",
        "Region": "us-east-2",
        "Resource": {
            "InstanceDetails": {
                "AvailabilityZone": "GeneratedFindingInstaceAvailabilityZone",
                "IamInstanceProfile": {
                    "Arn": "arn:aws:iam::id:example/instance/profile",
                    "Id": "GeneratedFindingInstanceProfileId"
                },
                "ImageDescription": "GeneratedFindingInstaceImageDescription",
                "ImageId": "ami-99999999",
                "InstanceId": "i-99999999",
                "InstanceState": "running",
                "InstanceType": "m3.xlarge",
                "OutpostArn": "arn:aws:outposts:us-west-2:id:"
                              "outpost/op-0fbc006e9abbc73c3",
                "LaunchTime": "2016-08-02T02:05:06.000Z",
                "NetworkInterfaces": [
                    {
                        "Ipv6Addresses": [],
                        "NetworkInterfaceId": "eni-bfcffe88",
                        "PrivateDnsName": "GeneratedFinding"
                                          "PrivateDnsName",
                        "PrivateIpAddress": "10.0.0.1",
                        "PrivateIpAddresses": [
                            {
                                "PrivateDnsName": "GeneratedFinding"
                                                  "PrivateName",
                                "PrivateIpAddress": "10.0.0.1"
                            }
                        ],
                        "PublicDnsName": "GeneratedFinding"
                                         "PublicDNSName",
                        "PublicIp": "198.51.100.0",
                        "SecurityGroups": [
                            {
                                "GroupId": "GeneratedFindingSecurityId",
                                "GroupName": "GeneratedFinding"
                                             "SecurityGroupName"
                            }
                        ],
                        "SubnetId": "GeneratedFindingSubnetId",
                        "VpcId": "GeneratedFindingVPCId"
                    }
                ],
                "ProductCodes": [
                    {}
                ],
                "Tags": [
                    {
                        "Key": "GeneratedFindingInstaceTag1",
                        "Value": "GeneratedFindingInstaceValue1"
                    },
                    {
                        "Key": "GeneratedFindingInstaceTag2",
                        "Value": "GeneratedFindingInstaceTagValue2"
                    },
                    {
                        "Key": "GeneratedFindingInstaceTag3",
                        "Value": "GeneratedFindingInstaceTagValue3"
                    },
                    {
                        "Key": "GeneratedFindingInstaceTag4",
                        "Value": "GeneratedFindingInstaceTagValue4"
                    },
                    {
                        "Key": "GeneratedFindingInstaceTag5",
                        "Value": "GeneratedFindingInstaceTagValue5"
                    },
                    {
                        "Key": "GeneratedFindingInstaceTag6",
                        "Value": "GeneratedFindingInstaceTagValue6"
                    },
                    {
                        "Key": "GeneratedFindingInstaceTag7",
                        "Value": "GeneratedFindingInstaceTagValue7"
                    },
                    {
                        "Key": "GeneratedFindingInstaceTag8",
                        "Value": "GeneratedFindingInstaceTagValue8"
                    },
                    {
                        "Key": "GeneratedFindingInstaceTag9",
                        "Value": "GeneratedFindingInstaceTagValue9"
                    }
                ]
            },
            "ResourceType": "Instance"
        },
        "SchemaVersion": "2.0",
        "Service": {
            "Action": {
                "ActionType": "PORT_PROBE",
                "PortProbeAction": {
                    "Blocked": False,
                    "PortProbeDetails": [
                        {
                            "LocalPortDetails": {
                                "Port": 80,
                                "PortName": "HTTP"
                            },
                            "LocalIpDetails": {
                                "IpAddressV4": "10.0.0.23"
                            },
                            "RemoteIpDetails": {
                                "City": {
                                    "CityName": "GeneratedFindingCityName1"
                                },
                                "Country": {
                                    "CountryName": "GeneratedFinding"
                                                   "CountryName1"
                                },
                                "GeoLocation": {
                                    "Lat": 0,
                                    "Lon": 0
                                },
                                "IpAddressV4": "198.51.100.0",
                                "Organization": {
                                    "Asn": "9808",
                                    "AsnOrg": "GeneratedFindingASNOrg1",
                                    "Isp": "GeneratedFindingISP1",
                                    "Org": "GeneratedFindingORG1"
                                }
                            }
                        },
                        {
                            "LocalPortDetails": {
                                "Port": 443,
                                "PortName": "HTTPS"
                            },
                            "LocalIpDetails": {
                                "IpAddressV4": "10.0.0.23"
                            },
                            "RemoteIpDetails": {
                                "City": {
                                    "CityName": "GeneratedFinding"
                                                "CityName2"
                                },
                                "Country": {
                                    "CountryName": "GeneratedFinding"
                                                   "CountryName2"
                                },
                                "GeoLocation": {
                                    "Lat": 0,
                                    "Lon": 0
                                },
                                "IpAddressV4": "198.51.100.1",
                                "Organization": {
                                    "Asn": "29073",
                                    "AsnOrg": "GeneratedFindingASNOrg2",
                                    "Isp": "GeneratedFindingISP2",
                                    "Org": "GeneratedFindingORG2"
                                }
                            }
                        }
                    ]
                }
            },
            "Evidence": {
                "ThreatIntelligenceDetails": [
                    {
                        "ThreatListName": "GeneratedFindingThreatListName",
                        "ThreatNames": [
                            "GeneratedFindingThreatName"
                        ]
                    }
                ]
            },
            "Archived": False,
            "Count": 5,
            "DetectorId": "detector",
            "EventFirstSeen": "2021-08-09T09:42:27.000Z",
            "EventLastSeen": "2021-09-30T10:19:47.000Z",
            "ResourceRole": "TARGET",
            "ServiceName": "guardduty"
        },
        "Severity": 2,
        "Title": "Unprotected port on EC2 instance "
                 "i-99999999 is being probed.",
        "Type": "Recon:EC2/PortProbeUnprotectedPort",
        "UpdatedAt": "2021-09-30T10:19:47.408Z"
    }
]


def guard_duty_response(tile_id=None):
    if tile_id == "port_probe_source_countries":
        return PORT_PROBE_FINDINGS
    return INSTANCE_SOURCE_FINDINGS


def tile_data_response(tile_id):
    data = {
        "affected_instances": {
            "data": {
                "cache_scope": "none",
                "data": [
                    {
                        "key": 0,
                        "segments": [
                            {
                                "key": 0,
                                "value": 1
                            },
                            {
                                "key": 1,
                                "value": 1
                            }
                        ],
                        "value": 2
                    }
                ],
                "hide_legend": False,
                "label_headers": [
                    "Affected instances",
                    "Finding types"
                ],
                "labels": [
                    [
                        "i-99999999"
                    ],
                    [
                        "Backdoor:EC2/C&CActivity.B!DNS",
                        "Trojan:EC2/DriveBySourceTraffic!DNS"
                    ]
                ]
            }
        },
        "events_per_day": {
            "data": {
                "cache_scope": "none",
                "data": [
                    {
                        "key": "09/28",
                        "label": "09/28",
                        "value": 0,
                        "values": []
                    },
                    {
                        "key": "09/27",
                        "label": "09/27",
                        "value": 0,
                        "values": []
                    },
                    {
                        "key": "09/26",
                        "label": "09/26",
                        "value": 0,
                        "values": []
                    },
                    {
                        "key": "09/25",
                        "label": "09/25",
                        "value": 0,
                        "values": []
                    },
                    {
                        "key": "09/24",
                        "label": "09/24",
                        "value": 0,
                        "values": []
                    },
                    {
                        "key": "09/23",
                        "label": "09/23",
                        "value": 1,
                        "values": [
                            {
                                "key": "high",
                                "value": 1
                            }
                        ]
                    },
                    {
                        "key": "09/22",
                        "label": "09/22",
                        "value": 1,
                        "values": [
                            {
                                "key": "high",
                                "value": 1
                            }
                        ]
                    }
                ],
                "hide_legend": False,
                "key_type": "string",
                "keys": [
                    {
                        "key": "high",
                        "label": "High"
                    }
                ]
            }
        },
        "top_ten_findings": {
            "data": {
                "cache_scope": "none",
                "data": ["|  №  | Description | Count |",
                         "| --- | ----------- | ----- |",
                         "| 1 | EC2 instance i-99999999 "
                         "is querying a domain name of "
                         "a remote host that is a known "
                         "source of Drive-By download "
                         "attacks. | 3 |",
                         "| 2 | EC2 instance i-99999999 "
                         "is querying a domain name "
                         "associated with a known "
                         "Command & Control server. | 3 |"],
                "hide_legend": False
            }
        },
        "total_events": {
            "data": {
                "cache_scope": "none",
                "data": [
                    {
                        "icon": "warning",
                        "label": "EC2 finding types",
                        "value": 6,
                        "value_unit": "integer"
                    },
                    {
                        "icon": "warning",
                        "label": "IAM finding types",
                        "value": 0,
                        "value_unit": "integer"
                    },
                    {
                        "icon": "warning",
                        "label": "S3 finding types",
                        "value": 0,
                        "value_unit": "integer"
                    }
                ],
                "hide_legend": False
            }
        },
        "port_probe_source_countries": {
            "data": {
                "cache_scope": "none",
                "data": [
                    {
                        "coordinates": [
                            0,
                            0
                        ],
                        "email_type": "N/A",
                        "hostname": "N/A",
                        "ip_address": "198.51.100.0",
                        "volume": 5
                    },
                    {
                        "coordinates": [
                            0,
                            0
                        ],
                        "email_type": "N/A",
                        "hostname": "N/A",
                        "ip_address": "198.51.100.1",
                        "volume": 5
                    }
                ],
                "hide_legend": False
            }
        }
    }
    data = data[tile_id]
    data["data"].update(
        {
            "observed_time": {
                "end_time": "2021-09-28T19:07:58",
                "start_time": "2021-09-21T16:07:58"
            },
            "valid_time": {
                "end_time": "2021-09-28T19:07:58",
                "start_time": "2021-09-21T16:07:58"
            }
        }
    )
    return data


def tiles_response():
    return {
        "data": [
            AFFECTED_INSTANCES_TILE,
            EVENTS_PER_DAY_TILE,
            TOP_TEN_FINDINGS_TILE,
            TOTAL_EVENTS_TILE,
            PORT_PROBE_COUNTRIES_TILE
        ]
    }


def tile_response(tile_id):
    response = {
        "affected_instances": AFFECTED_INSTANCES_TILE,
        "events_per_day": EVENTS_PER_DAY_TILE,
        "top_ten_findings": TOP_TEN_FINDINGS_TILE,
        "total_events": TOTAL_EVENTS_TILE,
        "port_probe_source_countries": PORT_PROBE_COUNTRIES_TILE
    }
    return {
        "data": response[tile_id]
    }
