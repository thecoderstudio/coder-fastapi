Authenticated = "Authenticated"
Allow = "Allow"
Deny = "Deny"
Everyone = "Everyone"

ACE = tuple[str, str, str]
ACL = tuple[ACE, ...]
DEFAULT_ACL: ACL = ((Allow, Everyone, "public"),)


class ACLProvider:
    acl: ACL = ()

    def __init__(self, acl: ACL = ()) -> None:
        self.acl = acl

    def __acl__(self) -> ACL:
        return self.acl + DEFAULT_ACL
