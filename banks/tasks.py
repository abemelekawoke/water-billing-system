from celery import shared_task
from .models import BillSync
import requests
import logging

logger = logging.getLogger(__name__)

@shared_task
def sync_bills_task():
    """
    Fetches bill sync data from an external API and updates the database.
    Runs periodically as scheduled by Celery Beat.
    """
    endpoint = 'http://196.189.53.130:28080/enterpriseApi/BillIntegrationResource/billSync'
    api_key = '7264CBE3CED649E6BAA0D47669932E2B.ED1E0A2606AB4DA1B5E93AE779BFAD9C'
    headers = {'Content-Type': 'application/json'}

    # Get all pending BillSync records
    pending_syncs = BillSync.objects.filter(status='Pending')

    if not pending_syncs.exists():
        logger.info("No pending bill sync requests.")
        return "No pending bill sync requests."

    successful_ids = []
    failed_ids = []

    for sync in pending_syncs:
        try:
            data = {
                'startDate': str(sync.start_date),
                'endDate': str(sync.end_date)
            }

            logger.info(f"Syncing bills from {sync.start_date} to {sync.end_date}")

            # Send the request
            response = requests.post(f"{endpoint}?API_KEY={api_key}", json=data, headers=headers)
            response.raise_for_status()  # Raise exception for HTTP errors (4xx, 5xx)

            if response.status_code == 200:
                response_data = response.json()

                if response_data:
                    for bill in response_data:
                        BillSync.objects.update_or_create(
                            bill_id=bill["billId"],
                            defaults={
                                'start_date': sync.start_date,
                                'end_date': sync.end_date,
                                'paid_on': bill["paidOn"],
                                'bank_transaction_reference': bill["bankTransactionReference"],
                                'bank_name': bill["bankName"],
                                'status': 'Completed',
                            }
                        )
                    successful_ids.append(sync.id)
                    logger.info(f"Bill sync from {sync.start_date} to {sync.end_date} succeeded.")
                else:
                    failed_ids.append(sync.id)
                    logger.warning(f"Bill sync failed: No data returned from {sync.start_date} to {sync.end_date}")
            else:
                failed_ids.append(sync.id)
                logger.error(f"Sync request failed with status code {response.status_code} for {sync.start_date} to {sync.end_date}")

        except requests.exceptions.RequestException as e:
            logger.error(f"Error syncing bills for {sync.start_date} to {sync.end_date}: {e}")
            failed_ids.append(sync.id)
        except Exception as e:
            logger.error(f"Unexpected error during sync for {sync.start_date} to {sync.end_date}: {e}")
            failed_ids.append(sync.id)

    # Bulk update statuses
    if successful_ids:
        BillSync.objects.filter(id__in=successful_ids).update(status='Success')
    if failed_ids:
        BillSync.objects.filter(id__in=failed_ids).update(status='Not Success')

    return f"Bill sync completed: {len(successful_ids)} succeeded, {len(failed_ids)} failed."
