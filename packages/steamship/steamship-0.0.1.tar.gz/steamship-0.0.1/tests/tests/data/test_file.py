import json

from steamship import MimeTypes
from steamship.data.block import Block
from steamship.data.file import File
from steamship.data.tags.tag import Tag
from tests.utils.client import get_steamship_client


def test_file_upload():
    steamship = get_steamship_client()
    a = steamship.upload(content="A", mime_type=MimeTypes.MKD).data
    assert a.id is not None
    assert a.mime_type == MimeTypes.MKD

    b = steamship.upload(content="B", mime_type=MimeTypes.TXT).data
    assert b.id is not None
    assert b.mime_type == MimeTypes.TXT
    assert a.id != b.id

    c = steamship.upload(content="B", mime_type=MimeTypes.MKD).data
    assert c.mime_type == MimeTypes.MKD  # The specified format gets precedence over filename

    d = steamship.upload(
        content="B",
    ).data
    assert d.mime_type == MimeTypes.TXT  # The filename is used in a pinch.

    a.delete()
    b.delete()
    c.delete()
    d.delete()


def test_file_scrape():
    steamship = get_steamship_client()

    a = steamship.scrape(url="https://edwardbenson.com/2020/10/gpt3-travel-agent").data
    assert a.id is not None
    assert a.mime_type == MimeTypes.HTML

    b = steamship.scrape(url="https://edwardbenson.com/2018/09/case-of-the-murderous-ai").data
    assert b.id is not None
    assert a.id != b.id
    assert b.mime_type == MimeTypes.HTML

    a.delete()
    b.delete()


def test_file_import_response_dict():
    resp = File.CreateResponse(_bytes=b"some bytes", mime_type=MimeTypes.BINARY)
    to_dict = resp.to_dict()
    from_dict = File.CreateResponse.from_dict(to_dict)
    assert resp.data == from_dict.data
    assert resp.mimeType == from_dict.mimeType


def test_file_import_response_bytes_serialization():
    file_resp = File.CreateResponse(_bytes=b"some bytes", mime_type=MimeTypes.BINARY)
    to_dict = file_resp.to_dict()
    as_json_string = json.dumps(to_dict)
    as_dict_again = json.loads(as_json_string)
    assert as_dict_again == to_dict


def test_file_upload_with_blocks():
    client = get_steamship_client()
    a = File.create(
        client=client,
        blocks=[
            Block.CreateRequest(text="A", tags=[Tag.CreateRequest(name="BlockTag")]),
            Block.CreateRequest(text="B"),
        ],
        tags=[Tag.CreateRequest(name="FileTag")],
    ).data
    assert a.id is not None

    blocks = Block.list_public(client, file_id=a.id)

    def check_blocks(block_list):
        assert len(block_list) == 2
        assert block_list[0].tags is not None
        assert len(block_list[0].tags) == 1
        assert block_list[0].tags[0].name == "BlockTag"
        assert block_list[0].text == "A"

    assert blocks.data.blocks is not None
    check_blocks(blocks.data.blocks)

    # Let's get the file fresh
    aa = File.get(client, _id=a.id).data
    check_blocks(aa.blocks)
    assert aa.tags is not None
    assert len(aa.tags) == 1
    assert aa.tags[0].name == "FileTag"

    a.delete()


def test_query():
    client = get_steamship_client()
    a = File.create(
        client=client,
        blocks=[
            Block.CreateRequest(text="A", tags=[Tag.CreateRequest(name="BlockTag")]),
            Block.CreateRequest(text="B"),
        ],
    ).data
    assert a.id is not None
    b = File.create(
        client=client,
        blocks=[Block.CreateRequest(text="A"), Block.CreateRequest(text="B")],
        tags=[Tag.CreateRequest(name="FileTag")],
    ).data
    assert b.id is not None

    files = File.query(client=client, tag_filter_query='blocktag and name "BlockTag"').data.files
    assert len(files) == 1
    assert files[0].id == a.id

    files = File.query(client=client, tag_filter_query='filetag and name "FileTag"').data.files
    assert len(files) == 1
    assert files[0].id == b.id

    a.delete()
    b.delete()
