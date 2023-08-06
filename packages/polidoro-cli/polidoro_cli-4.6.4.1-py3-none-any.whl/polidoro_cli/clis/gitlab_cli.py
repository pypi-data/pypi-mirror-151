import os
from datetime import timedelta

from polidoro_argument import Command
from time import sleep

from polidoro_cli import CLI
from polidoro_cli.cli.cli import import_dependency



def sort_jobs(j):
    if j.status == 'failed':
        return 9
    for value, status in enumerate(['running', 'pending', 'created', 'success']):
        if status == j.status:
            return value
    return 8


# noinspection PyTypeChecker
class GitLab(CLI):
    @staticmethod
    @Command(aliases=['m'])
    def monitor(*args):
        polidoro_terminal = import_dependency('polidoro_terminal')
        polidoro_table = import_dependency('polidoro_table')
        polidoro_gitlab = import_dependency('polidoro_gitlab')

        pipeline_id = None
        if args:
            pipeline_id = args[0]
        t2 = None
        pipeline = None
        try:
            polidoro_terminal.cursor.hide()
            gl = polidoro_gitlab.GitLab('https://gitlab.buser.com.br/',
                                        private_token=os.environ.get('PRIVATE_TOKEN', ''))
            project = GitLab.get_project(gl)
            if pipeline_id:
                pipeline = project.get_pipeline(pipeline_id)
            else:
                pipeline = GitLab.get_pipeline(project)

            def paint(text, color):
                return f'{color}{text}{polidoro_terminal.Format.NORMAL}'

            def status_color(status):
                return dict(
                    success=polidoro_terminal.Format.BOLD + polidoro_terminal.Color.GREEN,
                    running=polidoro_terminal.Color.CYAN + polidoro_terminal.Format.BLINK,
                    failed=polidoro_terminal.Format.BOLD + polidoro_terminal.Color.LIGHT_RED,
                    pending=polidoro_terminal.Color.YELLOW,
                    others=polidoro_terminal.Format.DIM,
                ).get(status, '')

            properties = [
                polidoro_table.Property(format=status_color('others'),
                                        condition='C("status") in ["skipped", "manual", "created"]'),
                polidoro_table.Property(format=status_color('success'), condition='C("status") == "success"'),
                polidoro_table.Property(format=status_color('failed'), condition='C("status") == "failed"'),
                polidoro_table.Property(format=status_color('pending'), condition='C("status") == "pending"'),
                polidoro_table.Property(format=status_color('running') - polidoro_terminal.Format.BLINK,
                                        condition='C("status") == "running"'),
            ]
            stop = False
            t2 = None
            while not stop:
                t1 = polidoro_table.Table(f'{pipeline.ref} (#{pipeline.id}) - '
                                          f'{paint(pipeline.status, status_color(pipeline.status))} - '
                                          f'{pipeline.web_url}')
                t1.add_columns(['name', 'status', 'queue', 'time', 'url'])
                jobs = list(filter(lambda _j: _j.status == 'pending', project.jobs.list()))

                stop = True
                pipe_jobs = pipeline.get_jobs()
                for j in sorted(pipe_jobs, key=sort_jobs):
                    pos = '-'
                    if j in jobs:
                        pos = jobs.index(j)

                    row = [j.name, j.status, pos]
                    if j.duration:
                        row.append(timedelta(seconds=int(j.duration)))
                    else:
                        row.append('-')
                    row.append(j.web_url)
                    if j.status in ['running', 'pending']:
                        stop = False
                    t1.add_row(row, properties=properties)
                if stop:
                    stop = pipeline.status not in ['running', 'pending']
                    pipeline.refresh()
                t1.print()
                t1.return_table_lines()
                t2 = t1
                sleep(0.5)
        except KeyboardInterrupt:
            polidoro_terminal.clear_to_end_of_line()
            print()
        finally:
            if t2 and pipeline:
                t2.print()
                icon = 'dialog-ok' if pipeline.status in ['success', 'manual'] else 'error'
                CLI.execute(f'notify-send -i {icon} "Pipeline #{pipeline.id} finished"', show_cmd=False)
            if polidoro_terminal.cursor:
                polidoro_terminal.cursor.show()

    @staticmethod
    def get_pipeline(project):
        # return project.get_pipelines()[0]
        branch, _ = CLI.execute('git rev-parse --abbrev-ref HEAD', capture_output=True, show_cmd=False)
        last_commit = project.commits.list(ref_name=branch.strip())[0]
        return project.get_pipeline(sha=last_commit.id)[0]

    @staticmethod
    def get_project(rest):
        polidoro_gitlab = import_dependency('polidoro_gitlab')
        out, _ = CLI.execute('git config --get remote.origin.url', capture_output=True, show_cmd=False)
        project_name = out.split('/')[-1].replace('.git', '').strip()
        projects = rest.projects.list(search=project_name)
        for p in projects:
            if p.path == project_name:
                return polidoro_gitlab.Project(p)
