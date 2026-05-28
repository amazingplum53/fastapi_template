import sys

from app.bootstrap import command

ALEMBIC_CONFIG_PATH = "app/database/alembic.ini"

def get_alembic_config():
    from alembic.config import Config

    return Config(ALEMBIC_CONFIG_PATH)


@command
def db_current():
    from alembic import command as alembic_command

    alembic_command.current(get_alembic_config())


@command
def db_upgrade():
    from alembic import command as alembic_command

    print("Running migrations...")
    alembic_command.upgrade(get_alembic_config(), "head")
    print("Migrations complete.")


@command
def db_revision(message: str):
    from alembic import command as alembic_command

    alembic_command.revision(
        get_alembic_config(),
        message=message,
        autogenerate=True,
    )


def main() -> None:
    if len(sys.argv) < 2:
        raise SystemExit(
            "Usage: python -m app.database.commands "
            "{db_current|db_upgrade|db_revision}"
        )

    command_name = sys.argv[1]

    if command_name == "db_current":
        db_current()

    elif command_name == "db_upgrade":
        db_upgrade()

    elif command_name == "db_revision":
        if len(sys.argv) < 3:
            raise SystemExit(
                'Usage: python -m app.database.commands db_revision "message"'
            )

        db_revision(sys.argv[2])

    else:
        raise SystemExit(f"Unknown command: {command_name}")


if __name__ == "__main__":
    main()