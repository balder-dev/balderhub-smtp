import logging
import dataclasses
import datetime
from typing import Optional

from balderhub.email.lib.utils import EmailDataMessage
from .smtp_server_feature import SmtpServerFeature

logger = logging.getLogger(__name__)


class SmtpReadableServerFeature(SmtpServerFeature):
    """
    Provides functionality for managing an SMTP server where it is possible to read the outgoing mails.

    This class is an extension of the :class:`balderhub.smtp.lib.scenario_features.SmtpServerFeature` and provides
    additional methods to interact with emails received by the server, allowing the retrieval and management
    of its outbox. It also includes utility methods for restarting and clearing the server’s state.
    """
    @dataclasses.dataclass
    class Message:
        """Bundle of an :class:`EmailDataMessage` together with the timestamp it was received."""
        mail: EmailDataMessage
        received_timestamp: datetime.datetime

    def get_outbox(self, for_mail_address: Optional[str] = None) -> list[Message]:
        """Return all emails received by the server.

        :param for_mail_address: If provided, only messages addressed to this email address
            (matched against the ``To`` header) are returned.
        :return: A list of :class:`Message` objects representing the received mails.
        """
        raise NotImplementedError

    def clear_outbox(self):
        """Remove all received messages from the server's outbox."""
        raise NotImplementedError

    def fixt_reboot_and_clear_outbox(self):
        """Balder fixture that reboots the SMTP server and clears its outbox"""
        logger.info('reboot SMTP server and clear outbox')
        if self.is_running():
            logger.debug(' - server is still running -> shut it down')
            self.shutdown()
        else:
            logger.debug(' - server is already shut down')
        logger.debug(' - clearing outbox')
        self.clear_outbox()
        logger.debug(' - restart server')
        self.start()
        yield
