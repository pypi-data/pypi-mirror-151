from kabaret import flow


# Default tasks
# -------------------------


class TaskTemplateChoiceValue(flow.values.SessionValue):

    DEFAULT_EDITOR = 'choice'

    def choices(self):
        mgr = self.root().project().get_task_manager()
        return mgr.task_templates.mapped_names()
    
    def update_default_value(self):
        choices = self.choices()
        if choices:
            self._value = choices[0]
        self.touch()


class CreateDefaultTaskAction(flow.Action):

    ICON = ('icons.gui', 'plus-sign-in-a-black-circle')

    task_name    = flow.SessionParam('')
    display_name = flow.SessionParam('')
    template     = flow.SessionParam(None, TaskTemplateChoiceValue)
    order        = flow.SessionParam(0).ui(editor='int')
    enabled      = flow.SessionParam(True).ui(
        editor='bool',
        tooltip='Dictates if the task must appear in the UI by default')
    optional     = flow.SessionParam(False).ui(
        editor='bool',
        tooltip='Dictates if the task must be created automatically')

    _map      = flow.Parent()

    def get_buttons(self):
        self.template.update_default_value()

        if len(self.template.choices()) == 0:
            self.message.set((
                '<h2>Add default task</h2>'
                '<font color=#D5000D>Please add a template '
                'before creating a default task.</font>'
            ))
            return ['Cancel']
        
        self.message.set('<h2>Add default task</h2>')
        return ['Add', 'Cancel']

    def run(self, button):
        if button == 'Cancel':
            return
        
        self._map.add_default_task(
            self.task_name.get(),
            self.display_name.get(),
            self.template.get(),
            self.order.get(),
            self.enabled.get(),
            self.optional.get()
        )


class DefaultTask(flow.Object):

    display_name = flow.Param() 
    template     = flow.Param()
    enabled      = flow.BoolParam(True)  # Dictates if task must appear int the UI by default
    optional     = flow.BoolParam(False) # Dictates if task must be created automatically


class DefaultTasks(flow.Map):

    add_dft_task = flow.Child(CreateDefaultTaskAction).ui(
        label='Add default task'
    )

    @classmethod
    def mapped_type(cls):
        return DefaultTask

    def add_default_task(self, name, display_name, template_name, order=-1, enabled=True, optional=False):
        if order < 0:
            order = len(self)
        
        dt = self.add(name)
        dt.display_name.set(display_name)
        dt.template.set(template_name)
        dt.enabled.set(enabled)
        dt.optional.set(optional)
        self._mapped_names.set_score(name, order)
        
        self.touch()


# Task templates
# -------------------------


class CreateTaskTemplateAction(flow.Action):

    ICON = ('icons.gui', 'plus-sign-in-a-black-circle')

    template_name = flow.SessionParam('').ui(label='Name')

    _map = flow.Parent()

    def get_buttons(self):
        self.message.set('<h2>Add task template</h2>')
        return ['Add', 'Cancel']

    def run(self, button):
        if button == 'Cancel':
            return
        
        self._map.add(self.template_name.get())
        self._map.touch()


class TaskTemplate(flow.Object):
    pass


class TaskTemplates(flow.Map):

    add_template = flow.Child(CreateTaskTemplateAction)

    @classmethod
    def mapped_type(cls):
        return TaskTemplate


# Task manager
# -------------------------


class TaskManager(flow.Object):
    """
    The task manager embeds an ordered list of default task
    names and a list of task templates
    """

    default_tasks  = flow.Child(DefaultTasks).ui(expanded=True)
    task_templates = flow.Child(TaskTemplates).ui(expanded=True)
