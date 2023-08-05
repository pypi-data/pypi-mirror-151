from rumpy.api.base import BaseAPI


class PaidGroup(BaseAPI):
    def dapp(self):
        """Get Info of Paidgroup DApp"""
        resp = self._get("/dapps/PaidGroupMvm", api_base=self._client.api_base_paid)
        if resp.get("success"):
            return resp.get("data")
        return resp

    def paidgroup(self):
        """Get Detail of a Paidgroup"""
        self._check_group_id()
        resp = self._get(f"/mvm/paidgroup/{self.group_id}", api_base=self._client.api_base_paid)
        if resp.get("success"):
            return resp.get("data").get("group")
        return resp

    def payment(self):
        """Check Payment"""
        self._check_group_id()
        resp = self._get(f"/mvm/paidgroup/{self.group_id}/{self.group.eth_addr}", api_base=self._client.api_base_paid)
        if resp.get("success"):
            return resp.get("data").get("payment")
        return resp

    def announce(self, amount, duration):
        """Announce a Paidgroup"""
        self._check_group_id()
        self._check_owner()

        relay = {
            "group": self.group_id,
            "owner": self.group.eth_addr,
            "amount": str(amount),
            "duration": duration,
        }
        resp = self._post("/mvm/paidgroup/announce", relay, api_base=self._client.api_base_paid)
        if resp.get("success"):
            return resp.get("data")
        return resp

    def pay(self):
        """Pay for a Paidgroup"""
        self._check_group_id()

        relay = {
            "user": self.group.eth_addr,
            "group": self.group_id,
        }
        resp = self._post("/mvm/paidgroup/pay", relay, api_base=self._client.api_base_paid)
        if resp.get("success"):
            return resp.get("data")
        return resp
