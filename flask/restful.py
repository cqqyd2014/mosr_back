from abc import ABCMeta, abstractmethod

class TableRestful(object):
    __metaclass__ = ABCMeta
    
    def __init__(self,args,db_session):
        self.args=args
        self.db_session=db_session
        
    def _limit(self):
        if 'limit' in self.args:
            self.q_limit=self.q_order.limit(int(args['limit']))
        else:
            self.q_limit=self.q_order
        
    @abstractmethod
    def _query_parmeter(self):
        pass
    
    @abstractmethod
    def _ordery_by(self):
        pass

    def get_rs_all(self):
        self._query_parmeter()
        self._ordery_by()
        self._limit()
        return self.q_limit.all()
        