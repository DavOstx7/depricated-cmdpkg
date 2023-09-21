from cmdpkg.shell import ShellRunnerSettings


def test_shell_runner_settings():
    settings = ShellRunnerSettings()

    assert settings.start_process_kwargs == {
        'shell': True,
        'env': settings.env,
        'cwd': settings.cwd,
        'stdin': settings.stdin,
        'stdout': settings.stdout,
        'stderr': settings.stderr
    }
