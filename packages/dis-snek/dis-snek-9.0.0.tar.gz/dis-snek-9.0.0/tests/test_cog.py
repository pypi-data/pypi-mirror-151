# import pytest
#
# from naff import Cog, Client
#
#
# @pytest.fixture()
# def cog():
#     class TestCog(Cog):
#         """Some test cog"""
#
#         ...
#
#     return TestCog(Client())
#
#
# def test_basic(cog):
#     assert cog.name == "TestCog"
#     assert cog.description == "Some test cog"
