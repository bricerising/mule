from mule.error import messages
import pystache
import time
from pydoc import locate
import mule.validator as validator

class ITask:

    required_fields = []
    dependencies = []

    def __init__(self, args):
        package_ref = self.__class__.__module__.replace('mule.task', '')
        self.task_id = f"{package_ref}.{self.__class__.__name__}".lstrip('.')
        # Include name in task id if one is provided
        if 'name' in args:
            self.task_id =  f"{self.task_id}.{args['name']}"
        if 'dependencies' in args:
            self.dependencies = args['dependencies']
        validator.validateRequiredTaskFieldsPresent(
            self.task_id,
            args,
            self.required_fields
        )

    def getId(self):
        return self.task_id
    
    def evaluateOutputFields(self, job_context):
        for field in self.__dict__.keys():
            if type(self.__dict__[field]) is str:
                self.__dict__[field] = pystache.render(self.__dict__[field], job_context.get_fields())

    def getDependencies(self):
        if type(self.dependencies) is str:
            return self.dependencies.split(' ')
        elif type(self.dependencies) is list:
            return self.dependencies
        return []

    def getDependencyEdges(self):
        dependency_edges = []
        for dependency in self.getDependencies():
            dependency_edges.append((dependency, self.getId()))
        return dependency_edges

    def execute(self, job_context):
        self.evaluateOutputFields(job_context)


class Job(ITask):

    required_fields = [
        'tasks',
        'task_configs'
    ]
    configs = {}

    def __init__(self, args):
        super().__init__(args)
        self.dependencies = args['tasks']
        self.task_configs = args['task_configs']
        if 'configs' in args:
            self.configs = args['configs']
        validator.validateJobFields(self)

    def execute(self, job_context):
        super().execute(job_context)
        self.buildJobContext(job_context)
        tasks_tbd = validator.getValidatedTaskDependencyChain(job_context, self.getDependencyEdges())
        for task in tasks_tbd:
            task_outputs = task.execute(job_context)
            task_id = task.getId()
            job_context.add_field(f"{task_id}.outputs", task_outputs)
            job_context.add_field(f"{task_id}.completed", True)
    
    def buildJobContext(self, job_context):
        for task_config in self.task_configs:
            task_config.update(self.configs)
            validator.validateTaskConfig(task_config)
            if 'name' in task_config:
                job_context.add_field(f"{task_config['task']}.{task_config['name']}.inputs", task_config)
            else:
                job_context.add_field(f"{task_config['task']}.inputs", task_config)

class HelloWorld(ITask):

    def execute(self, job_context):
        super().execute(job_context)
        print('Hello World!')

class Echo(ITask):
    required_fields = [
        'message'
    ]

    def __init__(self, args):
        super().__init__(args)
        self.message = args['message']

    def execute(self, job_context):
        super().execute(job_context)
        print(self.message)
        return {
            'message': self.message
        }
