import balderhub.smtp.lib.setup_features

class AiosmtpdServerFeature(balderhub.smtp.lib.setup_features.AiosmtpdServerFeature):

    @property
    def hostname(self) -> str:
        return "localhost"

    @property
    def port(self) -> int:
        return 8025
