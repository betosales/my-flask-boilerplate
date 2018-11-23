import unittest

from flask_migrate import Migrate

from project.server import app, db

migrate = Migrate(app, db)


@app.cli.command()
def test():
    """Runs the unit tests without test coverage."""
    tests = unittest.TestLoader().discover('project/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


@app.cli.command()
def create_db():
    """Creates the db tables."""
    db.create_all()


@app.cli.command()
def drop_db():
    """Drops the db tables."""
    db.drop_all()


@app.cli.command()
def drop_migrations():
    """Drops alembics directories and database resources."""
    db.engine.execute("DROP TABLE IF EXISTS alembic_version CASCADE")
    import shutil
    import os

    migration_dir = os.path.dirname(__file__) + '/migrations'
    shutil.rmtree(migration_dir, ignore_errors=True)

    print("Migrations are dropped.")


if __name__ == '__main__':
    app.run()
