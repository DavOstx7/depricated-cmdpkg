from unittest.mock import patch, Mock

from cmdpkg.process import ProcessRunner, ProcessRunnerSettings, DataStreamer, Command


class TestProcessRunnerSettings:
    def test_start_process_kwargs(self):
        settings = ProcessRunnerSettings()

        assert settings.start_process_kwargs == {
            'env': settings.env,
            'cwd': settings.cwd,
            'stdin': settings.stdin,
            'stdout': settings.stdout,
            'stderr': settings.stderr
        }


class TestProcessRunner:
    @patch('subprocess.Popen')
    def test_run_cmd(self, popen_class_mock: Mock, cmd_factory):
        cmd = cmd_factory()
        settings = ProcessRunnerSettings()
        runner = ProcessRunner(settings=settings)

        return_value = runner._run_cmd(cmd)

        popen_class_mock.assert_called_once_with(cmd, **settings.start_process_kwargs)
        popen_object_mock = popen_class_mock()
        popen_object_mock.wait.assert_called_once_with()
        assert return_value.stdout == popen_object_mock.stdout
        assert return_value.stderr == popen_object_mock.stderr
        assert return_value.exit_code == popen_object_mock.returncode

    @patch('subprocess.Popen')
    @patch.object(DataStreamer, 'stream')
    def test_run_command_with_stdin(self, stream_mock: Mock, popen_class_mock: Mock, cmd_factory, timeout_factory,
                                    binary_io_factory):
        command = Command(cmd_factory(), timeout=timeout_factory(), stdin=binary_io_factory())
        settings = ProcessRunnerSettings()
        streamer = DataStreamer()
        runner = ProcessRunner(settings=settings, streamer=streamer)

        return_value = runner._run_command(command)

        popen_class_mock.assert_called_once_with(command.cmd, **settings.start_process_kwargs)
        popen_object_mock = popen_class_mock()
        stream_mock.assert_called_once_with(source=command.stdin, destination=popen_object_mock.stdin)
        popen_object_mock.wait.assert_called_once_with(command.timeout)
        assert return_value.stdout == popen_object_mock.stdout
        assert return_value.stderr == popen_object_mock.stderr
        assert return_value.exit_code == popen_object_mock.returncode

    @patch('subprocess.Popen')
    @patch.object(DataStreamer, 'stream')
    def test_run_command_without_stdin(self, stream_mock: Mock, popen_class_mock: Mock, cmd_factory, timeout_factory,
                                       binary_io_factory):
        command = Command(cmd_factory(), timeout=timeout_factory())
        settings = ProcessRunnerSettings()
        streamer = DataStreamer()
        runner = ProcessRunner(settings=settings, streamer=streamer)

        return_value = runner._run_command(command)

        popen_class_mock.assert_called_once_with(command.cmd, **settings.start_process_kwargs)
        popen_object_mock = popen_class_mock()
        stream_mock.assert_not_called()
        popen_object_mock.wait.assert_called_once_with(command.timeout)
        assert return_value.stdout == popen_object_mock.stdout
        assert return_value.stderr == popen_object_mock.stderr
        assert return_value.exit_code == popen_object_mock.returncode
