from coderfastapi.lib.security import Allow, Authenticated
from coderfastapi.lib.security.acl import DEFAULT_ACL, ACLProvider


def test_acl_provider_acl():
    acl = ((Allow, Authenticated, "authenticated"),)
    provider = ACLProvider(acl)
    assert provider.__acl__() == acl + DEFAULT_ACL
