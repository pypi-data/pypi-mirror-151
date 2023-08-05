import paydunya


class PaymentAR():
    def __init__(self, master_key,private_key,paydunya_token,store,debug=True):
        """Create an invoice
            Accepts list of store object as initial parameter and
            a dictionary of tokens for accessing the PAYDUNYA API
        """
        self.store = store
        self.PAYDUNYA_ACCESS_TOKENS = {
            'PAYDUNYA-MASTER-KEY': master_key,
            'PAYDUNYA-PRIVATE-KEY': private_key,
            'PAYDUNYA-TOKEN': paydunya_token
        }
        self.paydunya=paydunya
        self.paydunya.debug = debug
        self.paydunya.api_keys = self.PAYDUNYA_ACCESS_TOKENS
    def payment_create(self,total_amount,return_url,return_url_parameter):
        '''
            return_url_parameter = "/?provider="+str(provider.id)
        '''
        store = self.paydunya.Store(name=self.store)
        invoice = self.paydunya.Invoice(store)
        invoice.total_amount = str(total_amount)
        invoice.return_url = return_url+return_url_parameter
        return invoice.create()

    def payment_result(self,token):
        invoice = self.paydunya.Invoice()
        return invoice.confirm(token)

class PaymentDirect():
    
    def __init__(self, master_key,private_key,paydunya_token,store,debug=True):
        """Create an invoice
            without redirection
        """
        self.store = store
        self.PAYDUNYA_ACCESS_TOKENS = {
            'PAYDUNYA-MASTER-KEY': master_key,
            'PAYDUNYA-PRIVATE-KEY': private_key,
            'PAYDUNYA-TOKEN': paydunya_token
        }
        self.paydunya=paydunya
        self.paydunya.debug = debug
        self.paydunya.api_keys = self.PAYDUNYA_ACCESS_TOKENS
    
    def pay_direct(self,account_alias,amount):
        '''
        The account allias can be a email or a telephone("EMAIL_OU_NUMERO_DU_CLIENT_PAYDUNYA")
        '''''
        # Direct Pay
        direct_pay = self.paydunya.DirectPay(account_alias, amount)
        return direct_pay.process()
