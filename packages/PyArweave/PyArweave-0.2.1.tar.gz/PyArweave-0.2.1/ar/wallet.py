import json
from jose import jwk
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_PSS
from Crypto.Hash import SHA256
from .utils import (
    winston_to_ar,
    owner_to_address,
)
from . import DEFAULT_API_URL
from .peer import Peer


class Wallet(object):
    HASH = 'sha256'

    def _set_jwk_params(self):
        self.jwk_data['p2s'] = ''
        self.jwk = jwk.construct(self.jwk_data, algorithm=jwk.ALGORITHMS.RS256)
        self.rsa = RSA.importKey(self.jwk.to_pem())

        self.owner = self.jwk_data.get('n')
        self.address = owner_to_address(self.owner)

        self.peer = Peer(DEFAULT_API_URL)
    @property
    def api_url(self):
        return self.peer.api_url
    @api_url.setter
    def set_api_url(self, api_url):
        self.peer.api_url = api_url

    def __init__(self, jwk_file='jwk_file.json'):
        with open(jwk_file, 'r') as j_file:
            self.jwk_data = json.loads(j_file.read())
        self._set_jwk_params()

    @classmethod
    def from_data(cls, jwk_data):
        wallet = cls.__new__(cls)
        wallet.jwk_data = jwk_data
        wallet._set_jwk_params()
        return wallet

    @property
    def balance(self):
        balance = self.peer.wallet_balance(self.address)
        return winston_to_ar(balance)

    def sign(self, message):
        h = SHA256.new(message)
        signed_data = PKCS1_PSS.new(self.rsa).sign(h)
        return signed_data

    def verify(self):
        pass

    def get_last_transaction_id(self):
        self.last_tx = self.peer.tx_anchor()
        return self.last_tx
