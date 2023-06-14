from dynaconf import Dynaconf


settings = Dynaconf(
    envvar_prefix="TR",
    settings_file=["settings.toml", ".secrets.toml"]
)