
def to_sqs_delete_response(successful_ids=None, failed_ids=None):
    to_id_list = lambda lst: [dict(Id=i) for i in (lst or [])]
    return dict(Successful=to_id_list(successful_ids), Failed=to_id_list(failed_ids))
