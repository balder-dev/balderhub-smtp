
import balder


class SmtpServerConfig(balder.Feature):
    """Configuration feature exposing the SMTP server's network coordinates.

    The default values point to a local SMTP server on the standard port. Subclasses can override
    :attr:`host` and :attr:`port` to target a different server.
    """

    @property
    def host(self):
        """Return the hostname or IP address of the SMTP server."""
        return "localhost"

    @property
    def port(self):
        """Return the TCP port the SMTP server is listening on."""
        return 25
