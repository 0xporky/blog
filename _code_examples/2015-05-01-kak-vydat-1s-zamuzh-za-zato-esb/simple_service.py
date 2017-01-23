from zato.server.service import Service

REDIS_KEY = 'partner:balance:{}'

class UpdateBalance(Service):

    class SimpleIO:
        output_optional = ('partner_id', 'balance')

    def handle(self):
        partner_id = self.request.payload['partner_id']
        balance = self.request.payload['balance']
        key = REDIS_KEY.format(partner_id)
        self.kvdb.conn.set(key, balance)
        self.kvdb.conn.expire(key, 30)
