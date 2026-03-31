from __future__ import annotations


def seed_exam_bcmp_job(app, exam_id: int, *, bcmp_job_id: str, upload_received_ind: int):
    with app.app_context():
        from app.models.bookings import Exam
        from qsystem import db

        exam = Exam.query.filter_by(exam_id=exam_id).first()
        exam.bcmp_job_id = bcmp_job_id
        exam.upload_received_ind = upload_received_ind
        db.session.add(exam)
        db.session.commit()
        return exam.exam_id


def exam_upload_received_ind(app, exam_id: int) -> int | None:
    with app.app_context():
        from app.models.bookings import Exam

        exam = Exam.query.filter_by(exam_id=exam_id).first()
        return exam.upload_received_ind


def exam_invigilator_id(app, exam_id: int) -> int | None:
    with app.app_context():
        from app.models.bookings import Exam

        exam = Exam.query.filter_by(exam_id=exam_id).first()
        return exam.invigilator_id
