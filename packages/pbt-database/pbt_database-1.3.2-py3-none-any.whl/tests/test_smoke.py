from sqlalchemy.engine import URL


def test_connection(options):
    """Test database connection params."""

    from database import connection
    assert connection.host == options['db_host']
    assert connection.port == int(options['db_port'])
    assert connection.database == options['db_name']
    assert connection.username == options['db_user']
    assert connection.password == options['db_password']

    assert connection.dsn == URL.create(
        drivername='postgresql+asyncpg',
        host=options['db_host'],
        port=int(options['db_port']),
        database=options['db_name'],
        username=options['db_user'],
        password=options['db_password'],
    )
