
from django.core.management.base import BaseCommand
from django.db import transaction
from random import choice, randint
from task3.models import User, Transaction
from task3.transaction_utils import deposit, save_transaction, withdraw, transfer

class Command(BaseCommand):
    help = 'Runs 50 asynchronous transactions (deposits, withdrawals, transfers)'

    def handle(self, *args, **options):
        with transaction.atomic(): 
            for _ in range(50):
                operation = choice(['deposit', 'withdraw', 'transfer'])
                if operation == 'deposit':
                    user = choice(User.objects.all())
                    amount = randint(100, 1000)
                    deposit.delay(user.id, amount)
                    save_transaction.delay('DEPOSIT', amount, user.id, user.id)
                elif operation == 'withdraw':
                    user = choice(User.objects.all())
                    amount = randint(50, 500)
                    withdraw.delay(user.id, amount)
                    save_transaction.delay('WITHDRAW', amount, user.id, user.id)
                elif operation == 'transfer':
                    from_user = choice(User.objects.all())
                    to_user = choice(User.objects.exclude(pk=from_user.pk))
                    amount = randint(100, 1000)
                    transfer.delay(from_user.id, to_user.id, amount)
                    save_transaction.delay('TRANSFER', amount, from_user.id, to_user.id)

        self.stdout.write(self.style.SUCCESS('Successfully queued 50 transactions.'))
