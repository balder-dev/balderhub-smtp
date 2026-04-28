import logging

import balder

logger = logging.getLogger(__name__)


class SmtpServerFeature(balder.Feature):
    """
    Abstract scenario feature describing an SMTP server used during a test.

    Concrete setup features (e.g. :class:`~balderhub.smtp.lib.setup_features.AiosmtpdServerFeature`)
    must implement the lifecycle methods (:meth:`start`, :meth:`shutdown`, :meth:`is_running`)
    as well as the outbox-related methods (:meth:`get_outbox`, :meth:`clear_outbox`).
    """

    def start(self):
        """Start the SMTP server so that it can accept incoming connections."""
        raise NotImplementedError

    def shutdown(self):
        """Shut the SMTP server down and release any held resources."""
        raise NotImplementedError

    def is_running(self) -> bool:
        """Return ``True`` if the SMTP server is currently running and reachable."""
        raise NotImplementedError
