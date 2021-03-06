import six


class Message(object):

    '''
    Represents an AMQP message.
    '''

    def __init__(self, body='', delivery_info=None, return_info=None,
                 **properties):
        '''
        :param delivery_info: pass only if messages was received via
          basic.deliver or basic.get_ok; MUST be None otherwise; default: None
        :param return_info: pass only if message was returned via basic.return;
          MUST be None otherwise; default: None
        '''
        if six.PY2:
            if isinstance(body, unicode):
                if 'content_encoding' not in properties:
                    properties['content_encoding'] = 'utf-8'
                body = body.encode(properties['content_encoding'])

        if not isinstance(body, (six.string_types, six.binary_type, bytearray)):
            raise TypeError("Invalid message content type %s" % (type(body)))

        self._body = body
        self._delivery_info = delivery_info
        self._return_info = return_info
        self._properties = properties

    @property
    def body(self):
        return self._body

    def __len__(self):
        return len(self._body)

    def __nonzero__(self):
        '''Have to define this because length is defined.'''
        return True

    def __eq__(self, other):
        if isinstance(other, Message):
            return self._properties == other._properties and \
                self._body == other._body
        return False

    @property
    def delivery_info(self):
        '''delivery_info dict if message was received via basic.deliver or
        basic.get_ok; None otherwise.
        '''
        return self._delivery_info

    @property
    def return_info(self):
        '''return_info dict if message was returned via basic.return; None
        otherwise.
        properties:
            'channel': Channel instance
            'reply_code': reply code (int)
            'reply_text': reply text
            'exchange': exchange name
            'routing_key': routing key
        '''
        return self._return_info

    @property
    def properties(self):
        return self._properties

    def __str__(self):
        return ("Message[body: %s, delivery_info: %s, return_info: %s, "
                "properties: %s]") %\
            (str(self._body).encode('string_escape'),
             self._delivery_info, self.return_info, self._properties)
