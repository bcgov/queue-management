def test_finish_service_query_compiles_without_loader_conflicts(app, db, migrated_database):
    del migrated_database

    from app.resources.theq.citizen.citizen_finish_service import _citizen_finish_service_query

    with app.app_context():
        compiled = _citizen_finish_service_query(1).statement.compile(dialect=db.engine.dialect)

    assert "FROM citizen" in str(compiled)
