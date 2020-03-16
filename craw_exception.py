

def analyse_statcode(json):
    stat_code = json['status']
    if stat_code == '0':
        # only if failed, can a info_code be generated
        info_code = json['infocode']
        if info_code == '10001':
            raise InvaluserkeyException('INVALID_USER_KEY_ERROR')
        if info_code == '10003':
            raise DailyoverlimException('DAILY_QUERY_OVER_LIMIT_ERROR')
        if info_code == '10004':
            raise TooFreqException('ACCESS_TOO_FREQUENT_ERROR')
        if info_code == '20001':
            raise MissReqParaException('MISSING_REQUIRED_PARAMS')
        else:
            #对于一些未知的错误
            raise OtherInfoCodeException("INFOCODE_ERROR:",info_code)

class OtherInfoCodeException(Exception):
    def __init__(self, msg,msg1):
        self.msg = msg
        self.msg1 = msg1

    def __str__(self):
        return self.msg + ':' + self.msg1


class MissReqParaException(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg

class InvaluserkeyException(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


class DailyoverlimException(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


class TooFreqException(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg

class NorouteException(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg

# class RequestatcodeException(Exception):
#     def __init__(self, msg):
#         self.msg = msg
#
#     def __str__(self):
#         return self.msg