# ruff: noqa: E501

import unittest

from embedchain.chunkers.text import TextChunker
from embedchain.config import ChunkerConfig


class TestTextChunker(unittest.TestCase):
    def test_chunks(self):
        """
        Test the chunks generated by TextChunker.
        # TODO: Not a very precise test.
        """
        chunker_config = ChunkerConfig(chunk_size=10, chunk_overlap=0, length_function=len)
        chunker = TextChunker(config=chunker_config)
        text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit."

        result = chunker.create_chunks(MockLoader(), text)

        documents = result["documents"]

        self.assertGreaterEqual(len(documents), 5)

    # Additional test cases can be added to cover different scenarios

    def test_big_chunksize(self):
        """
        Test that if an infinitely high chunk size is used, only one chunk is returned.
        """
        chunker_config = ChunkerConfig(chunk_size=9999999999, chunk_overlap=0, length_function=len)
        chunker = TextChunker(config=chunker_config)
        text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit."

        result = chunker.create_chunks(MockLoader(), text)

        documents = result["documents"]

        self.assertEqual(len(documents), 1)

    def test_small_chunksize(self):
        """
        Test that if a chunk size of one is used, every character is a chunk.
        """
        chunker_config = ChunkerConfig(chunk_size=1, chunk_overlap=0, length_function=len)
        chunker = TextChunker(config=chunker_config)
        # We can't test with lorem ipsum because chunks are deduped, so would be recurring characters.
        text = """0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ \t\n\r\x0b\x0c"""

        result = chunker.create_chunks(MockLoader(), text)

        documents = result["documents"]

        print(documents)

        self.assertEqual(len(documents), len(text))


class MockLoader:
    def load_data(self, src):
        """
        Mock loader that returns a list of data dictionaries.
        Adjust this method to return different data for testing.
        """
        return [
            {
                "content": src,
                "meta_data": {"url": "none"},
            }
        ]
