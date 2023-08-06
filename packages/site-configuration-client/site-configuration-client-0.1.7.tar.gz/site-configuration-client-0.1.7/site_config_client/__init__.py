import requests
from typing import Union
import uuid
from urllib.parse import urljoin

from .exceptions import SiteConfigurationError


class Client:
    def __init__(self, base_url, api_token, environment,
                 read_only_storage=None, cache=None, request_timeout=30):
        """
        Instantiate a new API Client
        """
        self.base_url = base_url
        self.api_token = api_token
        self.environment = environment
        self.read_only_storage = read_only_storage
        self.cache = cache
        self.request_timeout = request_timeout

    def request(self, method, url_path, success_status_code=200, **kwargs):
        """
        Send requests to the Site Configuration service and handle errors.

        Sets timeout and accepts a relative URL.
        """
        headers = {'Authorization': 'Token {}'.format(self.api_token)}
        response = requests.request(
            method=method,
            url=urljoin(self.base_url, url_path),
            timeout=self.request_timeout,
            headers=headers,
            **kwargs
        )

        if response.status_code == success_status_code:
            return response.json()
        else:
            raise SiteConfigurationError((
                'Something went wrong with the site configuration API '
                '`{path}` with status_code="{status_code}" body="{body}"'
            ).format(
                path=url_path,
                status_code=response.status_code,
                body=response.content,
            ))

    def create_site(self, domain_name: str, site_uuid=None):
        """
        Create a new site.
        """
        params = {'domain_name': domain_name}
        if site_uuid:
            params['uuid'] = site_uuid
        url = 'v1/environment/{}/site/'.format(self.environment)
        return self.request('post', url, success_status_code=201, json=params)

    def list_sites(self):
        """
        Returns a list of all Sites
        """
        url = 'v1/environment/{}/site/'.format(self.environment)
        return self.request('get', url)

    def list_active_sites(self):
        """
        Returns a list of all active Sites
        """
        url = 'v1/environment/{}/site/?is_active=True'.format(self.environment)
        return self.request('get', url)

    def get_backend_configs(self, site_uuid: Union[str, uuid.UUID],
                            status: str):
        """
        Returns a combination of Site information and `live` or `draft`
        Configurations (backend secrets included)

        [Client Configuration]
        - Django Cache
            - if cache key exists: return config from cache
            - if cache key does not exist: call endpoint to get config, set
              cache with config, return config
        """
        cache_key = 'site_config_client.{}.{}'.format(site_uuid, status)
        if self.cache:
            config = self.cache.get(key=cache_key)
            if config:
                return config

        api_endpoint = 'v1/environment/{}/combined-configuration/backend/{}/{}/'.format(
            self.environment, site_uuid, status
        )
        config = self.request('get', url_path=api_endpoint)

        if self.cache:
            self.cache.set(cache_key, config)
        return config

    def get_config(self, site_uuid: Union[str, uuid.UUID],
                   type: str, name: str, status: str):
        """
        Returns a single configuration object for Site
        """
        api_endpoint = 'v1/environment/{}/configuration/{}/'.format(self.environment, site_uuid)
        return self.request('get', url_path=api_endpoint, params={
            "type": type,
            "name": name,
            "status": status
        })

    def override_configs(self, site_uuid: Union[str, uuid.UUID], configs):
        """
        Override all live configs in a single pass.

        This uses the v0 API which should be deprecated after the initial
        rollout.
        """
        api_endpoint = 'v0/configuration-override/{}/'.format(site_uuid)
        return self.request('put', url_path=api_endpoint, json=configs)
