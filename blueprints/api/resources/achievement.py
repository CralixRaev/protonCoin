
class AchievementList()

count, records = AchievementQuery.get_achievements()
    marshalled_records = marshal(records, achievement_fields)
    print({
        "draw": int(request.args.get("draw")),
        "recordsTotal": AchievementQuery.get_total_count(),
        "recordsFiltered": count,
        "data": marshalled_records
    })
    return {
        "draw": int(request.args.get("draw")),
        "recordsTotal": AchievementQuery.get_total_count(),
        "recordsFiltered": count,
        "data": marshalled_records
    }