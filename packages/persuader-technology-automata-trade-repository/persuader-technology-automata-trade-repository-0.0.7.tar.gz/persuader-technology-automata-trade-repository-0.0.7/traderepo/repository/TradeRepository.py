from cache.holder.RedisCacheHolder import RedisCacheHolder
from core.options.exception.MissingOptionError import MissingOptionError
from core.trade.InstrumentTrade import InstrumentTrade, Status
from coreutility.string.string_utility import is_empty

from traderepo.repository.serialize.trade_deserializer import deserialize_trade
from traderepo.repository.serialize.trade_serializer import serialize_trade

TRADE_KEY = 'TRADE_KEY'


class TradeRepository:

    def __init__(self, options):
        self.options = options
        self.__check_options()
        self.cache = RedisCacheHolder()

    def __check_options(self):
        if self.options is None:
            raise MissingOptionError(f'missing option please provide options {TRADE_KEY}')
        if TRADE_KEY not in self.options:
            raise MissingOptionError(f'missing option please provide option {TRADE_KEY}')

    def build_trade_key(self):
        return self.options[TRADE_KEY]

    def build_historic_trades_key(self):
        trade_key = self.build_trade_key()
        return f'{trade_key}:history'

    def store_trade(self, trade: InstrumentTrade):
        trade_key = self.build_trade_key()
        trade_to_store = serialize_trade(trade)
        self.cache.store(trade_key, trade_to_store)
        self.store_historical_trade(trade)

    def retrieve_trade(self) -> InstrumentTrade:
        trade_key = self.build_trade_key()
        raw_trade = self.cache.fetch(trade_key, as_type=dict)
        return deserialize_trade(raw_trade)

    def store_historical_trade(self, trade: InstrumentTrade):
        if trade.status == Status.EXECUTED and is_empty(trade.order_id) is False:
            historical_trades = self.retrieve_historic_trades()
            if self.is_already_history(trade, historical_trades) is False:
                historical_trades.append(trade)
                entities_to_store = list([serialize_trade(trade) for trade in historical_trades])
                key = self.build_historic_trades_key()
                self.cache.store(key, entities_to_store)

    @staticmethod
    def is_already_history(trade, historical_trades):
        matching_trades = list([ht for ht in historical_trades if ht == trade])
        return len(matching_trades) > 0

    def retrieve_historic_trades(self):
        key = self.build_historic_trades_key()
        raw_entities = self.cache.fetch(key, as_type=list)
        return list([deserialize_trade(raw) for raw in raw_entities])
