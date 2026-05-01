import balderhub.email.lib.scenario_features
from balderhub.email.lib.utils import EmailDataMessage

from balderhub.smtp.lib.scenario_features import SmtpReadableServerFeature


class LocalSmtpReader(balderhub.email.lib.scenario_features.EmailReaderFeature):
    """
    Handles reading emails from a local SMTP servers' outbox.

    This class provides functionality to connect to a local SMTP server and
    retrieve emails from its outbox. It relies on the SmtpServerFeature to
    interact with the SMTP server.
    """
    #: feature reference to readable smtp server
    server = SmtpReadableServerFeature()

    def get_mails(self) -> list[EmailDataMessage]:
        outbox = self.server.get_outbox()
        if outbox is None:
            raise ValueError('SMTP server has not been started')
        return [msg.mail for msg in outbox]
