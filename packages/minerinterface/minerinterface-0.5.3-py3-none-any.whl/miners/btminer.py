from API.btminer import BTMinerAPI
from miners import BaseMiner
from API import APIError
import logging
from settings import MINER_FACTORY_GET_VERSION_RETRIES as DATA_RETRIES


class BTMiner(BaseMiner):
    def __init__(self, ip: str) -> None:
        api = BTMinerAPI(ip)
        self.model = None
        super().__init__(ip, api)
        self.nominal_chips = 66

    def __repr__(self) -> str:
        return f"BTMiner: {str(self.ip)}"

    async def get_model(self):
        if self.model:
            logging.debug(f"Found model for {self.ip}: {self.model}")
            return self.model
        version_data = await self.api.devdetails()
        if version_data:
            self.model = version_data["DEVDETAILS"][0]["Model"].split("V")[0]
            logging.debug(f"Found model for {self.ip}: {self.model}")
            return self.model
        logging.warning(f"Failed to get model for miner: {self}")
        return None

    async def get_hostname(self) -> str:
        if self.hostname:
            return self.hostname
        try:
            host_data = await self.api.get_miner_info()
            if host_data:
                host = host_data["Msg"]["hostname"]
                logging.debug(f"Found hostname for {self.ip}: {host}")
                self.hostname = host
                return self.hostname
        except APIError:
            logging.warning(f"Failed to get hostname for miner: {self}")
            return "?"
        except Exception as e:
            logging.warning(f"Failed to get hostname for miner: {self}")
            return "?"

    async def get_board_info(self) -> dict:
        """Gets data on each board and chain in the miner."""
        logging.debug(f"{self}: Getting board info.")
        devs = await self.api.devs()
        if not devs.get("DEVS"):
            print("devs error", devs)
            return {0: [], 1: [], 2: []}
        devs = devs["DEVS"]
        boards = {}
        offset = devs[0]["ID"]
        for board in devs:
            boards[board["ID"] - offset] = []
            if "Effective Chips" in board.keys():
                if not board["Effective Chips"] in self.nominal_chips:
                    nominal = False
                else:
                    nominal = True
                boards[board["ID"] - offset].append(
                    {
                        "chain": board["ID"] - offset,
                        "chip_count": board["Effective Chips"],
                        "chip_status": "o" * board["Effective Chips"],
                        "nominal": nominal,
                    }
                )
            else:
                logging.warning(f"Incorrect board data from {self}: {board}")
                print(board)
        logging.debug(f"Found board data for {self}: {boards}")
        return boards

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

        model = await self.get_model()
        hostname = await self.get_hostname()

        if model:
            data["Model"] = model

        if hostname:
            data["Hostname"] = hostname
        miner_data = None
        for i in range(DATA_RETRIES):
            miner_data = await self.api.multicommand("summary", "devs", "pools")
            if miner_data:
                break

        if not miner_data:
            return data

        summary = miner_data.get("summary")[0]
        devs = miner_data.get("devs")[0]
        pools = miner_data.get("pools")[0]

        if summary:
            summary_data = summary.get("SUMMARY")
            if summary_data:
                if len(summary_data) > 0:
                    hr = summary_data[0].get("MHS 5s")
                    if hr:
                        data["Hashrate"] = round(hr / 1000000, 2)

                    wattage = summary_data[0].get("Power")
                    if wattage:
                        data["Wattage"] = round(wattage)

        if devs:
            temp_data = devs.get("DEVS")
            if temp_data:
                for board in temp_data:
                    temp = board.get("Chip Temp Avg")
                    if temp and not temp == 0.0:
                        data["Temperature"] = round(temp)
                        break

        if pools:
            pool_1 = None
            pool_2 = None
            pool_1_user = None
            pool_2_user = None
            pool_1_quota = 1
            pool_2_quota = 1
            quota = 0
            for pool in pools.get("POOLS"):
                if not pool_1_user:
                    pool_1_user = pool.get("User")
                    pool_1 = pool["URL"]
                    pool_1_quota = pool["Quota"]
                elif not pool_2_user:
                    pool_2_user = pool.get("User")
                    pool_2 = pool["URL"]
                    pool_2_quota = pool["Quota"]
                if not pool.get("User") == pool_1_user:
                    if not pool_2_user == pool.get("User"):
                        pool_2_user = pool.get("User")
                        pool_2 = pool["URL"]
                        pool_2_quota = pool["Quota"]
            if pool_2_user and not pool_2_user == pool_1_user:
                quota = f"{pool_1_quota}/{pool_2_quota}"

            if pool_1:
                if pool_1.startswith("stratum+tcp://"):
                    pool_1.replace("stratum+tcp://", "")
                if pool_1.startswith("stratum2+tcp://"):
                    pool_1.replace("stratum2+tcp://", "")
                data["Pool 1"] = pool_1

            if pool_1_user:
                data["Pool 1 User"] = pool_1_user
                data["Pool User"] = pool_1_user

            if pool_2:
                if pool_2.startswith("stratum+tcp://"):
                    pool_2.replace("stratum+tcp://", "")
                if pool_2.startswith("stratum2+tcp://"):
                    pool_2.replace("stratum2+tcp://", "")
                data["Pool 2"] = pool_2

            if pool_2_user:
                data["Pool 2 User"] = pool_2_user

            if quota:
                data["Split"] = quota

        return data
