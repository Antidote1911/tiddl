import click

from click import style
from time import sleep

from tiddl.auth import getDeviceAuth, getToken, refreshToken
from .ctx import passContext, Context


@click.group("auth")
def AuthGroup():
    """Manage Tidal token"""


@AuthGroup.command("login")
@passContext
def login(ctx: Context):
    """Add token to the config"""

    if ctx.obj.config._config.get("token"):
        click.echo(style("Already logged in", fg="green"))
        return

    auth = getDeviceAuth()

    uri = f'https://{auth["verificationUriComplete"]}'
    click.launch(uri)
    click.echo(f"Go to {style(uri, fg='cyan')} and complete authentication!")

    # TODO: show time left for auth with `expiresIn`

    while True:
        sleep(auth["interval"])

        token = getToken(auth["deviceCode"])
        error: str | None = token.get("error")

        if error == "authorization_pending":
            continue

        if error == "expired_token":
            click.echo(f"Time for authentication {style('has expired', fg='red')}.")
            break

        assert error == None, token

        # TODO: save token to the config
        click.echo(token)

        click.echo(style("Authenticated!", fg="green"))

        break


@AuthGroup.command("logout")
@passContext
def logout(ctx: Context):
    """* Not implemented *"""
    # https://github.com/Fokka-Engineering/TIDAL/wiki/log-out
