from enum import Enum


class ZoneType(Enum):
    A = "A"
    AAAA = "AAAA"
    CERT = "CERT"
    CNAME = "CNAME"
    DNSKEY = "DNSKEY"
    DS = "DS"
    HTTPS = "HTTPS"
    LOC = "LOC"
    MX = "MX"
    NAPTR = "NAPTR"
    NS = "NS"
    SMIMEA = "SMIMEA"
    SRV = "SRV"
    SSHFP = "SSHFP"
    SVCB = "SVCB"
    TLSA = "TLSA"
    TXT = "TXT"
    URI = "URI"
