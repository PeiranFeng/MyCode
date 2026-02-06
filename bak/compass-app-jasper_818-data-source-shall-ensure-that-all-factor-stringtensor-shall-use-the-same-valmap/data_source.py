import torch

from datetime import datetime
from pathlib import Path
from omegaconf import OmegaConf

from lib.io.parquet import load as pq_load
from lib.data._tensor_.string import Tensor as StringTensor
from _data_ import StockTradeMask
from data._data_set_ import DataSet
from data._stock_data_ import StockData
from data._market_data_ import MarketData
from data._market_reference_ import MarketReference
from schema import Schema

class DataSource:
    def __init__(self, schema, path, window):
        print(f"""
            Warning: The `window` parameter of DataSource represents a datetime range {window}. 
            Please verify that the datetime column corresponds to the observed time.
        """)
        if OmegaConf.is_config(schema):
            schema = OmegaConf.to_container(schema, resolve=True)
        self.schema = Schema(tables=schema)
        if Path(path).is_absolute():
            self.path = path
        else:
            self.path = str(Path(__file__).parent.absolute() / path)

        # output
        self.data_set = DataSet()
        self.stock_trade_mask = None

        # time window range
        window = window if window is not None else []
        self.window = tuple(window)
        if len(self.window) == 2:
            window_start, window_end = self.window
            assert window_end >= window_start, "window_start must be <= window_end."
            self.window_start = self._strpdate(window_start)
            self.window_end = self._strpdate(window_end)
        elif len(self.window) == 0:
            print("Warning: `window` is not limited by the Hydra configuration. It will load the full date range when calling the `self.load` method.")
            self.window_start = None
            self.window_end = None
        else:
            raise RuntimeError("`window` length must be 2 or 0")

    def _strpdate(self, date):
        if isinstance(date, str):
            date = datetime.strptime(date, "%Y-%m-%d").date()
        return date

    def _pq_load(self, table, cols):
        assert isinstance(cols, list) and len(cols) > 0, 'cols cannot be empty.'
        
        file = table.get('file', None)
        assert file is not None, f"{table} must have the file option."

        data_path = f"{self.path}/{file}"

        filters = [
            [
                ('date', '>=', self.window_start), 
                ('date', '<=', self.window_end)
            ]
        ] if self.window_start and self.window_end else None

        df = pq_load(
            data_path,
            columns=[*cols],
            filters=filters
        )
        return df

    def _forloop_cols(self, table):
        static_columns = ['date']
        is_stock = False
        if self.schema.is_stock_tab(table):
            is_stock = True
            static_columns.append('stock_id')

        for col in table['columns']:
            name = col.get('name', None)

            # skip non-feature columns
            if not self.schema.is_feature(option=col):
                continue
            if name in static_columns or name is None:
                continue

            # load parquet file as DataFrame
            df = self._pq_load(table, [*static_columns, name])

            # Consolidate reference
            if is_stock:
                self.data_set.stock.reference.cat_single_reference(
                    df['stock_id'], 'stock'
                )
                self.data_set.stock.reference.cat_single_reference(
                    name, 'factor'
                )
            else:
                self.data_set.market.reference.cat_single_reference(
                    name, 'factor'
                )
            
            # Drop nans from input data before consolidating
            df = df.drop_nans()
            # Consolidate data
            if is_stock:
                data = StockData(
                    time=df['date'],
                    factor=StringTensor([name] * df.nrows()),
                    stock=df['stock_id'],
                    value=df[name],
                    factor_range={name: (0, df.nrows())}
                )
                self.data_set.stock.data.cat(data)
            else:
                data = MarketData(
                    time=df['date'],
                    factor=StringTensor([name] * df.nrows()),
                    value=df[name],
                    factor_range={name: (0, df.nrows())}
                )
                self.data_set.market.data.cat(data)
    
    def _load_tradability_mask(self):
        # Get parquet the table object
        tab = self.schema.tables.get(self.schema.limit_data_table, None)
        assert tab is not None, f"Cannot find {self.schema.limit_data_table} in the schema."

        # Load parquet data
        cols = ['date', 'stock_id', 'long_limit', 'short_limit']
        df = self._pq_load(table=tab,cols=cols)

        # Concatenate stock ids
        self.data_set.stock.reference.cat_single_reference(df['stock_id'], 'stock')

        # Cut limit data as float32
        df['long_limit'] = df['long_limit'].to(torch.float32)
        df['short_limit'] = df['short_limit'].to(torch.float32)
    
        return df
    
    def _load_index_chg_ratio(self):
        path = f"{self.path}/{self.schema.index_file}"
        df = pq_load(
            source=path,
            columns=['date', 'chg_ratio']
        ).drop_nans()
        df['value'] = df.pop('chg_ratio')
        df['name'] = StringTensor([self.schema.index] * df.nrows())
        return df

    def load(self):
        tables = self.schema.tables

        for _, table in tables.items():
            if self.schema.is_feature(option=table):
                self._forloop_cols(table)

        # Load tradability mask(non-feature)
        limit_df = self._load_tradability_mask()
        self.data_set.stock.reference.cat_single_reference(
            limit_df['date'],
            'time'
        )
        self.data_set.stock.reference.cat_single_reference(
            limit_df['stock_id'],
            'stock'
        )

        # Load Index chg_ratio
        index_df = self._load_index_chg_ratio()
        index_data = MarketData(
            time=index_df['date'],
            factor=index_df['name'],
            value=index_df['value'],
            factor_range={self.schema.index:(0, index_df.nrows())}
        )
        index_reference = MarketReference(
            time=index_df['date'],
            factor=self.schema.index,
        )
        self.data_set.market.data.cat(index_data)
        self.data_set.market.reference.cat(index_reference)

        # Set reference time
        stock_price_data = self.data_set.stock.data.slice(self.schema.chg_ratio)
        self.data_set.stock.reference.set_field(
            field='time',
            value=stock_price_data.time
        )
        self.data_set.market.reference.set_field(
            field='time',
            value=index_reference.time
        )

        self.data_set = self.data_set.refresh()
        self.data_set = self.data_set.cuda()
        
        # Generate the Limit data
        limit_df = limit_df.drop_nans()
        for k in limit_df.keys():
            limit_df[k] = limit_df[k].cuda()
        self.stock_trade_mask = StockTradeMask(
            time = limit_df['date'],
            stock = limit_df['stock_id'],
            long_limit = limit_df['long_limit'],
            short_limit = limit_df['short_limit']
        )
        return self

