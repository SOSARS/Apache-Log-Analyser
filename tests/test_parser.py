from file_parser import parse_apache_file


def test_parse_apache_file(tmp_path):

    # Fake log data for testing
    fake_log_content = """127.0.0.1 - - [10/Oct/2025:13:55:36 +0000] "GET /index.html HTTP/1.1" 200 2326
192.168.1.1 - - [10/Oct/2025:13:56:12 +0000] "GET /login.php HTTP/1.1" 404 123
127.0.0.1 - - [10/Oct/2025:13:57:01 +0000] "GET /style.css HTTP/1.1" 200 584
192.168.1.1 - - [10/Oct/2025:13:58:22 +0000] "POST /submit HTTP/1.1" 500 0
"""
    # Create a temporary file to write the content to
    # "tmp_path" is a special built-in pytest feature - creates a temp dir to use for testing
    log_file = tmp_path / "test_access.log"
    log_file.write_text(fake_log_content)

    # Define the dictionary output expected for the function to return
    expected_output = {
        "127.0.0.1": {"total": 2, "errors": 0},
        "192.168.1.1": {"total": 2, "errors": 2}
    }

    # Run the function being tested on the fake log file
    actual_output = parse_apache_file(log_file)

    # Check if the actual output is exactly as expected
    assert actual_output == expected_output
