from trac.core import Component, implements, TracError
from trac.db.schema import Table, Column
from trac.env import IEnvironmentSetupParticipant
from trac.db.api import DatabaseManager

PLUGIN_NAME = 'roadmap_tickets_slack'
PLUGIN_VERSION = 1

SCHEMA = [
    Table('roadmap_channel', key=('id',))[
        Column('id', auto_increment=True),
        Column('roadmap'),
        Column('channel'),
        Column('created'),
    ]
]


class RoadmapTicketsSlackSetup(Component):
    """Component that deals with database setup and upgrades."""

    implements(IEnvironmentSetupParticipant)

    def environment_created(self):
        dbm = DatabaseManager(self.env)
        dbm.create_tables(SCHEMA)
        self.__set_database_version(PLUGIN_VERSION, PLUGIN_NAME)

    def environment_needs_upgrade(self, db):
        """
        Called when Trac checks whether the environment needs to be upgraded.
        Returns `True` if upgrade is needed, `False` otherwise.
        """
        return self.__needs_upgrade(PLUGIN_VERSION, PLUGIN_NAME)

    def upgrade_environment(self, db):
        """
        Actually perform an environment upgrade, but don't commit as
        that is done by the common upgrade procedure when all plugins are done.
        """
        dbm = DatabaseManager(self.env)
        if self.__get_database_version(PLUGIN_NAME) == 0:
            dbm.create_tables(SCHEMA)
            self.__set_database_version(PLUGIN_VERSION, PLUGIN_NAME)
        else:
            self.__upgrade(PLUGIN_VERSION, PLUGIN_NAME, 'trac_slack_extend.roadmap_tickets_slack.db_upgrades')

    def __get_database_version(self, name='database_version'):
        """Returns the database version from the SYSTEM table as an int,
        or `False` if the entry is not found.

        :param name: The name of the entry that contains the database version
                     in the SYSTEM table. Defaults to `database_version`,
                     which contains the database version for Trac.
        """
        rows = self.env.db_query("""SELECT value FROM system WHERE name=%s""", (name,))
        return int(rows[0][0]) if rows else False

    def __needs_upgrade(self, version, name='database_version'):
        """Checks the database version to determine if an upgrade is needed.

        :param version: the expected integer database version.
        :param name: the name of the entry in the SYSTEM table that contains
                     the database version. Defaults to `database_version`,
                     which contains the database version for Trac.

        :return: `True` if the stored version is less than the expected
                  version, `False` if it is equal to the expected version.
        :raises TracError: if the stored version is greater than the expected
                           version.
        """
        dbver = self.__get_database_version(name)
        if dbver == version:
            return False
        elif dbver > version:
            raise TracError("Need to downgrade %s." % name)
        self.env.log.info("Need to upgrade %s from %d to %d", name, dbver, version)
        return True

    def __set_database_version(self, version, name='database_version'):
        """Sets the database version in the SYSTEM table.

        :param version: an integer database version.
        :param name: The name of the entry that contains the database version
                     in the SYSTEM table. Defaults to `database_version`,
                     which contains the database version for Trac.
        """
        current_database_version = self.__get_database_version(name)
        if current_database_version is False:
            self.env.db_transaction(""" INSERT INTO system (name, value) VALUES (%s, %s)""", (name, version))
        else:
            self.env.db_transaction("""UPDATE system SET value=%s WHERE name=%s""", (version, name))
            self.env.log.info("Upgraded %s from %d to %d", name, current_database_version, version)

    def __upgrade(self, version, name='database_version', pkg=None):
        """Invokes `do_upgrade(env, version, cursor)` in module
        `"%s/db%i.py" % (pkg, version)`, for each required version upgrade.

        :param version: the expected integer database version.
        :param name: the name of the entry in the SYSTEM table that contains
                     the database version. Defaults to `database_version`,
                     which contains the database version for Trac.
        :param pkg: the package containing the upgrade modules.

        :raises TracError: if the package or module doesn't exist.
        """
        dbver = self.__get_database_version(name)
        for i in range(dbver + 1, version + 1):
            module = 'db%i' % i
            try:
                upgrades = __import__(pkg, globals(), locals(), [module])
            except ImportError:
                raise TracError("No upgrade package %s" % pkg)
            try:
                script = getattr(upgrades, module)
            except AttributeError:
                raise TracError("No upgrade module %s.py" % module)
            with self.env.db_transaction as db:
                cursor = db.cursor()
                script.do_upgrade(self.env, i, cursor)
                self.__set_database_version(i, name)