if __name__ == '__main__':
    import hydra
    from omegaconf import DictConfig

    @hydra.main(version_base=None, config_path="conf", config_name="train")
    def test(cfg: DictConfig) -> None:
        ds = hydra.utils.instantiate(cfg.data_source)
        ds = ds.load()
        for _ in [
            ds.data_set.stock.data.time,
            ds.data_set.stock.data.factor,
            ds.data_set.stock.data.stock,
            ds.data_set.stock.data.value,
            ds.data_set.market.data.time,
            ds.data_set.market.data.factor,
            ds.data_set.market.data.value,
            ds.data_set.stock.reference.time,
            ds.data_set.stock.reference.factor,
            ds.data_set.stock.reference.stock,
            ds.data_set.market.reference.time,
            ds.data_set.market.reference.factor,
            ds.stock_trade_mask.time,
            ds.stock_trade_mask.stock,
            ds.stock_trade_mask.short_limit,
            ds.stock_trade_mask.long_limit
        ]:
            assert isinstance(_, torch.Tensor)
            assert _.dim() == 1
            assert _.is_cuda
            assert _.is_contiguous()

        valmap = ds.data_set.stock.reference.factor.valmap
        assert ds.data_set.market.reference.factor.valmap == valmap
        assert ds.data_set.stock.data.factor.valmap == valmap
        assert ds.data_set.market.data.factor.valmap == valmap

        assert torch.equal(
            ds.data_set.stock.reference.time,
            ds.data_set.market.reference.time,
        )
    test()