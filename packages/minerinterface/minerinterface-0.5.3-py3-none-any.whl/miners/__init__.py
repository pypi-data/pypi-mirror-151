from API.bmminer import BMMinerAPI
from API.bosminer import BOSMinerAPI
from API.cgminer import CGMinerAPI
from API.btminer import BTMinerAPI
from API.unknown import UnknownAPI
import ipaddress
import asyncssh
import logging


class BaseMiner:
    def __init__(
        self,
        ip: str,
        api: BMMinerAPI or BOSMinerAPI or CGMinerAPI or BTMinerAPI or UnknownAPI,
    ) -> None:
        self.ip = ipaddress.ip_address(ip)
        self.uname = None
        self.pwd = None
        self.api = api
        self.api_type = None
        self.model = None
        self.light = None
        self.hostname = None
        self.nominal_chips = 1

    async def _get_ssh_connection(self) -> asyncssh.connect:
        """Create a new asyncssh connection"""
        try:
            conn = await asyncssh.connect(
                str(self.ip),
                known_hosts=None,
                username=self.uname,
                password=self.pwd,
                server_host_key_algs=["ssh-rsa"],
            )
            return conn
        except asyncssh.misc.PermissionDenied:
            try:
                conn = await asyncssh.connect(
                    str(self.ip),
                    known_hosts=None,
                    username="admin",
                    password="admin",
                    server_host_key_algs=["ssh-rsa"],
                )
                return conn
            except asyncssh.misc.PermissionDenied:
                try:
                    conn = await asyncssh.connect(
                        str(self.ip),
                        known_hosts=None,
                        username="root",
                        password="root",
                        server_host_key_algs=["ssh-rsa"],
                    )
                    return conn
                except Exception as e:
                    # logging.warning(f"{self} raised an exception: {e}")
                    raise e
        except OSError:
            logging.warning(f"Connection refused: {self}")
            return None
        except Exception as e:
            # logging.warning(f"{self} raised an exception: {e}")
            raise e

    async def fault_light_on(self) -> bool:
        return False

    async def fault_light_off(self) -> bool:
        return False

    async def send_file(self, src, dest):
        async with (await self._get_ssh_connection()) as conn:
            await asyncssh.scp(src, (conn, dest))

    async def check_light(self):
        return self.light

    async def get_board_info(self):
        return None

    async def get_config(self):
        return None

    async def get_hostname(self):
        return None

    async def get_model(self):
        return None

    async def reboot(self):
        return False

    async def restart_backend(self):
        return False

    async def send_config(self, *args, **kwargs):
        return None

    async def get_data(self):
        data = {
            "IP": str(self.ip),
            "Model": "Unknown",
            "Hostname": "Unknown",
            "Hashrate": 0,
            "Temperature": 0,
            "Pool User": "Unknown",
            "Wattage": 0,
            "Split": 0,
            "Pool 1": "Unknown",
            "Pool 1 User": "Unknown",
            "Pool 2": "",
            "Pool 2 User": "",
        }
        return data
