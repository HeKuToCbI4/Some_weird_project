class VkWallMonitor:
    """
    Class used to monitor wall activities on desired domains.
    """

    def __init__(self, vk_api):
        self._vk_api = vk_api
        self._monitored_domains = []
        self.

    def add_domain(self, domain):
        if not domain in self._monitored_domains:
            self._monitored_domains.append(domain)
            # TODO: add logic to monitor it.
