from kabaret import flow
from kabaret.flow_entities.entities import Entity, Property

from ..utils.kabaret.flow_entities.entities import EntityView
from .file import FileSystemMap
from .maputils import SimpleCreateAction


class Task(Entity):
    """
    Defines an arbitrary task containing a list of files.

    Instances provide the `task` and `task_display_name` keys
    in their contextual dictionary (`settings` context).
    """
    
    display_name = Property().ui(hidden=True)
    enabled      = Property().ui(hidden=True, editor='bool')

    files = flow.Child(FileSystemMap).ui(
        expanded=True,
        action_submenus=True,
        items_action_submenus=True
    )

    @classmethod
    def get_source_display(cls, oid):
        split = oid.split('/')
        return f'{split[3]} · {split[5]} · {split[7]} · {split[9]}'
    
    def get_default_contextual_edits(self, context_name):
        if context_name == 'settings':
            return dict(
                task=self.name(),
                task_display_name=self.display_name.get(),
            )


class TaskCollection(EntityView):
    """
    Defines a collection of tasks.
    """

    add_task = flow.Child(SimpleCreateAction)

    @classmethod
    def mapped_type(cls):
        return flow.injection.injectable(Task)
    
    def collection_name(self):
        mgr = self.root().project().get_entity_manager()
        return mgr.get_task_collection().collection_name()
