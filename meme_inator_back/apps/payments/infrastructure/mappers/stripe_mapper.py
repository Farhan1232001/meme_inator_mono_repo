from apps.payments.domain.entities.unified_transaction_data_vo import UnifiedTransactionDataVo
from apps.payments.domain.iservices.itransaction_mapper import ITransactionMapper


class StripeMapper(ITransactionMapper):
    def to_unified_transaction(self, webhook_payload: dict) -> UnifiedTransactionDataVo:
        # Logic to map Stripe webhook payload to UnifiedTransactionDataVo
        pass