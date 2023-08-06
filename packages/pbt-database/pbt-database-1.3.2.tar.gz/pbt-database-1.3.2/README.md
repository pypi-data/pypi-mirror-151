[![N|Solid](https://294904.selcdn.ru/git/logo.png)](https://portalbilet.ru/)
## Database driver

Provide PostgresSQL Model built-ins with i18n support.

Use as package with service core and setup with env variables.

## Maintain
Use poetry for all:
```sh
poetry install
poetry build
poetry publish
```

## CI/CD Options

| option          | type  | info     |
| -----           | ----- | -----    |
| **DB_HOST**       | str   |  Host    |
| **DB_PORT**       | int   |  Port    |
| **DB_NAME**       | str   | Database |
| **DB_USER**       | str   | Username |
| **DB_PASSWORD**   | str   | Password |


## Testing
```.sh
pytest tests
```
| :warning: Check database connection before launch - all data will be erased!|
|-----------------------------------------------------------------------------|

## License
```
MIT © PortalBilet Team, 2022
```
