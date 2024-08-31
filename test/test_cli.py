import io

import pytest
from unittest.mock import patch, MagicMock
from phonebook.cli import determine_consistency
from unittest.mock import patch

@pytest.fixture
def valid_csv():

    csv_data = "Name,Phone Number\njoao,1234 56789\nmaria,9876 54321\n"
    return io.StringIO(csv_data)

@pytest.fixture
def invalid_csv():

    csv_data = "Name,Phone Number\njoao,1234 56789\nmaria,XXXX 54321\n"
    return io.StringIO(csv_data)

def test_determine_consistency_valid(valid_csv):

    determine_consistency(valid_csv)

def test_determine_consistency_invalid(invalid_csv):

    determine_consistency(invalid_csv)

def test_determine_consistency_empty():

    empty_csv = io.StringIO("")
    determine_consistency(empty_csv)

def test_determine_consistency_no_headers():

    no_header_csv = io.StringIO("Name,Phone Number\njoao,1234 56789\nmaria,9876 54321\n")
    determine_consistency(no_header_csv)

def test_determine_consistency_none_type():

    with pytest.raises(TypeError):
        determine_consistency(None)

def test_determine_consistency_missing_values():

    missing_value_csv = io.StringIO("Name,Phone Number\njoao,1234 56789\nmaria,\n")
    determine_consistency(missing_value_csv)

def test_determine_consistency_with_none_book(valid_csv):
    with patch('phonebook.cli.Phonebook', return_value=None):
        with pytest.raises(AttributeError):
            determine_consistency(valid_csv)

@patch('sys.stdout', new_callable=io.StringIO)
def test_determine_consistency_output(mock_stdout, valid_csv):
    
    determine_consistency(valid_csv)
    output = mock_stdout.getvalue().strip()
    expected_output = "Phonebook is consistent: True"
    assert output == expected_output, f"Expected '{expected_output}', but got '{output}'"


def test_determine_consistency_name_not_none(valid_csv):

    with patch('phonebook.cli.Phonebook') as Mock:
        mock_book = MagicMock()
        Mock.return_value = mock_book

        determine_consistency(valid_csv)

        assert mock_book.add.call_count == 2
        mock_book.add.assert_any_call("joao", "1234 56789")
        mock_book.add.assert_any_call("maria", "9876 54321")
