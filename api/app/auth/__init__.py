from qsystem import login_manager
from app.models.theq import CSR


@login_manager.user_loader
def load_user(user_id):
    csr = CSR.query.filter_by(csr_id=int(user_id)).filter(CSR.deleted.is_(None)).first()
    if not csr:
        return None

    if csr.deleted is None:
        csr.is_active = True
    else:
        csr.is_active = False

    csr.is_authenticated = True
    csr.is_anonymous = False

    return csr
