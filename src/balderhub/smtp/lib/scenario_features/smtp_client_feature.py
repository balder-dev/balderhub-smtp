from typing import Optional

import balder

from balderhub.email.lib.utils import EmailDataMessage


class SmtpClientFeature(balder.Feature):
    """
    Abstract scenario feature describing an SMTP client capable of sending emails.

    Concrete setup features (e.g. :class:`~balderhub.smtp.lib.setup_features.SmtplibClientFeature`)
    have to provide an actual implementation of :meth:`send_mail`.
    """

    def send_mail(
            self,
            message: EmailDataMessage,
            mail_from: Optional[str] = None,
            mail_to: Optional[list[str]] = None
    ):
        """Send the given :class:`EmailDataMessage` via SMTP.

        :param message: The fully prepared email to be sent.
        :param mail_from: Optional envelope sender address. If ``None``, the address of
            ``message.from_address`` is used by the underlying implementation.
        :param mail_to: Optional list of envelope recipient addresses. If ``None``, the recipients
            are derived from the ``To``/``Cc``/``Bcc`` headers of ``message``.
        """
