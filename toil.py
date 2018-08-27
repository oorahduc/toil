from sys import argv
from cement.core import foundation
from cement.core.controller import CementBaseController, expose
from toil_lib.engine import *
from toil_lib.style import *

# hack to list tasks by default if no args given.
if len(argv) == 1:
    argv.append("list")


class BaseController(CementBaseController):
    class Meta:
        label = 'base'
        description = ""
        arguments = [(['args'], dict(action='store', nargs='*'))]

    @expose(help='list all tasks')
    def list(self):
        counts = count_tasks()

        untagged = get_untagged_tasks()
        tags = get_tags()
        print("")

        if len(untagged) > 0:
            print("  Untagged" + " [" + str(len(untagged)) + "]")
            display_tasks(untagged)

        for tag in tags:
            tasks = get_tasks_by_tag(tag)
            print("  " + tagline(tag[0]) + " [" + str(len(tasks)) + "]")
            display_tasks(tasks)

        print(f"  {blue(str(counts[0])):{3}} notes  \U00002E2D  " + f"{red(str(counts[1]))} pending  \U00002E2D  " + f"{yellow(str(counts[2]))} starred\n")

    @expose(help='create new task')
    def task(self):

        task_args = self.app.pargs.args
        tags, task_name = construct_task(task_args)

        try:
            save_task(task_name, tags)
            print("added new task: " + task_name)
        except Exception as e:
            raise e
        self.list()

    @expose(help='star a task')
    def star(self):
        star_args = self.app.pargs.args
        # star_tasks(parse_args(star_args))
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

    # toil uncheck @1
    @expose(help='uncheck a task, returning it to pending')
    def uncheck(self):
        uncheck_args = self.app.pargs.args
        task_id = get_id(uncheck_args)
        uncheck_task(task_id)
        self.list()

    # toil delete @1
    @expose(help='delete a task')
    def delete(self):
        delete_args = self.app.pargs.args
        task_id = get_id(delete_args)
        delete_task(task_id)
        self.list()


    # toil priority @1 1
    @expose(help='set priority of a task')
    def priority(self):
        priority_args = self.app.pargs.args
        print(priority_args)
        task_id = get_id(priority_args)
        prioritize(task_id, int(priority_args[1]))
        self.list()

    # toil tag @2 @coding
    @expose(help='tag a task')
    def tag(self):
        tag_args = self.app.pargs.args



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
