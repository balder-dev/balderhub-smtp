import balder
import balderhub.email.lib.scenario_features
from balderhub.email.lib.utils import EmailDataMessage

from balderhub.smtp.lib.scenario_features import SmtpReadableServerFeature


class ProxySmtpReader(balderhub.email.lib.scenario_features.EmailReaderFeature):
    """
    Represents a proxy SMTP reader, that can be used if the readbale-smtp server does not belong to this device and
    is part of a remote device.
    """
    class SmtpServer(balder.VDevice):
        """VDevice representing SMTP server"""
        #: the readable server feature of the smtp server
        server = SmtpReadableServerFeature()

    def get_mails(self) -> list[EmailDataMessage]:
        outbox = self.SmtpServer.server.get_outbox()
        if outbox is None:
            raise ValueError('remote SMTP server has not been started')
        return [msg.mail for msg in outbox]
