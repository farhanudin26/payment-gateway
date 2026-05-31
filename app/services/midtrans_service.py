import midtransclient
from flask import current_app

def get_snap_client():
    return midtransclient.Snap(
        is_production=current_app.config['MIDTRANS_IS_PRODUCTION'],
        server_key=current_app.config['MIDTRANS_SERVER_KEY']
    )

def get_core_api_client():
    return midtransclient.CoreApi(
        is_production=current_app.config['MIDTRANS_IS_PRODUCTION'],
        server_key=current_app.config['MIDTRANS_SERVER_KEY']
    )

def create_snap_token(order_id, amount, customer):
    snap = get_snap_client()
    transaction = {
        "transaction_details": {
            "order_id": order_id,
            "gross_amount": amount
        },
        "customer_details": {
            "first_name": customer.get('name'),
            "email": customer.get('email'),
            "phone": customer.get('phone', '')
        }
    }
    result = snap.create_transaction(transaction)
    return result.get('token'), result.get('redirect_url')

def create_gopay_transaction(order_id, amount, customer):
    core = get_core_api_client()
    result = core.charge({
        "payment_type": "gopay",
        "transaction_details": {
            "order_id": order_id,
            "gross_amount": amount
        },
        "customer_details": {
            "first_name": customer.get('name'),
            "email": customer.get('email'),
        },
        "gopay": {
            "enable_callback": True,
            "callback_url": "http://localhost:5000"
        }
    })
    deeplink_url = None
    for action in result.get('actions', []):
        if action.get('name') == 'deeplink-redirect':
            deeplink_url = action.get('url')
            break
    return result.get('transaction_id'), deeplink_url

def create_shopeepay_transaction(order_id, amount, customer):
    core = get_core_api_client()
    result = core.charge({
        "payment_type": "shopeepay",
        "transaction_details": {
            "order_id": order_id,
            "gross_amount": amount
        },
        "customer_details": {
            "first_name": customer.get('name'),
            "email": customer.get('email'),
        },
        "shopeepay": {
            "callback_url": "http://localhost:5000"
        }
    })
    deeplink_url = None
    for action in result.get('actions', []):
        if action.get('name') == 'deeplink-redirect':
            deeplink_url = action.get('url')
            break
    return result.get('transaction_id'), deeplink_url

def create_va_transaction(order_id, amount, customer, bank):
    core = get_core_api_client()

    charge_data = {
        "payment_type": "bank_transfer",
        "transaction_details": {
            "order_id": order_id,
            "gross_amount": amount
        },
        "customer_details": {
            "first_name": customer.get('name'),
            "email": customer.get('email'),
        },
        "bank_transfer": {
            "bank": bank
        }
    }

    # Mandiri pakai echannel, bukan bank_transfer biasa
    if bank == 'mandiri':
        charge_data["payment_type"] = "echannel"
        charge_data["echannel"] = {
            "bill_info1": "Pembayaran",
            "bill_info2": "online"
        }
        del charge_data["bank_transfer"]

    result = core.charge(charge_data)

    va_number = None
    bill_key = None
    biller_code = None

    if bank == 'mandiri':
        bill_key = result.get('bill_key')
        biller_code = result.get('biller_code')
        va_number = bill_key  # untuk kompatibilitas
    else:
        va_list = result.get('va_numbers', [])
        if va_list:
            va_number = va_list[0].get('va_number')

    return result.get('transaction_id'), va_number, bill_key, biller_code

def create_qris_transaction(order_id, amount, customer):
    core = get_core_api_client()
    result = core.charge({
        "payment_type": "qris",
        "transaction_details": {
            "order_id": order_id,
            "gross_amount": amount
        },
        "customer_details": {
            "first_name": customer.get('name'),
            "email": customer.get('email'),
        },
        "qris": {
            "acquirer": "gopay"
        }
    })
    qr_url = None
    for action in result.get('actions', []):
        if action.get('name') == 'generate-qr-code':
            qr_url = action.get('url')
            break
    return result.get('transaction_id'), qr_url

def create_alfamart_transaction(order_id, amount, customer):
    core = get_core_api_client()
    result = core.charge({
        "payment_type": "cstore",
        "transaction_details": {
            "order_id": order_id,
            "gross_amount": amount
        },
        "customer_details": {
            "first_name": customer.get('name'),
            "email": customer.get('email'),
        },
        "cstore": {
            "store": "alfamart",
            "message": "Pembayaran"
        }
    })
    return result.get('transaction_id'), result.get('payment_code')

def create_indomaret_transaction(order_id, amount, customer):
    core = get_core_api_client()
    result = core.charge({
        "payment_type": "cstore",
        "transaction_details": {
            "order_id": order_id,
            "gross_amount": amount
        },
        "customer_details": {
            "first_name": customer.get('name'),
            "email": customer.get('email'),
        },
        "cstore": {
            "store": "indomaret",
            "message": "Pembayaran"
        }
    })
    return result.get('transaction_id'), result.get('payment_code')