from datetime import datetime
from lxml import etree


def add_customer(name='bill'):
    if name is None:
        raise ValueError('Name is a required field')
    name = name + datetime.now().strftime('%H%s')
    reqXML = """
        <?qbxml version="15.0"?>
        <QBXML>
            <QBXMLMsgsRq onError="stopOnError">
                <CustomerAddRq>
                    <CustomerAdd><Name>{}</Name></CustomerAdd>
                </CustomerAddRq> 
            </QBXMLMsgsRq>
        </QBXML>
        """.format(name)
    return reqXML


def add_credit_card_payment(credit_card='CalOil Card',
    vendor='ODI',
    date='2022-01-01',
    ref_number='3123',
    memo='MEMO',
    expense_account='', 
    amount=102.12, 
    expense_description=''):
        
    reqXML = """
    <?qbxml version="15.0"?>
    <QBXML>
    <QBXMLMsgsRq onError="stopOnError">
        <CreditCardChargeAddRq>
            <CreditCardChargeAdd> <!-- required -->
            <AccountRef> <!-- required -->                                        
                <FullName>{credit_card}</FullName> <!-- optional -->
            </AccountRef>

            <PayeeEntityRef> <!-- optional -->
                <FullName >{vendor}</FullName> <!-- optional -->
            </PayeeEntityRef>
            
            <TxnDate >{date}</TxnDate> <!-- optional -->
            <RefNumber >{ref_number}</RefNumber> <!-- optional -->
            <Memo >{memo}</Memo> <!-- optional -->
            
            <ExpenseLineAdd> <!-- optional, may repeat -->
                <AccountRef> <!-- optional -->
                    <FullName >{expense_account}</FullName> <!-- optional -->
                </AccountRef>
                <Amount >{amount}</Amount> <!-- optional -->
                <Memo >{expense_description}</Memo> <!-- optional -->
            </ExpenseLineAdd>
                    
            </CreditCardChargeAdd>
    </CreditCardChargeAddRq>
    </QBXMLMsgsRq>
    </QBXML>
    """.format(credit_card=credit_card, 
        vendor=vendor,
        date=date,
        ref_number=ref_number,
        memo=memo, 
        expense_account=expense_account,
        amount=amount,
        expense_description=expense_description
        )

    return reqXML



def process_response(response):
        
    qbxml_root = etree.fromstring(response)

    assert qbxml_root.tag == 'QBXML'

    qbxml_msg_rs = qbxml_root[0]

    assert qbxml_msg_rs.tag == 'QBXMLMsgsRs'

    response_body_root = qbxml_msg_rs[0]

    assert  'statusCode' in response_body_root.attrib  

    return response_body_root.attrib