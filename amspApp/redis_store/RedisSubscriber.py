# from ws4redis.subscriber import RedisSubscriber
#
#
from ws4redis.subscriber import RedisSubscriber


class RahsoonRedisSubscriber(RedisSubscriber):

    def parse_response(self):
        result = super(RahsoonRedisSubscriber, self).parse_response()

        return result
    # redis_publisher = RedisPublisher(facility='foobar', broadcast=True)
    # message = RedisMessage('Hello World بهمنی')
    # and somewhere else
    # redis_publisher.publish_message(message)

    # redis_publisher = RedisPublisher(facility='foobar', users=['narimani', 'bahmany'])
    # redis_publisher = RedisPublisher(facility='foobar', users=[SELF],)
    # redis_publisher = None

    # def __init__(self):
    #     self.redis_publisher = RedisPublisher(facility='foobar', broadcast=True)

    # message = RedisMessage('Mmmmmmmmmmmmmmmmmmy God')
    # and somewhere else
    # redis_publisher.publish_message(message)
    # pass

    # def release(self):
    #     result = super(RahsoonRedisSubscriber, self).release()
    #     a = 1

    #
    # def RedisSubscriberReqCallback(request):
    #     token = dict(request.REQUEST).get('token')
    #     if token:
    #         if len(token) > 40:
    #             userID = BasicAuths.objects.filter(token=token)
    #             # Session.objects.filter(session_key=reqse)
    #     # cc = authenticate()
    #     a = 1
