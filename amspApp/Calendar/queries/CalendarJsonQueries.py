import json


def calendarGetDateBetweenAggregate():
    return (
        {"$project":
            {
                "year": {"$year": "$startDate"},
                "month": {"$month": "$startDate"},
                "day": {"$dayOfMonth": "$startDate"}
            }
        },
        {"$group": {
            "_id": {"year": "$year", "month": "$month", "day": "$day", "finished":"$finished"},
            # "seen": {"year": "$year", "month": "$month", "day": "$day"},
            "count": {"$sum": 1},

        }
        }
    )


def InboxGetDateBetweenAggregate():
    return (
        {"$project":
            {
                "year": {"$year": "$dateOfObservable"},
                "month": {"$month": "$dateOfObservable"},
                "day": {"$dayOfMonth": "$dateOfObservable"}
            }
        },
        {"$group": {
            "_id": {"year": "$year", "month": "$month", "day": "$day"},
            "count": {"$sum": 1},

        }
        }
    )
