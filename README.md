# SQLAlchemy ORM 1.4 with FastAPI on asyncio

This is a tutorial app build for my [blog post](https://rogulski.it/blog/sqlalchemy-14-async-orm-with-fastapi/)
## Run project
`docker-compose up`

## Run tests
`docker-compose run app pytest`

## Generate migrations
`docker-compose run app alembic revision --autogenerate`

## Run migrations
`docker-compose run app alembic upgrate head`