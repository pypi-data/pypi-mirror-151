from logging import getLogger
from typing import Any, Callable, Dict, Type

from requests import Session

from pyinaturalist.auth import get_access_token
from pyinaturalist.constants import JsonResponse
from pyinaturalist.controllers import (
    ObservationController,
    PlaceController,
    ProjectController,
    TaxonController,
    UserController,
)
from pyinaturalist.models import T
from pyinaturalist.paginator import Paginator
from pyinaturalist.request_params import get_valid_kwargs, strip_empty_values
from pyinaturalist.session import ClientSession

logger = getLogger(__name__)


# 'iNatClient' is nonstandard casing, but 'InatClient' just looks wrong. Deal with it, pep8.
class iNatClient:
    """**WIP/Experimental**

    API client class that provides a higher-level interface that is easier to configure, and returns
    :ref:`model objects <models>` instead of JSON. See :ref:`Controller classes <controllers>` for
    request details.

    Examples:
        **Basic usage**

        Search for observations by taxon name:

        >>> from pyinaturalist import iNatClient
        >>> client = iNatClient()
        >>> observations = client.observations.search(taxon_name='Danaus plexippus')

        Get a single observation by ID:

        >>> observation = client.observations(12345)

        **Authentication**

        Add credentials needed for authenticated requests:
        Note: Passing credentials via environment variables or keyring is preferred

        >>> creds = {
        ...     'username': 'my_inaturalist_username',
        ...     'password': 'my_inaturalist_password',
        ...     'app_id': '33f27dc63bdf27f4ca6cd95dd9dcd5df',
        ...     'app_secret': 'bbce628be722bfe2abd5fc566ba83de4',
        ... }
        >>> client = iNatClient(creds=creds)

        **Default request parameters:**

        Add default ``locale`` and ``preferred_place_id`` request params to pass to any requests
        that use them:

        >>> default_params={'locale': 'en', 'preferred_place_id': 1}
        >>> client = iNatClient(default_params=default_params)

        **Caching, Rate-limiting, and Retries**

        See :py:class:`.ClientSession` and the :ref:`user_guide` for details on these settings.
        ``iNatClient`` will accept any arguments for ``ClientSession``, for example:

        >>> client = iNatClient(per_second=50, expire_after=3600, retries=3)

        Or you can provide your own custom session object:

        >>> session = MyCustomSession(encabulation_factor=47.2)
        >>> client = iNatClient(session=session)

        **Updating settings**

        All settings can also be modified after creating the client:

        >>> client.session = ClientSession()
        >>> client.creds['username'] = 'my_inaturalist_username'
        >>> client.default_params['locale'] = 'es'
        >>> client.dry_run = True

    Args:
        creds: Optional arguments for :py:func:`.get_access_token`, used to get and refresh access
            tokens as needed. Using a keyring instead is recommended, though.
        default_params: Default request parameters to pass to any applicable API requests
        dry_run: Just log all requests instead of sending real requests
        session: Session object to use instead of creating a new one
        kwargs: Keyword arguments for :py:class:`.ClientSession`
    """

    def __init__(
        self,
        creds: Dict[str, str] = None,
        default_params: Dict[str, Any] = None,
        dry_run: bool = False,
        session: Session = None,
        **kwargs,
    ):
        self.creds = creds or {}
        self.default_params = default_params or {}
        self.dry_run = dry_run
        self.session = session or ClientSession(**kwargs)

        self._access_token = None
        self._token_expires = None

        # Controllers
        # TODO: Improve Sphinx docs generated for these attributes
        self.observations = ObservationController(self)  #: Interface for observation requests
        self.places = PlaceController(self)  #: Interface for project requests
        self.projects = ProjectController(self)  #: Interface for project requests
        self.taxa = TaxonController(self)  #: Interface for taxon requests
        self.users = UserController(self)  #: Interface for user requests

    def _update_kwargs(self, request_function, auth: bool = False, **kwargs):
        """Apply any applicable client settings to request parameters before sending a request.
        Explicit keyword arguments will override any client settings.
        """
        kwargs = strip_empty_values(kwargs)
        client_settings = {
            'dry_run': self.dry_run,
            'session': self.session,
        }

        # Add access token and default params, if applicable
        if auth:
            client_settings['access_token'] = get_access_token(**self.creds)  # type: ignore
        client_settings.update(get_valid_kwargs(request_function, self.default_params))

        for k, v in client_settings.items():
            kwargs.setdefault(k, v)

        return kwargs

    def request(self, request_function: Callable, auth: bool = False, **kwargs) -> JsonResponse:
        """Send a request, with client settings applied

        Args:
            request_function: The API request function to call, which should return a JSON response
            auth: Indicates that the request requires authentication
            params: Original request parameters
        """
        kwargs = self._update_kwargs(request_function, auth, **kwargs)
        return request_function(**kwargs)

    def paginate(
        self,
        request_function: Callable,
        model: T,
        auth: bool = False,
        cls: Type[Paginator] = Paginator,
        **kwargs,
    ) -> Paginator[T]:
        """Create a paginator for a request, with client settings applied

        Args:
            request_function: The API request function to call, which should return a JSON response
            model: Model class used for the response
            auth: Indicates that the request requires authentication
            cls: Alternative Paginator class to use
            params: Original request parameters
        """
        kwargs = self._update_kwargs(request_function, auth, **kwargs)
        return cls(request_function, model, **kwargs)
