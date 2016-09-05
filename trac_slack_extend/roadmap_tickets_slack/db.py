from trac.core import Component, implements
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
        dbm.set_database_version(PLUGIN_VERSION, PLUGIN_NAME)

    def environment_needs_upgrade(self, db):
        """
        Called when Trac checks whether the environment needs to be upgraded.
        Returns `True` if upgrade is needed, `False` otherwise.
        """
        dbm = DatabaseManager(self.env)
        return dbm.needs_upgrade(PLUGIN_VERSION, PLUGIN_NAME)

    def upgrade_environment(self, db):
        """
        Actually perform an environment upgrade, but don't commit as
        that is done by the common upgrade procedure when all plugins are done.
        """
        dbm = DatabaseManager(self.env)
        if dbm.get_database_version(PLUGIN_NAME) == 0:
            dbm.create_tables(SCHEMA)
            dbm.set_database_version(PLUGIN_VERSION, PLUGIN_NAME)
        else:
            dbm.upgrade(PLUGIN_VERSION, PLUGIN_NAME, 'trac_slack_extend.roadmap_tickets_slack.db_upgrades')