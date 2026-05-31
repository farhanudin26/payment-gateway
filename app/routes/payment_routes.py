from flask import Blueprint, request, jsonify, render_template
from app import db
from app.models import Transaction
from app.services.midtrans_service import (
    create_snap_token,
    create_gopay_transaction,
    create_shopeepay_transaction,
    create_va_transaction,
    create_qris_transaction,
    create_alfamart_transaction,
    create_indomaret_transaction
)
import uuid

payment_bp = Blueprint('payment', __name__)

def generate_order_id():
    return f"ORDER-{uuid.uuid4().hex[:8].upper()}"

# --- Halaman HTML ---
@payment_bp.route('/')
def index():
    return render_template('index.html')

@payment_bp.route('/transaksi')
def transaksi():
    return render_template('transaksi.html')

# --- API List ---
@payment_bp.route('/api/payment/list', methods=['GET'])
def list_payments():
    transactions = Transaction.query.order_by(Transaction.created_at.desc()).all()
    return jsonify([t.to_dict() for t in transactions])

# --- API Status ---
@payment_bp.route('/api/payment/status/<order_id>', methods=['GET'])
def payment_status(order_id):
    transaction = Transaction.query.filter_by(order_id=order_id).first_or_404()
    return jsonify(transaction.to_dict())

# --- Snap (semua metode via popup) ---
@payment_bp.route('/api/payment/create', methods=['POST'])
def create_payment():
    data = request.get_json()
    order_id = generate_order_id()
    token, redirect_url = create_snap_token(order_id, data['amount'], data['customer'])
    transaction = Transaction(
        order_id=order_id,
        amount=data['amount'],
        customer_name=data['customer']['name'],
        customer_email=data['customer']['email'],
        payment_method='snap',
        snap_token=token
    )
    db.session.add(transaction)
    db.session.commit()
    return jsonify({'order_id': order_id, 'snap_token': token, 'redirect_url': redirect_url}), 201

# --- GoPay ---
@payment_bp.route('/api/payment/gopay', methods=['POST'])
def create_gopay():
    data = request.get_json()
    order_id = generate_order_id()
    transaction_id, deeplink_url = create_gopay_transaction(order_id, data['amount'], data['customer'])
    _save_transaction(order_id, data, 'gopay')
    simulator_url = f"https://simulator.sandbox.midtrans.com/gopay/ui/index?action=pay&deeplink={deeplink_url}"
    return jsonify({'order_id': order_id, 'deeplink_url': deeplink_url, 'simulator_url': simulator_url}), 201

# --- ShopeePay ---
@payment_bp.route('/api/payment/shopeepay', methods=['POST'])
def create_shopeepay():
    data = request.get_json()
    order_id = generate_order_id()
    transaction_id, deeplink_url = create_shopeepay_transaction(order_id, data['amount'], data['customer'])
    _save_transaction(order_id, data, 'shopeepay')
    simulator_url = f"https://simulator.sandbox.midtrans.com/shopeepay/ui/index?action=pay&deeplink={deeplink_url}"
    return jsonify({'order_id': order_id, 'deeplink_url': deeplink_url, 'simulator_url': simulator_url}), 201

# --- Virtual Account ---
@payment_bp.route('/api/payment/va', methods=['POST'])
def create_va():
    data = request.get_json()
    bank = data.get('bank', 'bca')
    order_id = generate_order_id()

    transaction_id, va_number, bill_key, biller_code = create_va_transaction(
        order_id, data['amount'], data['customer'], bank
    )

    _save_transaction(order_id, data, f'va_{bank}')

    # Simulator URL per bank
    simulator_urls = {
        'bca': f"https://simulator.sandbox.midtrans.com/bca/ui/index?va_number={va_number}",
        'bni': f"https://simulator.sandbox.midtrans.com/bni/ui/index?va_number={va_number}",
        'bri': f"https://simulator.sandbox.midtrans.com/bri/ui/index?va_number={va_number}",
        'mandiri': f"https://simulator.sandbox.midtrans.com/mandiri/ui/index?bill_key={bill_key}&biller_code={biller_code}",
        'permata': f"https://simulator.sandbox.midtrans.com/permata/ui/index?va_number={va_number}",
    }

    response = {
        'order_id': order_id,
        'bank': bank,
        'va_number': va_number,
        'simulator_url': simulator_urls.get(bank, '')
    }

    # Tambahkan info khusus Mandiri
    if bank == 'mandiri':
        response['bill_key'] = bill_key
        response['biller_code'] = biller_code

    return jsonify(response), 201

# --- QRIS ---
@payment_bp.route('/api/payment/qris', methods=['POST'])
def create_qris():
    data = request.get_json()
    order_id = generate_order_id()
    transaction_id, qr_url = create_qris_transaction(order_id, data['amount'], data['customer'])
    _save_transaction(order_id, data, 'qris')
    simulator_url = f"https://simulator.sandbox.midtrans.com/v2/qris/index?qr_url={qr_url}"
    return jsonify({'order_id': order_id, 'qr_url': qr_url, 'simulator_url': simulator_url}), 201

# --- Alfamart ---
@payment_bp.route('/api/payment/alfamart', methods=['POST'])
def create_alfamart():
    data = request.get_json()
    order_id = generate_order_id()
    transaction_id, payment_code = create_alfamart_transaction(order_id, data['amount'], data['customer'])
    _save_transaction(order_id, data, 'alfamart')
    simulator_url = f"https://simulator.sandbox.midtrans.com/alfamart/ui/index?payment_code={payment_code}"
    return jsonify({'order_id': order_id, 'payment_code': payment_code, 'simulator_url': simulator_url}), 201

# --- Indomaret ---
@payment_bp.route('/api/payment/indomaret', methods=['POST'])
def create_indomaret():
    data = request.get_json()
    order_id = generate_order_id()
    transaction_id, payment_code = create_indomaret_transaction(order_id, data['amount'], data['customer'])
    _save_transaction(order_id, data, 'indomaret')
    simulator_url = f"https://simulator.sandbox.midtrans.com/indomaret/ui/index?payment_code={payment_code}"
    return jsonify({'order_id': order_id, 'payment_code': payment_code, 'simulator_url': simulator_url}), 201

# --- Helper simpan transaksi ---
def _save_transaction(order_id, data, method):
    transaction = Transaction(
        order_id=order_id,
        amount=data['amount'],
        customer_name=data['customer']['name'],
        customer_email=data['customer']['email'],
        payment_method=method
    )
    db.session.add(transaction)
    db.session.commit()