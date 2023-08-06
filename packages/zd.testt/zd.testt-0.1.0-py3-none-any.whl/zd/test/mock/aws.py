
class CallTracker(object):
    def __init__(self):
        self.calls = []

    def add_call(self, caller_name, *args, **kwargs):
        self.calls.append(dict(caller_name=caller_name, args=args, kwargs=kwargs))


class MockLambdaClient(CallTracker):
    def __init__(self):
        super(MockLambdaClient, self).__init__()

    def invoke(self, FunctionName, InvocationType, Payload=None):
        assert FunctionName is not None and InvocationType in ['Event', 'RequestResponse', 'DryRun']
        self.add_call('invoke', FunctionName, InvocationType, Payload=Payload)
