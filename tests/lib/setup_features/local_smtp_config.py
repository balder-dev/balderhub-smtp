import balderhub.smtp.lib.scenario_features


class LocalSmtpConfig(balderhub.smtp.lib.scenario_features.SmtpServerConfig):

    @property
    def port(self):
        return 8025
