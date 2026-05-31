from flask import Blueprint, request, jsonify
from app import db
from app.models import Transaction

webhook_bp = Blueprint('webhook', __name__)

@webhook_bp.route('/midtrans', methods=['POST'])
def midtrans_notification():
    data = request.get_json()
    order_id = data.get('order_id')
    transaction_status = data.get('transaction_status')
    fraud_status = data.get('fraud_status')

    transaction = Transaction.query.filter_by(order_id=order_id).first()
    if not transaction:
        return jsonify({'message': 'Not found'}), 404

    if transaction_status == 'capture' and fraud_status == 'accept':
        transaction.status = 'success'
    elif transaction_status == 'settlement':
        transaction.status = 'success'
    elif transaction_status in ('cancel', 'deny', 'expire'):
        transaction.status = 'failed'
    elif transaction_status == 'pending':
        transaction.status = 'pending'

    db.session.commit()
    return jsonify({'message': 'OK'}), 200