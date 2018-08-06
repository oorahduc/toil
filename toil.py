from cement.core import foundation
from cement.core.controller import CementBaseController, expose
from toil_lib.utils import *


class BaseController(CementBaseController):
    class Meta:
        label = 'base'
        description = ""
        arguments = [(['args'],
                      dict(action='store', nargs='*'))]

    @expose(help='list all tasks')
    def list(self):
        counts = count_tasks()
        # print(f"{underline('Orchestrate'):>{15}}")
        tags = get_tags()
        print("")
        for tag in tags:
            tasks = get_tasks_by_tag(tag)
            print("  " + bright(underline(tag[0])) + " [" + str(len(tasks)) + "]")
            display_tasks(tasks)
        print(f"{counts[0]:{3}} notes  \U00002E2D  " + f"{counts[1]} pending  \U00002E2D  " + f"{counts[2]} starred\n")

    @expose(help='create new task')
    def task(self):

        # tasks = load_factory()
        task_args = self.app.pargs.args
        tags, task_name = construct_task(task_args)

        try:
            save_task(task_name, tags)
            print("added new task: " + task_name)
        except Exception as e:
            raise e

    @expose(help='star a task')
    def star(self):
        star_args = self.app.pargs.args
        task_id = get_id(star_args)
        star_task(task_id)
        self.list()

    @expose(help='unstar a task')
    def unstar(self):
        star_args = self.app.pargs.args
        task_id = get_id(star_args)
        unstar_task(task_id)
        self.list()

    @expose(help='check a task as done')
    def check(self):
        check_args = self.app.pargs.args
        task_id = get_id(check_args)
        check_task(task_id)
        self.list()

    @expose(help='uncheck a task, returning it to pending')
    def uncheck(self):
        uncheck_args = self.app.pargs.args
        task_id = get_id(uncheck_args)
        uncheck_task(task_id)
        self.list()

    @expose(help='uncheck a task, returning it to pending')
    def delete(self):
        delete_args = self.app.pargs.args
        task_id = get_id(delete_args)
        delete_task(task_id)
        self.list()


class Toil(foundation.CementApp):
    class Meta:
        label = 'toil'
        extensions = ['json']
        base_controller = 'base'
        handlers = [BaseController]


def main():
    with Toil() as app:
        app.setup()
        app.run()


if __name__ == '__main__':
    main()
