from cmdpkg.shell import ShellRunnerSettings


class TestShellRunnerSettings:
    def test_start_process_kwargs(self):
        settings = ShellRunnerSettings()

        assert settings.start_process_kwargs == {
            'shell': True,
            'env': settings.env,
            'cwd': settings.cwd,
            'stdin': settings.stdin,
            'stdout': settings.stdout,
            'stderr': settings.stderr
        }
