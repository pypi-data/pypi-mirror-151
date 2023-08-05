from io import BytesIO

from pg8000.core import (
    CoreConnection,
    NULL_BYTE,
    PASSWORD,
    _create_message,
)


def test_handle_AUTHENTICATION_3(mocker):
    """Shouldn't send a FLUSH message, as FLUSH only used in extended-query"""

    mocker.patch.object(CoreConnection, "__init__", lambda x: None)
    con = CoreConnection()
    password = "barbour".encode("utf8")
    con.password = password
    con._flush = mocker.Mock()
    buf = BytesIO()
    con._write = buf.write
    CoreConnection.handle_AUTHENTICATION_REQUEST(con, b"\x00\x00\x00\x03", None)
    assert buf.getvalue() == _create_message(PASSWORD, password + NULL_BYTE)
    # assert buf.getvalue() == b"p\x00\x00\x00\x0cbarbour\x00"


def test_create_message():
    msg = _create_message(PASSWORD, "barbour".encode("utf8") + NULL_BYTE)
    assert msg == b"p\x00\x00\x00\x0cbarbour\x00"


def test_handle_ERROR_RESPONSE(mocker):
    """Check it handles invalid encodings in the error messages"""

    mocker.patch.object(CoreConnection, "__init__", lambda x: None)
    con = CoreConnection()
    con._client_encoding = "utf8"
    CoreConnection.handle_ERROR_RESPONSE(con, b"S\xc2err" + NULL_BYTE + NULL_BYTE, None)
    assert str(con.error) == "{'S': '�err'}"
