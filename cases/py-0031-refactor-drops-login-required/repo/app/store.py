class _Store:
    """Stand-in for the data layer. It does no access checks: views are expected to be
    behind @login_required, and most methods take the acting user's id first."""
    def __getattr__(self, name):
        def call(*args):
            return (name, args)
        return call


store = _Store()
