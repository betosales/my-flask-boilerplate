<<<<<<< HEAD
# -*- coding: utf-8 -*-
=======
>>>>>>> d3c274b57f6102f820b377efbc00e4c8d07dc009
import unittest

from flask_migrate import Migrate

from project.server import app, db

migrate = Migrate(app, db)


@app.cli.command()
def test():
    """Runs the unit tests without test coverage."""
<<<<<<< HEAD
    if app.config['TESTING'] is not True:
        raise AttributeError('Environment testing system is not properly configured.')
    # create all tables to begin the tests
    db.create_all()

    # looking for all python files starts with test in project/server
    tests = unittest.TestLoader() \
        .discover('project/server/', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)

    # drop all tables when tests are finished
    db.drop_all()
=======
    tests = unittest.TestLoader().discover('project/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
>>>>>>> d3c274b57f6102f820b377efbc00e4c8d07dc009
    if result.wasSuccessful():
        return 0
    return 1


@app.cli.command()
def create_db():
<<<<<<< HEAD
    """Create the db tables."""
=======
    """Creates the db tables."""
>>>>>>> d3c274b57f6102f820b377efbc00e4c8d07dc009
    db.create_all()


@app.cli.command()
def drop_db():
<<<<<<< HEAD
    """Drop the db tables."""
=======
    """Drops the db tables."""
>>>>>>> d3c274b57f6102f820b377efbc00e4c8d07dc009
    db.drop_all()


@app.cli.command()
def drop_migrations():
<<<<<<< HEAD
    """Drop alembics directories and database resources."""
=======
    """Drops alembics directories and database resources."""
>>>>>>> d3c274b57f6102f820b377efbc00e4c8d07dc009
    db.engine.execute("DROP TABLE IF EXISTS alembic_version CASCADE")
    import shutil
    import os

    migration_dir = os.path.dirname(__file__) + '/migrations'
    shutil.rmtree(migration_dir, ignore_errors=True)

    print("Migrations are dropped.")


if __name__ == '__main__':
    app.run()
