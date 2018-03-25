def test_mkdir(mocker):
    mocker.patch('pathlib.Path')
    UnixFS.rm('file')
    os.remove.assert_called_once_with('file')