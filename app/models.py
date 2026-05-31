from app import db
from datetime import datetime
import uuid

class Transaction(db.Model):
    __tablename__ = 'transactions'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    order_id = db.Column(db.String(100), unique=True, nullable=False)
    amount = db.Column(db.Integer, nullable=False)  # dalam Rupiah
    status = db.Column(db.String(20), default='pending')  # pending, success, failed, cancel
    payment_method = db.Column(db.String(50))
    customer_name = db.Column(db.String(100))
    customer_email = db.Column(db.String(100))
    snap_token = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'order_id': self.order_id,
            'amount': self.amount,
            'status': self.status,
            'customer_name': self.customer_name,
            'created_at': self.created_at.isoformat()
        }