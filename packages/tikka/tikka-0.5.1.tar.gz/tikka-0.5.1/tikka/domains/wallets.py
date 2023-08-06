# Copyright 2021 Vincent Texier <vit@free.fr>
#
# This software is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
import hashlib
import random
from typing import Optional

from Crypto.Cipher import ChaCha20_Poly1305
from substrateinterface import Keypair, KeypairType

from tikka.domains.currencies import Currencies
from tikka.domains.entities.constants import WALLETS_NONCE_SIZE
from tikka.domains.entities.wallet import Wallet
from tikka.interfaces.adapters.repository.wallets import WalletsRepositoryInterface


class Wallets:
    """
    Wallets domain class
    """

    def __init__(self, repository: WalletsRepositoryInterface, currencies: Currencies):
        """
        Init Wallets domain

        :param repository: Database adapter instance
        :param currencies: Currencies domain instance
        """
        self.repository = repository
        self.currencies = currencies

    @staticmethod
    def create(address: str, seed_hex: str, password: str) -> Wallet:
        """
        Return an encrypted Wallet instance from seed_hex and password

        :param address: Wallet address
        :param seed_hex: Seed as hexadecimal string
        :param password: Clear password
        :return:
        """
        password_hash = hashlib.sha256(password.encode("utf-8")).digest()
        nonce = random_bytes(WALLETS_NONCE_SIZE)
        cypher = ChaCha20_Poly1305.new(key=password_hash, nonce=nonce)
        encrypted_seed, mac_tag = cypher.encrypt_and_digest(bytes.fromhex(seed_hex))
        return Wallet(
            address=address,
            encrypted_seed=encrypted_seed.hex(),
            encryption_nonce=nonce.hex(),
            encryption_mac_tag=mac_tag.hex(),
        )

    def new_from_seed_hex(
        self, seed_hex: str, password: str, crypto_type: int = KeypairType.SR25519
    ) -> Wallet:
        """
        Create Wallet and add it to repository from seed_hex
        if wallet already exists, update password

        :param seed_hex: Seed hexadecimal string
        :param password: Password string
        :param crypto_type: KeypairType constant, SR25519 by default
        :return:
        """
        # create keypair from mnemonic to get seed as hexadecimal
        keypair = Keypair.create_from_seed(
            seed_hex=seed_hex,
            crypto_type=crypto_type,
            ss58_format=self.currencies.get_current().ss58_format,
        )
        wallet = self.create(keypair.ss58_address, seed_hex, password)

        if self.exists(keypair.ss58_address):
            self.update(wallet)
        else:
            self.add(wallet)

        return wallet

    def add(self, wallet: Wallet):
        """
        Add wallet

        :param wallet: Wallet instance
        :return:
        """
        # add wallet
        self.repository.add(wallet)

    def get(self, address: str) -> Optional[Wallet]:
        """
        Return Wallet instance from address

        :param address:
        :return:
        """
        return self.repository.get(address)

    def get_keypair(self, address: str, password: str) -> Optional[Keypair]:
        """
        Get Keypair instance from Wallet address

        :param address: Wallet address
        :param password: Wallet password
        :return:
        """
        wallet = self.get(address)
        if wallet is None:
            return None
        password_hash = hashlib.sha256(password.encode("utf-8")).digest()
        cypher = ChaCha20_Poly1305.new(
            key=password_hash, nonce=bytes.fromhex(wallet.encryption_nonce)
        )
        seed_hex_bytes = cypher.decrypt_and_verify(
            bytes.fromhex(wallet.encrypted_seed),
            bytes.fromhex(wallet.encryption_mac_tag),
        )
        return Keypair.create_from_seed(
            seed_hex=seed_hex_bytes.hex(),
            ss58_format=self.currencies.get_current().ss58_format,
        )

    def update(self, wallet: Wallet):
        """
        Update wallet

        :param wallet: Wallet instance
        :return:
        """
        self.repository.update(wallet)

    def delete(self, address: str) -> None:
        """
        Delete wallet in repository

        :param address: Wallet address to delete
        :return:
        """
        self.repository.delete(address)

    def exists(self, address: str) -> bool:
        """
        Return True if wallet with address exists in repository

        :param address: Address to check
        :return:
        """
        return self.repository.exists(address)


def random_bytes(size: int) -> bytes:
    """
    Return random bytes of given length

    :param size: Size of nonce in bytes
    :return:
    """
    return bytearray(random.getrandbits(8) for _ in range(size))
