from zato.server.service import Service

REDIS_KEY = 'partner:balance:{}'

class GetBalance(Service):

    class SimpleIO:
        output_optional = ('partner_id', 'balance')


    def handle(self):

        partner_id = self.request.payload['partner_id']
        key = REDIS_KEY.format(partner_id)

        partner_balance = self.kvdb.conn.get(key)

        if (partner_balance):
            self.response.payload.partner_id = partner_id
            self.response.payload.balance = partner_balance
        else:
            conn = self.outgoing.soap.get('Partner balance').conn
            with conn.client() as client:
                response = client.service.getPartnerBalance(partner_id)
                code = response['Meta']['Code']
                if (int(code) == 200):
                    partner_balance = response['Data']['Balance']
                    self.kvdb.conn.set(key, partner_balance)
                    self.kvdb.conn.expire(key, 30)
                    self.response.payload.partner_id = partner_id
                    self.response.payload.balance = partner_balance
                else:
                    self.response.payload.partner_id = partner_id
                    self.response.payload.balance = 0
