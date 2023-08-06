import sys

import nox

nox.options.sessions = ['tests_wagtail215', 'tests_wagtail30']

dj32 = nox.param('3.2', id='dj32')
dj40 = nox.param('4.0', id='dj40')


def install_and_run_tests(session):
    session.install('-r', 'requirements-test.txt')
    session.install('-e', '.[factories]')
    tests = session.posargs or ['tests/']
    session.run(
        'pytest',
        '--cov',
        '--cov-config=pyproject.toml',
        '--cov-report=',
        *tests,
        env={'COVERAGE_FILE': f'.coverage.{session.name}'},
    )
    session.notify('coverage')


@nox.session
@nox.parametrize('django', [dj32])
def tests_wagtail215(session, django):
    session.install(f'django=={django}')
    session.install('wagtail==2.15')
    install_and_run_tests(session)


@nox.session
@nox.parametrize('django', [dj32, dj40])
def tests_wagtail30(session, django):
    if django == '4.0' and sys.version_info.minor < 8:
        session.skip("Django 4.0 requires Python 3.8+")
    session.install(f'django=={django}')
    session.install('wagtail==3.0')
    install_and_run_tests(session)


@nox.session
def coverage(session):
    session.install('coverage[toml]')
    session.run('coverage', 'combine')
    session.run('coverage', 'report', '--show-missing')
    session.run('coverage', 'xml')
    session.run('coverage', 'erase')


@nox.session
def lint(session):
    session.install('pre-commit')
    session.run(
        'pre-commit',
        'run',
        '--all-files',
        '--show-diff-on-failure',
        '--hook-stage=manual',
        *session.posargs,
    )
