'''
Created on 2 déc. 2014

@author: inso
'''

from .. import PROTOCOL_VERSION
from . import Document
from .certification import SelfCertification, Certification
from .membership import Membership
from .transaction import Transaction

import re
import logging


class Block(Document):
    '''
Version: VERSION
Type: Block
Currency: CURRENCY
Nonce: NONCE
Number: BLOCK_NUMBER
PoWMin: NUMBER_OF_ZEROS
Time: GENERATED_ON
MedianTime: MEDIAN_DATE
UniversalDividend: DIVIDEND_AMOUNT
Issuer: ISSUER_KEY
PreviousHash: PREVIOUS_HASH
PreviousIssuer: PREVIOUS_ISSUER_KEY
Parameters: PARAMETERS
MembersCount: WOT_MEM_COUNT
Identities:
PUBLIC_KEY:SIGNATURE:TIMESTAMP:USER_ID
...
Joiners:
PUBLIC_KEY:SIGNATURE:NUMBER:HASH:TIMESTAMP:USER_ID
...
Actives:
PUBLIC_KEY:SIGNATURE:NUMBER:HASH:TIMESTAMP:USER_ID
...
Leavers:
PUBLIC_KEY:SIGNATURE:NUMBER:HASH:TIMESTAMP:USER_ID
...
Excluded:
PUBLIC_KEY
...
Certifications:
PUBKEY_FROM:PUBKEY_TO:BLOCK_NUMBER:SIGNATURE
...
Transactions:
COMPACT_TRANSACTION
...
BOTTOM_SIGNATURE
    '''

    re_type = re.compile("Type: (Block)\n")
    re_noonce = re.compile("Nonce: ([0-9]+)\n")
    re_number = re.compile("Number: ([0-9]+)\n")
    re_powmin = re.compile("PoWMin: ([0-9]+)\n")
    re_time = re.compile("Time: ([0-9]+)\n")
    re_mediantime = re.compile("MedianTime: ([0-9]+)\n")
    re_universaldividend = re.compile("UniversalDividend: ([0-9]+)\n")
    re_issuer = re.compile("Issuer: ([1-9A-Za-z][^OIl]{42,45})\n")
    re_previoushash = re.compile("PreviousHash: ([0-9a-fA-F]{5,40})\n")
    re_previousissuer = re.compile("PreviousIssuer: ([1-9A-Za-z][^OIl]{42,45})\n")
    re_parameters = re.compile("Parameters: ([0-9]+\.[0-9]+):([0-9]+):([0-9]+):([0-9]+):\
([0-9]+):([0-9]+):([0-9]+):([0-9]+):([0-9]+):([0-9]+):([0-9]+):([0-9]+):([0-9]+):\
([0-9]+\.[0-9]+)\n")
    re_memberscount = re.compile("MembersCount: ([0-9]+)\n")
    re_identities = re.compile("Identities:\n")
    re_joiners = re.compile("Joiners:\n")
    re_actives = re.compile("Actives:\n")
    re_leavers = re.compile("Leavers:\n")
    re_excluded = re.compile("Excluded:\n")
    re_exclusion = re.compile("([1-9A-Za-z][^OIl]{42,45})\n")
    re_certifications = re.compile("Certifications:\n")
    re_transactions = re.compile("Transactions:\n")

    def __init__(self, version, currency, noonce, number, powmin, time,
                 mediantime, ud, issuer, prev_hash, prev_issuer,
                 parameters, members_count, identities, joiners,
                 actives, leavers, excluded, certifications,
                 transactions, signature):
        '''
        Constructor
        '''
        super().__init__(version, currency, [signature])
        self.noonce = noonce
        self.number = number
        self.powmin = powmin
        self.time = time
        self.mediantime = mediantime
        self.ud = ud
        self.issuer = issuer
        self.prev_hash = prev_hash
        self.prev_issuer = prev_issuer
        self.parameters = parameters
        self.members_count = members_count
        self.identities = identities
        self.joiners = joiners
        self.actives = actives
        self.leavers = leavers
        self.excluded = excluded
        self.certifications = certifications
        self.transactions = transactions

    @classmethod
    def from_signed_raw(cls, raw):
        lines = raw.splitlines(True)
        n = 0

        version = int(Block.re_version.match(lines[n]).group(1))
        n = n + 1

        Block.re_type.match(lines[n]).group(1)
        n = n + 1

        currency = Block.re_currency.match(lines[n]).group(1)
        n = n + 1

        noonce = int(Block.re_noonce.match(lines[n]).group(1))
        n = n + 1

        number = int(Block.re_number.match(lines[n]).group(1))
        n = n + 1

        powmin = int(Block.re_powmin.match(lines[n]).group(1))
        n = n + 1

        time = int(Block.re_time.match(lines[n]).group(1))
        n = n + 1

        mediantime = int(Block.re_mediantime.match(lines[n]).group(1))
        n = n + 1

        ud = Block.re_universaldividend.match(lines[n])
        if ud is not None:
            ud = int(ud.group(1))
            n = n + 1

        issuer = Block.re_issuer.match(lines[n]).group(1)
        n = n + 1

        prev_hash = None
        prev_issuer = None
        if number > 0:
            prev_hash = Block.re_previoushash.match(lines[n]).group(1)
            n = n + 1

            prev_issuer = Block.re_previousissuer.match(lines[n]).group(1)
            n = n + 1

        parameters = None
        if number == 0:
            parameters = Block.re_parameters.match(lines[n]).groups()
            n = n + 1

        members_count = int(Block.re_memberscount.match(lines[n]).group(1))
        n = n + 1

        identities = []
        joiners = []
        actives = []
        leavers = []
        excluded = []
        certifications = []
        transactions = []

        if Block.re_identities.match(lines[n]) is not None:
            n = n + 1
            while Block.re_joiners.match(lines[n]) is None:
                selfcert = SelfCertification.from_inline(version, currency, lines[n])
                identities.append(selfcert)
                n = n + 1

        if Block.re_joiners.match(lines[n]):
            n = n + 1
            while Block.re_actives.match(lines[n]) is None:
                membership = Membership.from_inline(version, currency, "IN", lines[n])
                joiners.append(membership)
                n = n + 1

        if Block.re_actives.match(lines[n]):
            n = n + 1
            while Block.re_leavers.match(lines[n]) is None:
                membership = Membership.from_inline(version, currency, "IN", lines[n])
                actives.append(membership)
                n = n + 1

        if Block.re_leavers.match(lines[n]):
            n = n + 1
            while Block.re_excluded.match(lines[n]) is None:
                membership = Membership.from_inline(version, currency, "OUT", lines[n])
                leavers.append(membership)
                n = n + 1

        if Block.re_excluded.match(lines[n]):
            n = n + 1
            while Block.re_certifications.match(lines[n]) is None:
                membership = Block.re_exclusion.match(lines[n]).group(1)
                excluded.append(membership)
                n = n + 1

        if Block.re_certifications.match(lines[n]):
            n = n + 1
            while Block.re_transactions.match(lines[n]) is None:
                certification = Certification.from_inline(version, currency,
                                                          prev_hash, lines[n])
                certifications.append(certification)
                n = n + 1

        if Block.re_transactions.match(lines[n]):
            n = n + 1
            while not Block.re_signature.match(lines[n]):
                tx_lines = ""
                header_data = Transaction.re_header.match(lines[n])
                version = int(header_data.group(1))
                issuers_num = int(header_data.group(2))
                inputs_num = int(header_data.group(3))
                outputs_num = int(header_data.group(4))
                has_comment = int(header_data.group(5))
                tx_max = n+issuers_num*2+inputs_num+outputs_num+has_comment+1
                for i in range(n, tx_max):
                    tx_lines += lines[n]
                    n = n + 1
                transaction = Transaction.from_compact(currency, tx_lines)
                transactions.append(transaction)

        signature = Block.re_signature.match(lines[n]).group(1)

        return cls(version, currency, noonce, number, powmin, time,
                   mediantime, ud, issuer, prev_hash, prev_issuer,
                   parameters, members_count, identities, joiners,
                   actives, leavers, excluded, certifications,
                   transactions, signature)

    def raw(self):
        doc = """Version: {0}
Type: Block
Currency: {1}
Nonce: {2}
Number: {3}
PoWMin: {4}
Time: {5}
MedianTime: {6}
""".format(self.version,
                      self.currency,
                      self.noonce,
                      self.number,
                      self.powmin,
                      self.time,
                      self.mediantime)
        if self.ud:
            doc += "UniversalDividend: {0}\n".format(self.ud)

        doc += "Issuer: {0}\n".format(self.issuer)

        if self.number == 0:
            str_params = ":".join(self.parameters)
            doc += "Parameters: {0}\n".format(str_params)
        else:
            doc += "PreviousHash: {0}\n\
PreviousIssuer: {1}\n".format(self.prev_hash, self.prev_issuer)

        doc += "MembersCount: {0}\n".format(self.members_count)

        doc += "Identities:\n"
        for identity in self.identities:
            doc += "{0}\n".format(identity.inline())

        doc += "Joiners:\n"
        for joiner in self.joiners:
            doc += "{0}\n".format(joiner.inline())

        doc += "Actives:\n"
        for active in self.actives:
            doc += "{0}\n".format(active.inline())

        doc += "Leavers:\n"
        for leaver in self.leavers:
            doc += "{0]\n".format(leaver.inline())

        doc += "Excluded:\n"
        for exclude in self.excluded:
            doc += "{0}\n".format(exclude)

        doc += "Certifications:\n"
        for cert in self.certifications:
            doc += "{0}\n".format(cert.inline())

        doc += "Transactions:\n"
        for transaction in self.transactions:
            doc += "{0}\n".format(transaction.compact())

        return doc
