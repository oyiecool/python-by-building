rows = db.execute(sql + " ORDER BY spent_on DESC, id DESC LIMIT ?", [*args, limit]).fetchall()
